# generated from rosidl_generator_py/resource/_idl.py.em
# with input from unitree_go:msg/VoxelHeightMapState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VoxelHeightMapState(type):
    """Metaclass of message 'VoxelHeightMapState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('unitree_go')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'unitree_go.msg.VoxelHeightMapState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__voxel_height_map_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__voxel_height_map_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__voxel_height_map_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__voxel_height_map_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__voxel_height_map_state

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VoxelHeightMapState(metaclass=Metaclass_VoxelHeightMapState):
    """Message class 'VoxelHeightMapState'."""

    __slots__ = [
        '_stamp',
        '_stamp_cloud',
        '_stamp_odom',
        '_height_map_size',
        '_voxel_map_size',
    ]

    _fields_and_field_types = {
        'stamp': 'double',
        'stamp_cloud': 'double',
        'stamp_odom': 'double',
        'height_map_size': 'uint32',
        'voxel_map_size': 'uint32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stamp = kwargs.get('stamp', float())
        self.stamp_cloud = kwargs.get('stamp_cloud', float())
        self.stamp_odom = kwargs.get('stamp_odom', float())
        self.height_map_size = kwargs.get('height_map_size', int())
        self.voxel_map_size = kwargs.get('voxel_map_size', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stamp != other.stamp:
            return False
        if self.stamp_cloud != other.stamp_cloud:
            return False
        if self.stamp_odom != other.stamp_odom:
            return False
        if self.height_map_size != other.height_map_size:
            return False
        if self.voxel_map_size != other.voxel_map_size:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'stamp' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'stamp' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._stamp = value

    @builtins.property
    def stamp_cloud(self):
        """Message field 'stamp_cloud'."""
        return self._stamp_cloud

    @stamp_cloud.setter
    def stamp_cloud(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'stamp_cloud' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'stamp_cloud' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._stamp_cloud = value

    @builtins.property
    def stamp_odom(self):
        """Message field 'stamp_odom'."""
        return self._stamp_odom

    @stamp_odom.setter
    def stamp_odom(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'stamp_odom' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'stamp_odom' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._stamp_odom = value

    @builtins.property
    def height_map_size(self):
        """Message field 'height_map_size'."""
        return self._height_map_size

    @height_map_size.setter
    def height_map_size(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'height_map_size' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'height_map_size' field must be an unsigned integer in [0, 4294967295]"
        self._height_map_size = value

    @builtins.property
    def voxel_map_size(self):
        """Message field 'voxel_map_size'."""
        return self._voxel_map_size

    @voxel_map_size.setter
    def voxel_map_size(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'voxel_map_size' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'voxel_map_size' field must be an unsigned integer in [0, 4294967295]"
        self._voxel_map_size = value
