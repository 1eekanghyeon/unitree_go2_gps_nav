# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import NavSatFix, NavSatStatus
# from robot_localization.srv import SetDatum
# from geographic_msgs.msg import GeoPose, GeoPoint
# # tf_transformations 라이브러리는 ROS 2 기본 설치에 포함되지 않을 수 있습니다.
# # 만약 없다면, 간단한 쿼터니언 계산으로 대체하거나 설치해야 합니다.
# # 여기서는 Yaw=0 (동쪽)이므로 쿼터니언은 (x=0, y=0, z=0, w=1)로 간단합니다.

# class AutoDatumSetter(Node):
#     def __init__(self):
#         super().__init__('auto_datum_setter_node') # 노드 이름 명시적 변경

#         self.datum_set_successfully = False # datum 설정 성공 여부 플래그
#         self.rtk_fix_stability_counter = 0
#         # RTK Fixed 상태가 몇 번 연속으로 들어와야 datum 설정을 시도할지 결정
#         self.required_consecutive_rtk_fixes = self.declare_parameter(
#             'required_consecutive_rtk_fixes', 5).get_parameter_value().integer_value
        
#         # "항상 동쪽을 보고 시작한다"는 가정 하에 초기 Yaw 값 (ENU 기준, 동쪽=0)
#         self.initial_enu_yaw = self.declare_parameter(
#             'initial_enu_yaw_radians', 0.0).get_parameter_value().double_value

#         self.get_logger().info(
#             f'AutoDatumSetter node started. Waiting for {self.required_consecutive_rtk_fixes} '
#             f'consecutive RTK Fixed GPS signals to set datum...')
#         self.get_logger().info(f'Assumed initial ENU Yaw (0=East): {self.initial_enu_yaw} radians')

#         self.subscription = self.create_subscription(
#             NavSatFix,
#             '/fix',  # gps_node.py가 발행하는 토픽
#             self.fix_callback,
#             10) # QoS 설정은 실제 환경에 맞게 조정 가능

#         self.datum_service_client = self.create_client(SetDatum, '/datum')
#         while not self.datum_service_client.wait_for_service(timeout_sec=1.0):
#             self.get_logger().warn('/datum service not available, waiting...')

#     def fix_callback(self, msg: NavSatFix):
#         if self.datum_set_successfully:
#             # 이미 datum이 성공적으로 설정되었다면 더 이상 아무 작업도 하지 않음
#             # 필요하다면 여기서 구독을 해제하거나 노드를 종료할 수도 있습니다.
#             # self.destroy_subscription(self.subscription)
#             # self.get_logger().info('Datum already set successfully. Stopping GPS fix listener.')
#             return

#         # gps_node.py에서 qual=4 (RTK Fixed)를 NavSatStatus.STATUS_GBAS_FIX로 매핑했으므로 이를 확인
#         if msg.status.status == NavSatStatus.STATUS_GBAS_FIX:
#             self.rtk_fix_stability_counter += 1
#             self.get_logger().info(
#                 f'RTK Fixed signal received. Stability count: '
#                 f'{self.rtk_fix_stability_counter}/{self.required_consecutive_rtk_fixes}')

#             if self.rtk_fix_stability_counter >= self.required_consecutive_rtk_fixes:
#                 self.get_logger().info(
#                     f'Stable RTK Fixed signal achieved. Attempting to set datum using: '
#                     f'Lat={msg.latitude:.7f}, Lon={msg.longitude:.7f}, Alt={msg.altitude:.3f}')

#                 datum_request = SetDatum.Request()
#                 datum_request.geo_pose.position.latitude = msg.latitude
#                 datum_request.geo_pose.position.longitude = msg.longitude
#                 datum_request.geo_pose.position.altitude = msg.altitude # 고도값 포함

#                 # 초기 방위각(Yaw)을 쿼터니언으로 변환 (Roll=0, Pitch=0 가정)
#                 # ENU 좌표계에서 Yaw=0은 동쪽을 의미
#                 # Yaw (z-axis rotation), Pitch (y-axis rotation), Roll (x-axis rotation)
#                 # 간단한 쿼터니언: x=0, y=0, z=sin(yaw/2), w=cos(yaw/2)
#                 yaw = self.initial_enu_yaw # 사용자가 항상 동쪽을 본다고 가정하면 0.0
#                 half_yaw = yaw / 2.0
#                 # math.sin, math.cos를 사용하려면 import math 필요
#                 # 여기서는 yaw=0 가정이므로 직접 값 입력
#                 if yaw == 0.0:
#                     datum_request.geo_pose.orientation.x = 0.0
#                     datum_request.geo_pose.orientation.y = 0.0
#                     datum_request.geo_pose.orientation.z = 0.0
#                     datum_request.geo_pose.orientation.w = 1.0
#                 else:
#                     # 만약 다른 방위각을 사용한다면 tf_transformations 또는 numpy로 계산
#                     # 예: q = quaternion_from_euler(0.0, 0.0, yaw)
#                     # datum_request.geo_pose.orientation.x = q[0] ... 등
#                     # 이 예제에서는 yaw=0만 간단히 처리
#                     self.get_logger().warn(
#                         f"Initial ENU Yaw is non-zero ({yaw} rad), but this script only sets "
#                         "quaternion for yaw=0. Please implement full quaternion conversion if needed.")
#                     # 일단 yaw=0으로 진행
#                     datum_request.geo_pose.orientation.x = 0.0
#                     datum_request.geo_pose.orientation.y = 0.0
#                     datum_request.geo_pose.orientation.z = 0.0
#                     datum_request.geo_pose.orientation.w = 1.0


#                 # 비동기 서비스 호출
#                 future = self.datum_service_client.call_async(datum_request)
#                 future.add_done_callback(self.datum_response_callback)
                
#                 # 서비스 호출 후에는 더 이상 이 콜백에서 datum 설정을 시도하지 않도록 플래그 변경
#                 # 응답을 기다리지 않고 바로 성공으로 간주 (실제로는 응답 콜백에서 최종 처리)
#                 self.datum_set_successfully = True 
#                 self.get_logger().info("SetDatum service request sent.")
#                 # 성공적으로 요청을 보냈으므로, GPS 메시지 구독 중단 (선택 사항)
#                 if self.subscription:
#                     self.destroy_subscription(self.subscription)
#                     self.subscription = None 
#                     self.get_logger().info("GPS fix subscription cancelled after sending datum request.")

#         else:
#             # RTK Fixed 상태가 아니면 카운터 리셋
#             if self.rtk_fix_stability_counter > 0:
#                 self.get_logger().info(
#                     f'RTK Fixed signal lost or status changed to {msg.status.status}. '
#                     'Resetting stability counter.')
#             self.rtk_fix_stability_counter = 0
#             # 현재 GPS 상태 로깅 (디버깅에 유용)
#             # self.get_logger().debug(f'Waiting for RTK Fixed. Current NavSatStatus: {msg.status.status}')

#     def datum_response_callback(self, future):
#         try:
#             response = future.result()
#             self.get_logger().info(f'SetDatum service call successful: {response}')
#             # 여기서 datum_set_successfully = True 로 최종 확정하는 것이 더 정확할 수 있으나,
#             # 요청을 보낸 시점에서 더 이상 시도하지 않도록 하는 것도 방법입니다.
#         except Exception as e:
#             self.get_logger().error(f'SetDatum service call failed: {e}')
#             # 서비스 호출 실패 시, 다시 시도할 수 있도록 플래그를 리셋할 수 있습니다.
#             # self.datum_set_successfully = False 
#             # self.rtk_fix_stability_counter = 0 # 다시 안정적인 fix를 기다리도록
#             # if self.subscription is None: # 만약 구독이 해제되었다면 다시 생성
#             #     self.subscription = self.create_subscription(...)

# def main(args=None):
#     rclpy.init(args=args)
#     auto_datum_setter_node = AutoDatumSetter()
#     try:
#         rclpy.spin(auto_datum_setter_node)
#     except KeyboardInterrupt:
#         auto_datum_setter_node.get_logger().info('Keyboard interrupt, shutting down.')
#     finally:
#         # 노드가 rclpy.spin()에서 빠져나오면 (예: KeyboardInterrupt 또는 다른 이유로 shutdown)
#         # 노드를 명시적으로 파괴하고 rclpy를 종료합니다.
#         if rclpy.ok(): # rclpy 컨텍스트가 여전히 유효한지 확인
#             if auto_datum_setter_node.is_valid: # 노드가 여전히 유효한지 확인 (이미 파괴되지 않았다면)
#                  auto_datum_setter_node.destroy_node()
#             rclpy.shutdown()
#     auto_datum_setter_node.get_logger().info('AutoDatumSetter node shutdown complete.')

# if __name__ == '__main__':
#     main()