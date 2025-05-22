#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from tf_transformations import euler_from_quaternion, quaternion_from_euler
import utm
import math
import copy

class GPSHeadingFuser(Node):
    def __init__(self):
        super().__init__('gps_heading_fuser')
        self.prev_e = None
        self.prev_n = None
        self.yaw = 0.0
        self.distance_threshold = 1.0  # 1m 이상 이동 시 보정

        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.create_subscription(NavSatFix, '/fix', self.gps_callback, 10)
        self.fused_pub = self.create_publisher(Odometry, '/odom_fused', 10)

    def gps_callback(self, msg: NavSatFix):
        e, n, _, _ = utm.from_latlon(msg.latitude, msg.longitude)
        if self.prev_e is not None:
            dx = e - self.prev_e
            dy = n - self.prev_n
            dist = math.hypot(dx, dy)
            if dist >= self.distance_threshold:
                self.yaw = math.atan2(dy, dx)
        self.prev_e, self.prev_n = e, n

    def odom_callback(self, msg: Odometry):
        q0 = msg.pose.pose.orientation
        roll, pitch, _ = euler_from_quaternion(
            [q0.x, q0.y, q0.z, q0.w]
        )
        qx, qy, qz, qw = quaternion_from_euler(roll, pitch, self.yaw)

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
