#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import Imu
from go2_interfaces.msg import IMU as Go2IMU
from tf_transformations import euler_from_quaternion
class IMUConverter(Node):
    def __init__(self):
        super().__init__('imu_converter_node')

        self.subscription = self.create_subscription(
            Go2IMU,
            '/imu',  # 그대로 유지
            self.imu_callback,
            10
        )

        self.publisher = self.create_publisher(
            Imu,
            '/imu_converted',
            10
        )

    def imu_callback(self, msg):
        imu_msg = Imu()

        # header 직접 생성
        imu_msg.header = Header()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'base_link'

        # 데이터 변환 (float64[] → float)
        imu_msg.orientation.x = float(msg.quaternion[1])
        imu_msg.orientation.y = float(msg.quaternion[2])
        imu_msg.orientation.z = float(msg.quaternion[3])
        imu_msg.orientation.w = float(msg.quaternion[0])

        imu_msg.angular_velocity.x = float(msg.gyroscope[0])
        imu_msg.angular_velocity.y = float(msg.gyroscope[1])  
        imu_msg.angular_velocity.z = float(msg.gyroscope[2])

        imu_msg.linear_acceleration.x = float(msg.accelerometer[0])
        imu_msg.linear_acceleration.y = float(msg.accelerometer[1])
        imu_msg.linear_acceleration.z = float(msg.accelerometer[2])
        imu_msg.orientation_covariance[0] = 0.0005  # Roll 분산
        imu_msg.orientation_covariance[4] = 0.0005 # Pitch 분산
        imu_msg.orientation_covariance[8] = 0.0001  # Yaw 분산

        # angular_velocity_covariance: X, Y, Z 각속도 분산
        imu_msg.angular_velocity_covariance[0] = 0.001 # X축 각속도 분산
        imu_msg.angular_velocity_covariance[4] = 0.001 # Y축 각속도 분산
        imu_msg.angular_velocity_covariance[8] = 0.001 # Z축 각속도 분산

        # linear_acceleration_covariance: X, Y, Z 선형 가속도 분산
        imu_msg.linear_acceleration_covariance[0] = 1e-4 # X축 가속도 분산 (보통 가속도계가 자이로보다 노이즈가 큼)
        imu_msg.linear_acceleration_covariance[4] = 1e-4 # Y축 가속도 분산
        imu_msg.linear_acceleration_covariance[8] = 1e-4 # Z축 가속도 분산

        # try:
        #     roll, pitch, yaw = euler_from_quaternion([imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z, imu_msg.orientation.w])
        #     # yaw는 z축 회전각
        #     self.get_logger().info(f"[CHECK] imu_callback → yaw: {yaw:.3f} rad")  # yaw 값 로그 출력
        # except Exception as e:
        #     self.get_logger().error(f'쿼터니언 변환 실패: {e}')

      
        self.publisher.publish(imu_msg)


def main(args=None):
    rclpy.init(args=args)
    node = IMUConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
