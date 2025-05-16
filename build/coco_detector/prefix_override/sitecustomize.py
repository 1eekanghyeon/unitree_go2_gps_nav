import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/hiwilab/Project/DOG/ros2_ws/install/coco_detector'
