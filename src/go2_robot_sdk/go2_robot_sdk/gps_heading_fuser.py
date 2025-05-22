import math
import utm
import copy
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
from tf_transformations import euler_from_quaternion, quaternion_from_euler


def normalize_angle(yaw: float) -> float:
    """
    Normalize angle to be within [-pi, pi].
    """
    return math.atan2(math.sin(yaw), math.cos(yaw))


class GPSHeadingFuser(Node):
    def __init__(self):
        super().__init__('gps_heading_fuser')
        # GPS UTM coordinates
        self.current_e = None
        self.current_n = None
        self.prev_e = None
        self.prev_n = None
        # Yaw offset
        self.offset = 0.0
        # Movement thresholds
        self.distance_threshold = 1.0  # meters
        self.linear_threshold = 0.1    # m/s
        self.angular_threshold = 0.05  # rad/s

        # Subscriptions
        self.create_subscription(
            Odometry,
            '/odometry/global_filtered',
            self.odom_callback,
            10
        )
        self.create_subscription(
            NavSatFix,
            '/fix',
            self.gps_callback,
            10
        )
        self.create_subscription(
            Float64,
            '/initial_yaw_offset',
            self.initial_yaw_cb,
            10
        )

        # Publisher for corrected odometry
        self.fused_pub = self.create_publisher(Odometry, '/odom_fused', 10)

    def initial_yaw_cb(self, msg: Float64):
        # Apply initial yaw offset in ENU frame
        self.offset = normalize_angle(msg.data)
        self.get_logger().info(f'Initial yaw offset set to {self.offset:.3f} rad')

    def gps_callback(self, msg: NavSatFix):
        # Always update current UTM from GPS fix
        e, n, _, _ = utm.from_latlon(msg.latitude, msg.longitude)
        self.current_e = e
        self.current_n = n

        # Initialize prev on first GPS
        if self.prev_e is None:
            self.prev_e = e
            self.prev_n = n

    def odom_callback(self, msg: Odometry):
        # Extract current yaw from odometry
        q0 = msg.pose.pose.orientation
        roll, pitch, current_yaw = euler_from_quaternion([
            q0.x, q0.y, q0.z, q0.w
        ])

        # Check for straight movement: linear forward & minimal rotation
        lin = msg.twist.twist.linear.x
        ang = msg.twist.twist.angular.z
        if (self.current_e is not None and
            abs(ang) < self.angular_threshold and
            lin > self.linear_threshold):
            dx = self.current_e - self.prev_e
            dy = self.current_n - self.prev_n
            dist = math.hypot(dx, dy)
            if dist >= self.distance_threshold:
                # True yaw from GPS delta
                true_yaw = math.atan2(dy, dx)
                # Compute new offset
                self.offset = normalize_angle(true_yaw - current_yaw)
                self.get_logger().info(
                    f'Dynamic yaw calibrate: true={true_yaw:.3f}, ' +
                    f'odom={current_yaw:.3f}, offset={self.offset:.3f}'
                )
                # Reset prev for next calibration
                self.prev_e = self.current_e
                self.prev_n = self.current_n

        # Apply offset to current yaw
        corrected_yaw = normalize_angle(current_yaw + self.offset)
        # Build corrected quaternion
        qx, qy, qz, qw = quaternion_from_euler(roll, pitch, corrected_yaw)

        # Publish fused odometry
        fused = copy.deepcopy(msg)
        fused.pose.pose.orientation.x = qx
        fused.pose.pose.orientation.y = qy
        fused.pose.pose.orientation.z = qz
        fused.pose.pose.orientation.w = qw
        self.fused_pub.publish(fused)


def main(args=None):
    rclpy.init(args=args)
    node = GPSHeadingFuser()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()