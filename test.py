# gps_delay_checker.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import numpy as np
import time

class GpsDelayChecker(Node):
    def __init__(self):
        super().__init__('gps_delay_checker')
        self.subscription = self.create_subscription(NavSatFix, '/fix', self.listener_callback, 10)
        self.delays = []
        self.start_time = time.time()
        self.get_logger().info("GPS Delay Checker- NMEA 데이터 수신 대기 중...")


    def listener_callback(self, msg):
        # Ensure that the system clock is reasonably synchronized,
        # or this measurement might not be accurate.
        # Also, consider initial large delays if messages were buffered.
        if len(self.delays) > 1000: # Keep a rolling window of delays or stop after enough samples
            self.delays.pop(0)

        current_ros_time_sec = self.get_clock().now().nanoseconds / 1e9
        gps_header_time_sec = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9

        # Check if header timestamp is unrealistically in the future or too far in the past
        if gps_header_time_sec > current_ros_time_sec + 1.0: # More than 1 sec in future
            self.get_logger().warn(f"GPS header timestamp ({gps_header_time_sec:.4f}) is in the future compared to ROS time ({current_ros_time_sec:.4f}). Skipping.")
            return
        if current_ros_time_sec > gps_header_time_sec + 5.0: # More than 5 secs old
             self.get_logger().warn(f"GPS header timestamp ({gps_header_time_sec:.4f}) is too old compared to ROS time ({current_ros_time_sec:.4f}). Skipping.")
             return


        delay = current_ros_time_sec - gps_header_time_sec

        if delay >= 0: # Only consider non-negative delays
            self.delays.append(delay)

        if len(self.delays) > 0 and len(self.delays) % 50 == 0 : # Log every 50 samples
            avg_delay = np.mean(self.delays)
            std_dev_delay = np.std(self.delays)
            self.get_logger().info(f'Collected {len(self.delays)} samples. Average GPS delay: {avg_delay:.4f} s, StdDev: {std_dev_delay:.4f} s')


def main(args=None):
    rclpy.init(args=args)
    node = GpsDelayChecker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        avg_delay_final = np.mean(node.delays) if node.delays else 0
        std_dev_final = np.std(node.delays) if node.delays else 0
        node.get_logger().info(f'Final {len(node.delays)} samples - Average GPS delay: {avg_delay_final:.4f} s, StdDev: {std_dev_final:.4f} s')
        node.get_logger().info("GPS Delay Checker 종료.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
