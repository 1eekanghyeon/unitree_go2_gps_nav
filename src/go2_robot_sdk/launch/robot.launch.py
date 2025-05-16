# Copyright (c) 2024, RoboVerse community
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import FrontendLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch.actions import TimerAction

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    with_rviz2 = LaunchConfiguration('rviz2', default='true')
    with_nav2 = LaunchConfiguration('nav2', default='true')
    with_slam = LaunchConfiguration('slam', default='true')
    with_foxglove = LaunchConfiguration('foxglove', default='true')
    with_joystick = LaunchConfiguration('joystick', default='true')
    with_teleop = LaunchConfiguration('teleop', default='true')

    robot_token = os.getenv('ROBOT_TOKEN', '') # how does this work for multiple robots?
    robot_ip = os.getenv('ROBOT_IP', '')
    robot_ip_lst = robot_ip.replace(" ", "").split(",")
    print("IP list:", robot_ip_lst)

    # 새로운 환경 변수 가져오기 (시리얼 번호 기반 연결 지원)
    serial_number = os.getenv('SERIAL_NUMBER', '')
    unitree_email = os.getenv('UNITREE_EMAIL', '')
    unitree_password = os.getenv('UNITREE_PASSWORD', '')

    # these are debug only
    map_name = os.getenv('MAP_NAME', '3d_map')
    save_map = os.getenv('MAP_SAVE', 'true')

    conn_type = os.getenv('CONN_TYPE', 'webrtc')

    conn_mode = "single" if len(robot_ip_lst) == 1 and conn_type != "cyclonedds" else "multi"

    if conn_mode == 'single':
        rviz_config = "single_robot_conf.rviz"
    else:
        rviz_config = "multi_robot_conf.rviz"

    if conn_type == 'cyclonedds':
        rviz_config = "cyclonedds_config.rviz"

    urdf_file_name = 'multi_go2.urdf'
    urdf = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        "urdf",
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_desc_modified_lst = []

    for i in range(len(robot_ip_lst)):
        robot_desc_modified_lst.append(robot_desc.format(robot_num=f"robot{i}"))

    urdf_launch_nodes = []

    joy_params = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config', 'joystick.yaml'
    )

    default_config_topics = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config', 'twist_mux.yaml')

    foxglove_launch = os.path.join(
        get_package_share_directory('foxglove_bridge'),
        'launch',
        'foxglove_bridge_launch.xml',
    )

    slam_toolbox_config = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config',
        'mapper_params_online_async.yaml'
    )

    nav2_config = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config',
        'nav2_params.yaml'
    )

    navsat_config = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config',
        'navsat_config.yaml'
    )

    print(f"Navsat Config Path: {navsat_config}")

    ekf_local_config = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config',
        'ekf_local.yaml'
    )

    ekf_global_config = os.path.join(
        get_package_share_directory('go2_robot_sdk'),
        'config',
        'ekf_global.yaml'
    )

    if conn_mode == 'single':

        urdf_file_name = 'go2.urdf'
        urdf = os.path.join(
            get_package_share_directory('go2_robot_sdk'),
            "urdf",
            urdf_file_name)
        with open(urdf, 'r') as infp:
            robot_desc = infp.read()

        urdf_launch_nodes.append(
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[{'use_sim_time': use_sim_time,
                             'robot_description': robot_desc}],
                arguments=[urdf]
            ),
        )
        urdf_launch_nodes.append(
            Node(
                package='pointcloud_to_laserscan',
                executable='pointcloud_to_laserscan_node',
                name='pointcloud_to_laserscan',
                remappings=[
                    ('cloud_in', 'point_cloud2'),
                    ('scan', 'scan'),
                ],
                parameters=[{
                    'target_frame': 'base_link',
                    'max_height': 0.5
                }],
                output='screen',
            ),
        )

    else:

        for i in range(len(robot_ip_lst)):
            urdf_launch_nodes.append(
                Node(
                    package='robot_state_publisher',
                    executable='robot_state_publisher',
                    name='robot_state_publisher',
                    output='screen',
                    namespace=f"robot{i}",
                    parameters=[{'use_sim_time': use_sim_time,
                                 'robot_description': robot_desc_modified_lst[i]}],
                    arguments=[urdf]
                ),
            )
            urdf_launch_nodes.append(
                Node(
                    package='pointcloud_to_laserscan',
                    executable='pointcloud_to_laserscan_node',
                    name='pointcloud_to_laserscan',
                    remappings=[
                        ('cloud_in', f'robot{i}/point_cloud2'),
                        ('scan', f'robot{i}/scan'),
                    ],
                    parameters=[{
                        'target_frame': f'robot{i}/base_link',
                        'max_height': 0.1
                    }],
                    output='screen',
                ),
            )

    return LaunchDescription([

        *urdf_launch_nodes,
        Node(
            package='go2_robot_sdk',
            executable='go2_driver_node',
            parameters=[{
                'robot_ip': robot_ip,
                'token': robot_token,
                'enable_video': True, 
                'conn_type': conn_type,
                'serial_number': serial_number,  # 추가: 시리얼 번호
                'email': unitree_email,          # 추가: 이메일
                'password': unitree_password     # 추가: 비밀번호
            }],
        ),
        Node(
            package='go2_robot_sdk',
            executable='lidar_to_pointcloud',
            parameters=[{'robot_ip_lst': robot_ip_lst, 'map_name': map_name, 'map_save': save_map}],
        ),

        # Node(
        #     package='nav2_map_server',
        #     executable='map_server',
        #     name='map_server',
        #     output='screen',
        #     parameters=[{
        #         'yaml_filename': hiwi_map,
        #         'use_sim_time': use_sim_time,
        #     }],
        # ),

        # Node(
        #     package='nav2_amcl',
        #     executable='amcl',
        #     name='amcl',
        #     output='screen',
        #     parameters=[{
        #         'use_sim_time': use_sim_time,
        #         'base_frame_id': 'base_link',
        #         'odom_frame_id': 'odom',
        #         'global_frame_id': 'map',
        #         'scan_topic': 'scan',
        #         'map_topic': '/map',
        #     }],
        # ),

        # Node(
        #     package='nav2_lifecycle_manager',
        #     executable='lifecycle_manager',
        #     name='lifecycle_manager_localization',
        #     output='screen',
        #     parameters=[{
        #         'use_sim_time': use_sim_time,
        #         'autostart': True,
        #         'node_names': ['map_server','amcl'],
        #     }],
        # ),
                
        Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            condition=IfCondition(with_rviz2),
            name='rviz2',
            arguments=['-d' + os.path.join(get_package_share_directory('go2_robot_sdk'), 'config', rviz_config)]
        ),
        Node(
            package='joy',
            executable='joy_node',
            condition=IfCondition(with_joystick),
            parameters=[joy_params]
        ),
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_node',
            condition=IfCondition(with_joystick),
            parameters=[default_config_topics],
        ),
        Node(
            package='twist_mux',
            executable='twist_mux',
            output='screen',
            condition=IfCondition(with_teleop),
            parameters=[
                {'use_sim_time': use_sim_time},
                default_config_topics
            ],
        ),

        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            output='log',
            parameters=[{
                'world_frame_id': 'map',         # <-- 가장 중요!
                'frequency': 30.0,
                'delay': 0.0011,
                'transform_timeout': 0.2,
                'magnetic_declination_radians': 0.0,
                'yaw_offset': 0.0,
                'zero_altitude': True,
                'broadcast_cartesian_transform': False,
                'publish_filtered_gps': True,
                'use_odometry_yaw': False,
                'wait_for_datum': True,        # datum 관련 로그 및 동작 확인 위해 True 유지
                'use_sim_time': False
            }],
            remappings=[
                ('gps/fix', '/fix'),
                ('imu', '/imu_converted'),
                ('odometry/filtered', '/odometry/filtered_local'),
                ('odometry/gps', '/odometry/gps')
            ],
         
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_local_node', # YAML 파일의 최상위 키와 일치시킴 (또는 원하는 이름 사용)
            output='screen',
            parameters=[ekf_local_config],
            remappings=[('odometry/filtered', 'odometry/filtered_local')], # 출력 토픽 이름 변경
        ),

        # 예시: Global EKF 노드 추가 (ekf_global.yaml 설정 필요)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_global_node', # 또는 'ekf_filter_node_map' 등
            output='screen',
            parameters=[ekf_global_config], # 예: ekf_global.yaml
            remappings=[('odometry/filtered', 'odometry/global_filtered')] # 또는 Nav2가 사용할 이름
        ),
            

    
   
       

        Node(
            package='go2_robot_sdk',                # 본인이 만든 패키지명
            executable='gps_node',               # setup.py entry_points 이름
            name='gps_tcp_ros2',
            output='screen'
        ),

        # 8) IMU Converter Node (imu_converter_node.py)
        Node(
            package='go2_robot_sdk',
            executable='imu_converter_node',
            name='imu_converter_node',
            output='screen'
        ),

        IncludeLaunchDescription(
            FrontendLaunchDescriptionSource(foxglove_launch),
            condition=IfCondition(with_foxglove),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory(
                    'slam_toolbox'), 'launch', 'online_async_launch.py')
            ]),
            condition=IfCondition(with_slam),
            launch_arguments={
                'slam_params_file': slam_toolbox_config,
                'use_sim_time': use_sim_time,
                
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory(
                    'nav2_bringup'), 'launch', 'navigation_launch.py')
            ]),
            condition=IfCondition(with_nav2),
            launch_arguments={
                'params_file': nav2_config,
                'use_sim_time': use_sim_time,
            }.items(),
        ),
    ])
