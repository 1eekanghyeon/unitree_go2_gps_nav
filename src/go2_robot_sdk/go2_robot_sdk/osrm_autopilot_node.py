#!/usr/bin/env python3
"""
OSRM API로 보행자 경로를 얻어와 Nav2 FollowWaypoints로 주행하는 노드
"""
import math
import requests
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import FollowWaypoints
from pyproj import Transformer


class OSRMAutopilot(Node):
    def __init__(self):
        super().__init__('osrm_autopilot')
        self.get_logger().info('OSRM Autopilot 노드 초기화...')

        # 1) GPS fix 구독
        self.fix = None
        self.create_subscription(NavSatFix, '/fix', self.fix_cb, 10)

        # 2) 목표 위·경도 구독 (std_msgs/String: "lat,lon")
        self.goal_lat = None
        self.goal_lon = None
        self.create_subscription(String, '/autopilot/goal', self.goal_cb, 10)

        # 3) 좌표 변환기: WGS84(lat/lon) → UTM zone 52N (필요에 따라 EPSG 코드 수정)
        self.transformer = Transformer.from_crs(
            "epsg:4326",
            "epsg:32652",
            always_xy=True
        )

        # 4) FollowWaypoints 액션 클라이언트
        self.cli = ActionClient(self, FollowWaypoints, 'follow_waypoints')

    def fix_cb(self, msg: NavSatFix):
        if msg.status.status >= msg.status.STATUS_SBAS_FIX and self.fix is None:
            self.fix = msg
            self.get_logger().info(f'Received GPS fix: lat={msg.latitude}, lon={msg.longitude}')

    def goal_cb(self, msg: String):
        if self.goal_lat is None:
            try:
                lat, lon = map(float, msg.data.split(','))
                self.goal_lat = lat
                self.goal_lon = lon
                self.get_logger().info(f'Received goal: lat={lat}, lon={lon}')
            except Exception as e:
                self.get_logger().error(f'Goal parsing error: {e}')

    def run(self):
        # 5) GPS 확보 대기
        self.get_logger().info('GPS 수신 대기 중...')
        while rclpy.ok() and self.fix is None:
            rclpy.spin_once(self, timeout_sec=0.1)

        # 6) 목표 위·경도 메시지 대기
        self.get_logger().info('목표 수신 대기 중... topic: /autopilot/goal')
        while rclpy.ok() and (self.goal_lat is None or self.goal_lon is None):
            rclpy.spin_once(self, timeout_sec=0.1)

        lat0, lon0 = self.fix.latitude, self.fix.longitude
        lat_goal, lon_goal = self.goal_lat, self.goal_lon

        # 7) OSRM API 호출
        url = f"http://router.project-osrm.org/route/v1/foot/{lon0},{lat0};{lon_goal},{lat_goal}"
        params = {'overview':'full', 'geometries':'geojson'}
        self.get_logger().info(f'OSRM 요청: {url}')
        try:
            resp = requests.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            self.get_logger().error(f'OSRM 호출 실패: {e}')
            rclpy.shutdown()
            return

        coords = data.get('routes', [])[0]['geometry']['coordinates']
        if not coords:
            self.get_logger().error('OSRM 경로를 찾을 수 없습니다.')
            rclpy.shutdown()
            return

        # 8) PoseStamped 리스트 작성
        self.get_logger().info(f'경로 점 개수: {len(coords)}')
        x0, y0 = self.transformer.transform(lon0, lat0)
        poses = []

        for i, (lon, lat) in enumerate(coords):
            x, y = self.transformer.transform(lon, lat)
            ps = PoseStamped()
            ps.header.frame_id = 'utm'
            ps.header.stamp = self.get_clock().now().to_msg()
            ps.pose.position.x = x - x0
            ps.pose.position.y = y - y0
            # orientation: 다음 점 향하도록 yaw 계산
            if i < len(coords) - 1:
                lon2, lat2 = coords[i+1]
                x2, y2 = self.transformer.transform(lon2, lat2)
                yaw = math.atan2(y2 - y, x2 - x)
            else:
                yaw = 0.0
            ps.pose.orientation = Quaternion(
                x=0.0,
                y=0.0,
                z=math.sin(yaw / 2.0),
                w=math.cos(yaw / 2.0)
            )
            poses.append(ps)

        # 9) FollowWaypoints 액션 전송
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
            rclpy.shutdown()
            return
        self.get_logger().info('웨이포인트 목표 수락됨')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_result)

    def on_result(self, future):
        result = future.result().result
        self.get_logger().info(f'FollowWaypoints 결과: {result}')
        rclpy.shutdown()


def main():
    rclpy.init()
    node = OSRMAutopilot()
    node.run()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()