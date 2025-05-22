import math
import requests
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String, Float64
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Quaternion, Twist
from tf_transformations import euler_from_quaternion, quaternion_from_euler
from nav2_msgs.action import FollowWaypoints
from rclpy.action import ActionClient
from pyproj import Transformer

def normalize_angle(yaw: float) -> float:
    return math.atan2(math.sin(yaw), math.cos(yaw))

class OSRMAutopilot(Node):
    def __init__(self):
        super().__init__('osrm_autopilot')
        self.get_logger().info('OSRM Autopilot 노드 초기화...')

        # GPS fix storage
        self.fix = None
        self.create_subscription(NavSatFix, '/fix', self.fix_cb, 10)

        # Goal latitude/longitude
        self.goal_lat = None
        self.goal_lon = None
        self.create_subscription(String, '/autopilot/goal', self.goal_cb, 10)

        # Publisher: initial yaw offset for GPSHeadingFuser
        self.offset_pub = self.create_publisher(Float64, '/initial_yaw_offset', 10)

        # Publisher: cmd_vel for calibration drive
        qos = QoSProfile(depth=1)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', qos)

        # **New**: Subscribe to fused odom to get current odom yaw
        self.latest_odom_yaw = None
        self.create_subscription(Odometry, '/odom_fused', self.odom_cb, 10)

        # Transformer for WGS84 → UTM
        self.transformer = Transformer.from_crs(
            'epsg:4326', 'epsg:32652', always_xy=True
        )

        # Waypoint follower action client
        self.cli = ActionClient(self, FollowWaypoints, 'follow_waypoints')

    def odom_cb(self, msg: Odometry):
        # Save latest odom yaw for offset calculation
        q = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        self.latest_odom_yaw = yaw

    def calibrate_initial_yaw(self, speed=0.2):
        # 1) Wait for first GPS fix
        while rclpy.ok() and self.fix is None:
            rclpy.spin_once(self, timeout_sec=0.1)
        lat0, lon0 = self.fix.latitude, self.fix.longitude
        e0, n0, _, _ = self.transformer.transform(lon0, lat0)

        # 2) Drive straight until 1m movement
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = 0.0
        self.get_logger().info('초기 yaw 보정을 위해 직진 시작...')
        while rclpy.ok():
            self.cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.fix is None:
                continue
            e1, n1, _, _ = self.transformer.transform(
                self.fix.longitude, self.fix.latitude
            )
            if math.hypot(e1 - e0, n1 - n0) >= 1.0:
                break

        # 3) Stop robot
        self.cmd_pub.publish(Twist())
        self.get_logger().info('직진 완료, 초기 yaw 계산 중...')

        # 4) Compute true yaw from GPS
        dy = n1 - n0
        dx = e1 - e0
        true_yaw = normalize_angle(math.atan2(dy, dx))
        self.get_logger().info(f'초기 true_yaw: {true_yaw:.3f} rad')
        
        for _ in range(10):  # 10번 * 0.1초 = 최대 1초 대기
            if self.latest_odom_yaw is not None:
                break
            self.get_logger().debug('Waiting for latest_odom_yaw to be updated...')
            rclpy.spin_once(self, timeout_sec=0.1)
      
        # 5) Calculate real offset = true_yaw - odom_yaw
        if self.latest_odom_yaw is None:
            self.get_logger().warn(
                'odom yaw 정보 없음—true_yaw를 offset으로 사용합니다.'
            )
            offset = true_yaw
        else:
            offset = normalize_angle(true_yaw - self.latest_odom_yaw)
            self.get_logger().info(
                f'Offset 계산: true={true_yaw:.3f}, odom={self.latest_odom_yaw:.3f}, offset={offset:.3f}'
            )

        # 6) Publish the correct offset
        self.offset_pub.publish(Float64(data=offset))
        self.get_logger().info(f'Initial yaw offset published: {offset:.3f}')


    def run(self):
        # Wait for GPS and goal
        while rclpy.ok() and (self.fix is None or self.goal_lat is None):
            rclpy.spin_once(self, timeout_sec=0.1)

        # Calibrate initial yaw
        self.calibrate_initial_yaw()

        # Proceed with OSRM routing...
        lat0, lon0 = self.fix.latitude, self.fix.longitude
        lat_goal, lon_goal = self.goal_lat, self.goal_lon

        url = f"http://router.project-osrm.org/route/v1/foot/{lon0},{lat0};{lon_goal},{lat_goal}"
        params = {'overview': 'full', 'geometries': 'geojson'}
        self.get_logger().info(f'OSRM 요청: {url}')
        try:
            resp = requests.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            self.get_logger().error(f'OSRM 호출 실패: {e}')
            return

        coords = data.get('routes', [])[0]['geometry']['coordinates']
        if not coords:
            self.get_logger().error('OSRM 경로를 찾을 수 없습니다.')
            return

        # Build PoseStamped list in UTM-relative frame
        x0, y0 = self.transformer.transform(lon0, lat0)
        poses = []
        for i, (lon, lat) in enumerate(coords):
            x, y = self.transformer.transform(lon, lat)
            ps = PoseStamped()
            ps.header.frame_id = 'utm'
            ps.header.stamp = self.get_clock().now().to_msg()
            ps.pose.position.x = x - x0
            ps.pose.position.y = y - y0
            # Compute orientation toward next point
            if i < len(coords) - 1:
                lon2, lat2 = coords[i+1]
                x2, y2 = self.transformer.transform(lon2, lat2)
                yaw = math.atan2(y2 - y, x2 - x)
            else:
                yaw = 0.0
            yaw = normalize_angle(yaw)
            ps.pose.orientation = Quaternion(
                x=0.0, y=0.0,
                z=math.sin(yaw / 2.0),
                w=math.cos(yaw / 2.0)
            )
            poses.append(ps)

        # Send FollowWaypoints action
        self.get_logger().info('FollowWaypoints 액션 서버 연결 대기...')
        self.cli.wait_for_server()
        goal_msg = FollowWaypoints.Goal(poses=poses)
        self.get_logger().info('웨이포인트 목표 전송')
        send_goal_future = self.cli.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('웨이포인트 목표 거부됨')
        else:
            self.get_logger().info('웨이포인트 목표 수락됨')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_result)

    def on_result(self, future):
        result = future.result().result
        self.get_logger().info(f'FollowWaypoints 결과: {result}')


def main():
    rclpy.init()
    node = OSRMAutopilot()
    node.run()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()