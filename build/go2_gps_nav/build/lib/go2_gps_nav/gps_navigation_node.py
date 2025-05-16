#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from go2_interfaces.msg import IMU as Go2IMU
from geometry_msgs.msg import Twist
import math
import utm
import numpy as np
from collections import deque

class OutdoorNavigationNode(Node):
    def __init__(self):
        super().__init__('outdoor_navigation_node_gps_imu_fusion')

        # Parameters (사용자 로그 기반 angular_speed 조정)
        self.declare_parameter('gps_filter_window', 10)
        self.declare_parameter('min_init_gps_samples', 10)
        self.declare_parameter('min_init_displacement', 0.75) # 초기 Heading 설정을 위한 최소 이동 거리 (m)
        self.declare_parameter('init_movement_timeout', 30.0)
        self.declare_parameter('init_forward_speed', 0.1) # 0이면 수동 이동

        self.declare_parameter('displacement_threshold_recal', 1.0) # 오프셋 재보정을 위한 GPS 이동 거리 (m)
        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('angular_speed', 0.5) # 사용자 로그 반영
        self.declare_parameter('goal_threshold', 1.0)
        self.declare_parameter('yaw_threshold', 0.08)
        self.declare_parameter('fine_tune_angular_scale', 0.3)
        self.declare_parameter('offset_recal_ema_alpha', 0.3) # 오프셋 재보정 시 EMA 가중치

        self.gps_filter_window = self.get_parameter('gps_filter_window').value
        self.min_init_gps_samples = max(self.get_parameter('min_init_gps_samples').value, self.gps_filter_window)
        self.min_init_displacement = self.get_parameter('min_init_displacement').value
        self.init_movement_timeout = self.get_parameter('init_movement_timeout').value
        self.init_forward_speed = self.get_parameter('init_forward_speed').value

        self.displacement_threshold_recal = self.get_parameter('displacement_threshold_recal').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.goal_threshold = self.get_parameter('goal_threshold').value
        self.yaw_threshold = self.get_parameter('yaw_threshold').value
        self.fine_tune_angular_scale = self.get_parameter('fine_tune_angular_scale').value
        self.offset_recal_ema_alpha = self.get_parameter('offset_recal_ema_alpha').value


        # State variables
        self.filtered_utm = None
        self.prev_utm_for_offset_recal = None # 오프셋 재보정을 위한 이전 UTM
        self.goal_utm = None
        self.raw_imu_rpy = None # IMU RPY (roll, pitch, imu_yaw)

        self.current_enu_yaw = None # 최종 추정된 ENU Yaw (IMU + GPS 오프셋)
        self.enu_heading_to_imu_rpy2_offset = None # GPS Heading과 IMU rpy[2] 간의 오프셋
        self.goal_reached = True

        self.gps_buffer = deque(maxlen=self.gps_filter_window)

        self.STATE_INIT_GPS_STABILIZE = "INIT_GPS_STABILIZE"
        self.STATE_INIT_SET_HEADING_AND_OFFSET = "INIT_SET_HEADING_AND_OFFSET"
        self.STATE_OPERATIONAL = "OPERATIONAL"
        self.current_state = self.STATE_INIT_GPS_STABILIZE

        self.init_gps_samples_collected = 0
        self.init_start_utm_for_heading = None
        self.init_movement_start_time = None
        self.initial_imu_rpy2_at_heading_set = None


        self.gps_subscription = self.create_subscription(NavSatFix, '/fix', self.gps_callback, 10)
        self.imu_subscription = self.create_subscription(Go2IMU, '/imu', self.imu_callback, 10)
        self.goal_subscription = self.create_subscription(NavSatFix, '/goal', self.goal_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info(f"'{self.get_name()}' initialized.")
        self.log_state_transition()

    def log_state_transition(self):
        self.get_logger().info(f"Current State: {self.current_state}")
        if self.current_state == self.STATE_INIT_GPS_STABILIZE:
            self.get_logger().info(f"Waiting for {self.min_init_gps_samples} GPS samples to stabilize filter...")
        elif self.current_state == self.STATE_INIT_SET_HEADING_AND_OFFSET:
            self.get_logger().info(f"GPS stabilized. Move robot forward > {self.min_init_displacement:.2f}m to set initial ENU heading and IMU offset.")
            if self.init_forward_speed > 0:
                self.get_logger().info(f"Attempting auto-forward at {self.init_forward_speed:.2f} m/s.")
            self.init_movement_start_time = self.get_clock().now()

    def gps_callback(self, msg: NavSatFix):
        try:
            easting, northing, _, _ = utm.from_latlon(msg.latitude, msg.longitude)
            current_raw_utm = (easting, northing)

            if self.current_state == self.STATE_INIT_GPS_STABILIZE:
                self.gps_buffer.append(current_raw_utm)
                self.init_gps_samples_collected += 1
                self.get_logger().info(f"GPS Samples: {self.init_gps_samples_collected}/{self.min_init_gps_samples}", throttle_duration_sec=1.0)
                if self.init_gps_samples_collected >= self.min_init_gps_samples:
                    if len(self.gps_buffer) > 0:
                        avg_easting = sum(p[0] for p in self.gps_buffer) / len(self.gps_buffer)
                        avg_northing = sum(p[1] for p in self.gps_buffer) / len(self.gps_buffer)
                        self.filtered_utm = (avg_easting, avg_northing)
                        self.init_start_utm_for_heading = self.filtered_utm
                        self.prev_utm_for_offset_recal = self.filtered_utm # 오프셋 재보정 기준점도 초기화
                        self.current_state = self.STATE_INIT_SET_HEADING_AND_OFFSET
                        self.log_state_transition()
                    else:
                        self.get_logger().warn("GPS buffer empty after collecting samples.")
            else: # STATE_INIT_SET_HEADING_AND_OFFSET or STATE_OPERATIONAL
                self.gps_buffer.append(current_raw_utm)
                if len(self.gps_buffer) > 0:
                    avg_easting = sum(p[0] for p in self.gps_buffer) / len(self.gps_buffer)
                    avg_northing = sum(p[1] for p in self.gps_buffer) / len(self.gps_buffer)
                    self.filtered_utm = (avg_easting, avg_northing)
        except Exception as e:
            self.get_logger().error(f'Error processing GPS data: {e}')
            self.filtered_utm = None

    def imu_callback(self, msg: Go2IMU):
        try:
            if hasattr(msg, 'rpy') and len(msg.rpy) >= 3:
                self.raw_imu_rpy = msg.rpy # (roll, pitch, imu_rpy2_value)
                # 실시간 ENU Yaw 업데이트 (오프셋이 설정된 경우)
                if self.enu_heading_to_imu_rpy2_offset is not None and self.current_state == self.STATE_OPERATIONAL:
                    # current_imu_rpy2 = self.raw_imu_rpy[2]
                    # self.current_enu_yaw = self.normalize_angle(current_imu_rpy2 - self.enu_heading_to_imu_rpy2_offset)
                    # 주의: IMU rpy[2]의 부호 및 기준에 따라 offset 더하기/빼기 결정.
                    # 일반적 가정: ENU = IMU_abs - OFFSET_abs 또는 ENU = IMU_abs + OFFSET_rel
                    # 여기서 offset은 (IMU값 - ENU값) 이므로, ENU = IMU - offset.
                    self.current_enu_yaw = self.normalize_angle(self.raw_imu_rpy[2] - self.enu_heading_to_imu_rpy2_offset)

            else:
                self.raw_imu_rpy = None
        except Exception as e:
            self.get_logger().warn(f'Error processing IMU data: {e}', throttle_duration_sec=5.0)
            self.raw_imu_rpy = None

    def goal_callback(self, msg: NavSatFix):
        if self.current_state != self.STATE_OPERATIONAL:
            self.get_logger().warn(f'System not in OPERATIONAL state ({self.current_state}). Goal rejected.')
            return
        try:
            easting, northing, _, _ = utm.from_latlon(msg.latitude, msg.longitude)
            self.goal_utm = (easting, northing)
            self.goal_reached = False
            if self.filtered_utm:
                dist = math.hypot(self.goal_utm[0] - self.filtered_utm[0], self.goal_utm[1] - self.filtered_utm[1])
                self.get_logger().info(f'New goal: UTM {self.goal_utm}. Dist: {dist:.2f}m')
            else:
                self.get_logger().info(f'New goal: UTM {self.goal_utm}. Current location unknown.')
        except Exception as e:
            self.get_logger().error(f'Error processing goal data: {e}')
            self.goal_utm = None

    def calculate_enu_heading(self, current_utm, prev_utm):
        if current_utm is None or prev_utm is None: return None
        dx = current_utm[0] - prev_utm[0]
        dy = current_utm[1] - prev_utm[1]
        if math.hypot(dx, dy) < 0.01: return None
        return math.atan2(dy, dx)

    def normalize_angle(self, angle):
        if angle is None: return None
        while angle > math.pi: angle -= 2.0 * math.pi
        while angle < -math.pi: angle += 2.0 * math.pi
        return angle

    def control_loop(self):
        cmd_vel = Twist()

        if self.current_state == self.STATE_INIT_GPS_STABILIZE:
            self.cmd_vel_publisher.publish(cmd_vel)
            return

        if self.current_state == self.STATE_INIT_SET_HEADING_AND_OFFSET:
            if self.filtered_utm and self.init_start_utm_for_heading and self.raw_imu_rpy is not None:
                displacement = math.hypot(self.filtered_utm[0] - self.init_start_utm_for_heading[0],
                                          self.filtered_utm[1] - self.init_start_utm_for_heading[1])
                self.get_logger().info(f"Initial setup: Moved {displacement:.2f}/{self.min_init_displacement:.2f}m. Waiting for IMU.", throttle_duration_sec=1.0)

                if displacement >= self.min_init_displacement:
                    initial_gps_enu_heading = self.calculate_enu_heading(self.filtered_utm, self.init_start_utm_for_heading)
                    if initial_gps_enu_heading is not None:
                        self.current_enu_yaw = self.normalize_angle(initial_gps_enu_heading) # 현재 Yaw를 GPS heading으로 우선 설정
                        self.initial_imu_rpy2_at_heading_set = self.raw_imu_rpy[2]
                        # 오프셋 계산: offset = IMU_yaw - GPS_ENU_yaw.
                        # 나중에 ENU_yaw = IMU_yaw - offset 으로 사용.
                        self.enu_heading_to_imu_rpy2_offset = self.normalize_angle(
                            self.initial_imu_rpy2_at_heading_set - self.current_enu_yaw
                        )
                        self.prev_utm_for_offset_recal = self.filtered_utm # 다음 오프셋 재보정 기준점 설정
                        self.current_state = self.STATE_OPERATIONAL
                        self.goal_reached = True # 운영 상태 시작 시 정지 유지
                        self.log_state_transition()
                        self.get_logger().info(f"Initial ENU Heading by GPS: {self.current_enu_yaw:.3f} rad.")
                        self.get_logger().info(f"Initial IMU rpy[2]: {self.initial_imu_rpy2_at_heading_set:.3f} rad.")
                        self.get_logger().info(f"Calculated (IMU_rpy[2] - ENU_Yaw) Offset: {self.enu_heading_to_imu_rpy2_offset:.3f} rad.")
                    else:
                        self.get_logger().warn("Displacement met, but failed to calc initial GPS heading. Resetting start UTM.")
                        self.init_start_utm_for_heading = self.filtered_utm
                elif self.init_forward_speed > 0:
                    cmd_vel.linear.x = self.init_forward_speed
            else:
                if self.raw_imu_rpy is None:
                    self.get_logger().warn("Waiting for IMU data for initial setup.", throttle_duration_sec=1.0)
                else:
                    self.get_logger().warn("Waiting for UTM data for initial setup.", throttle_duration_sec=1.0)


            if self.init_movement_start_time and \
               (self.get_clock().now() - self.init_movement_start_time).nanoseconds / 1e9 > self.init_movement_timeout:
                self.get_logger().error(f"Initial heading/offset setup FAILED: Timeout ({self.init_movement_timeout}s).")
                rclpy.shutdown()
                return
            self.cmd_vel_publisher.publish(cmd_vel)
            return

        # --- STATE_OPERATIONAL ---
        if self.filtered_utm is None or self.current_enu_yaw is None or self.raw_imu_rpy is None or self.enu_heading_to_imu_rpy2_offset is None:
            self.get_logger().warn('OPERATIONAL: Waiting for valid UTM, IMU, ENU Yaw, or Offset...', throttle_duration_sec=1.0)
            self.cmd_vel_publisher.publish(cmd_vel)
            return

        # 오프셋 주기적 재보정 (GPS 이동 기반)
        if self.prev_utm_for_offset_recal and self.filtered_utm:
            displacement_for_recal = math.hypot(self.filtered_utm[0] - self.prev_utm_for_offset_recal[0],
                                                 self.filtered_utm[1] - self.prev_utm_for_offset_recal[1])
            if displacement_for_recal >= self.displacement_threshold_recal:
                current_gps_enu_heading = self.calculate_enu_heading(self.filtered_utm, self.prev_utm_for_offset_recal)
                if current_gps_enu_heading is not None and self.raw_imu_rpy is not None:
                    # 새로운 오프셋 계산
                    new_offset = self.normalize_angle(self.raw_imu_rpy[2] - current_gps_enu_heading)
                    # EMA 필터로 오프셋 부드럽게 업데이트
                    self.enu_heading_to_imu_rpy2_offset = self.normalize_angle(
                        self.offset_recal_ema_alpha * new_offset +
                        (1 - self.offset_recal_ema_alpha) * self.enu_heading_to_imu_rpy2_offset
                    )
                    self.get_logger().info(f"IMU Offset RECALIBRATED to {self.enu_heading_to_imu_rpy2_offset:.3f} rad based on GPS heading {current_gps_enu_heading:.3f} (disp: {displacement_for_recal:.2f}m)")
                    self.prev_utm_for_offset_recal = self.filtered_utm # 기준점 업데이트
                    # 오프셋 재보정 후 current_enu_yaw도 GPS heading으로 한번 동기화
                    self.current_enu_yaw = self.normalize_angle(current_gps_enu_heading)


        # 실시간 current_enu_yaw는 imu_callback에서 IMU값과 offset을 이용해 계속 업데이트됨.
        # 여기서는 목표 처리 및 제어 명령만.

        if self.goal_utm is None or self.goal_reached:
            self.cmd_vel_publisher.publish(cmd_vel)
            return

        distance_to_goal = math.hypot(self.goal_utm[0] - self.filtered_utm[0], self.goal_utm[1] - self.filtered_utm[1])
        if distance_to_goal < self.goal_threshold:
            self.get_logger().info(f'Goal reached! Distance: {distance_to_goal:.2f}m')
            self.goal_reached = True
            self.cmd_vel_publisher.publish(cmd_vel)
            return

        target_bearing = self.calculate_enu_heading(self.goal_utm, self.filtered_utm)
        if target_bearing is None:
             self.get_logger().warn("Target bearing calculation failed (current and goal UTM too close). Stopping.")
             self.goal_reached = True
             self.cmd_vel_publisher.publish(cmd_vel)
             return
        target_bearing = self.normalize_angle(target_bearing)
        
        yaw_error = self.normalize_angle(target_bearing - self.current_enu_yaw)

        if abs(yaw_error) > self.yaw_threshold:
            cmd_vel.angular.z = self.angular_speed * np.sign(yaw_error)
            cmd_vel.linear.x = 0.0
        else:
            cmd_vel.linear.x = self.linear_speed
            cmd_vel.angular.z = self.fine_tune_angular_scale * self.angular_speed * np.sign(yaw_error)

        self.cmd_vel_publisher.publish(cmd_vel)

        self.get_logger().info(
            f"Dist: {distance_to_goal:.2f}m | "
            f"CurENUYaw(IMU+Off): {self.current_enu_yaw:.2f} ({math.degrees(self.current_enu_yaw):.1f}°) | "
            f"IMU_rpy[2]: {self.raw_imu_rpy[2]:.2f} | Offset: {self.enu_heading_to_imu_rpy2_offset:.2f} | "
            f"TgtBearing: {target_bearing:.2f} ({math.degrees(target_bearing):.1f}°) | "
            f"YawErr: {yaw_error:.2f} ({math.degrees(yaw_error):.1f}°) | "
            f"CmdVel: L={cmd_vel.linear.x:.2f}, A={cmd_vel.angular.z:.2f}",
            throttle_duration_sec=0.5
        )

def main(args=None):
    rclpy.init(args=args)
    node = OutdoorNavigationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt received.')
    except Exception as e:
        node.get_logger().error(f"Unhandled exception in spin: {e}")
    finally:
        node.get_logger().info('Shutting down. Sending zero velocity.')
        stop_cmd = Twist()
        if hasattr(node, 'cmd_vel_publisher') and node.cmd_vel_publisher.is_activated:
             node.cmd_vel_publisher.publish(stop_cmd)
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()
        node.get_logger().info('Shutdown complete.')

if __name__ == '__main__':
    main()