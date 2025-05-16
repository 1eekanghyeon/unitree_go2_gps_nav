#!/usr/bin/env python3

import socket
import rclpy
import pynmea2 # NMEA 메시지 파싱 라이브러리
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus # <<< NavSatStatus 임포트 추가

HOST = '10.8.0.2'
PORT = 6000

class GpsTcpRos2(Node):
    def __init__(self):
        super().__init__('gps_tcp_ros2')

        self.get_logger().info(f'Connecting to TCP {HOST}:{PORT}')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            self.get_logger().error(f'Failed to connect: {e}')
            # 연결 실패 시 노드를 안전하게 종료하도록 rclpy.shutdown() 호출
            if rclpy.ok():
                rclpy.shutdown()
            return # __init__에서 return하여 spin으로 넘어가지 않도록 함
        self.get_logger().info('Connected. Waiting for GGA lines')

        self.buf = ''
        self.fix_pub = self.create_publisher(NavSatFix, '/fix', 10)
        self.create_timer(0.1, self.timer_callback) # 10Hz로 NMEA 데이터 처리 시도

    def timer_callback(self):
        try:
            data = self.sock.recv(1024).decode('ascii', errors='ignore')
            if not data:
                # 연결이 끊겼을 수 있음 (데이터가 없으면 루프에서 대기)
                return
            self.buf += data

            while '\n' in self.buf:
                line, self.buf = self.buf.split('\n', 1)
                line = line.strip()

                if not (line.startswith('$GPGGA') or line.startswith('$GNGGA')):
                    continue

                try:
                    nmea_msg = pynmea2.parse(line)
                    if not isinstance(nmea_msg, pynmea2.types.talker.GGA):
                        continue
                except pynmea2.ParseError as e:
                    self.get_logger().warn(f'Failed to parse NMEA line: "{line}" - Error: {e}')
                    continue

                fix = NavSatFix()
                fix.header.stamp = self.get_clock().now().to_msg()
                # frame_id: GPS 안테나의 TF 프레임 이름 사용 권장 (예: 'gps_link')
                # 현재는 이전 코드대로 'base_link' 유지
                fix.header.frame_id = 'base_link' 

                fix.latitude = nmea_msg.latitude
                fix.longitude = nmea_msg.longitude
                fix.altitude = nmea_msg.altitude

                # GPS 수신 상태 (NavSatStatus)
                qual = 0
                if hasattr(nmea_msg, 'gps_qual') and nmea_msg.gps_qual is not None:
                    try:
                        qual = int(nmea_msg.gps_qual)
                    except ValueError:
                        self.get_logger().warn(f"Could not parse gps_qual: {nmea_msg.gps_qual}")
                        qual = 0 # 파싱 실패 시 NO_FIX로 처리

                # NavSatStatus 상수 사용 (NavSatFix.STATUS_ 대신 NavSatStatus.STATUS_ 사용)
                if qual == 0: # Fix not available or invalid
                    fix.status.status = NavSatStatus.STATUS_NO_FIX
                elif qual == 1: # GPS SPS Mode, fix valid
                    fix.status.status = NavSatStatus.STATUS_FIX
                elif qual == 2: # Differential GPS, SPS Mode, fix valid
                    fix.status.status = NavSatStatus.STATUS_SBAS_FIX
                elif qual == 4: # Real Time Kinematic, fixed integers (RTK Fixed)
                    fix.status.status = NavSatStatus.STATUS_GBAS_FIX # <<< 수정됨
                elif qual == 5: # Real Time Kinematic, float integers (RTK Float)
                    fix.status.status = NavSatStatus.STATUS_SBAS_FIX # <<< RTK Float은 SBAS_FIX로 매핑 (Fixed보다 낮음)
                else: # Estimated, Manual, Simulation, PPS (qual 3) etc.
                    fix.status.status = NavSatStatus.STATUS_NO_FIX # 기타 상태는 NO_FIX로 간주
                
                fix.status.service = NavSatStatus.SERVICE_GPS

                # 위치 공분산 (Position Covariance)
                if fix.status.status >= NavSatStatus.STATUS_FIX: # 유효한 Fix일 때만 공분산 설정
                    # RTK GPS는 매우 정밀합니다. (표준편차)^2 = 분산.
                    # 예: 수평(East, North) 표준편차 2cm (0.02m), 수직(Altitude) 표준편차 4cm (0.04m) 가정
                    # 실제 사용하시는 RTK GPS 스펙에 맞춰 이 값을 조정해야 합니다.
                    horizontal_accuracy_std_dev = 0.02  # 2cm
                    vertical_accuracy_std_dev = 0.04    # 4cm
                    
                    fix.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN
                    
                    # Covariance matrix (9 elements: [xx, xy, xz, yx, yy, yz, zx, zy, zz])
                    # 대각선 요소만 설정 (x, y, z 순서는 ENU 기준 분산으로 가정)
                    fix.position_covariance[0] = horizontal_accuracy_std_dev**2  # Easting^2 (m^2)
                    fix.position_covariance[4] = horizontal_accuracy_std_dev**2  # Northing^2 (m^2)
                    fix.position_covariance[8] = vertical_accuracy_std_dev**2    # Altitude^2 (m^2)
                else: 
                    fix.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN
                    # NO_FIX 상태일 때는 공분산이 0으로 채워지거나 매우 큰 값으로 설정될 수 있음
                    # NavSatFix 메시지 초기화 시 기본적으로 0으로 채워짐

                self.fix_pub.publish(fix)

                # 로그 출력용 상태 문자열 (pynmea2.types.talker.GGA.GPS_QUALITY_INDICATORS 참고)
                # 사용자님의 기존 로그 매핑이 pynmea2와 약간 달라서 pynmea2 기준으로 수정합니다.
                pynmea_qual_str = {
                    0: "No fix",
                    1: "GPS fix (SPS)",
                    2: "DGPS fix",
                    3: "PPS fix",
                    4: "Real Time Kinematic (Fixed)", # RTK Fixed
                    5: "Float RTK",                 # RTK Float
                    6: "Estimated (dead reckoning)",
                    7: "Manual input mode",
                    8: "Simulation mode"
                }.get(qual, f"OTHER QUAL({qual})")
                self.get_logger().info(f'GGA Sent: qual={qual} ({pynmea_qual_str}), NavSatFix_status={fix.status.status}, Lat={fix.latitude:.7f}, Lon={fix.longitude:.7f}')

        except UnicodeDecodeError:
            self.get_logger().warn(f'UnicodeDecodeError while processing NMEA data. Buffer might be corrupted.')
            # 버퍼에서 다음 라인 찾기 시도 또는 부분 초기화
            if '\n' in self.buf:
                 _, self.buf = self.buf.split('\n', 1)
            else: # 문제가 될 수 있는 부분 제거
                 self.buf = self.buf[-100:] # 최근 100자만 남기거나 비우기
        except ConnectionResetError:
            self.get_logger().error(f'Connection reset by peer. Shutting down.')
            if rclpy.ok(): rclpy.shutdown()
        except BrokenPipeError:
            self.get_logger().error(f'Broken pipe. Connection lost. Shutting down.')
            if rclpy.ok(): rclpy.shutdown()
        except Exception as e:
            self.get_logger().error(f'TCP recv/parse error in timer_callback: {e}')
            # 심각한 오류 시 종료 고려
            # if rclpy.ok(): rclpy.shutdown()

def main():
    rclpy.init()
    node = GpsTcpRos2()
    # 노드 초기화(특히 소켓 연결) 실패 시 node.sock이 없을 수 있음
    if not hasattr(node, 'sock') or node.sock is None:
        if rclpy.ok() and node.is_valid(): # 노드가 생성되었지만 연결 실패한 경우
            node.destroy_node()
        if rclpy.ok(): # rclpy가 아직 실행 중이면 종료
            rclpy.try_shutdown()
        return # spin 하지 않고 종료

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down.')
    except Exception as e:
        node.get_logger().error(f'Unhandled exception in spin: {e}')
    finally:
        if hasattr(node, 'sock') and node.sock:
            try:
                node.sock.close()
                node.get_logger().info('Socket closed.')
            except Exception as e:
                node.get_logger().error(f'Error closing socket: {e}')
        if rclpy.ok():
            if node.is_valid():
                 node.destroy_node()
            rclpy.try_shutdown()
        node.get_logger().info('GPS node shutdown complete.')

if __name__ == '__main__':
    main()