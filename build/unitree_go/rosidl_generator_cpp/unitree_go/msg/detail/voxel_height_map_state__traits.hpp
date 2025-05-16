// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/voxel_height_map_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const VoxelHeightMapState & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: stamp_cloud
  {
    out << "stamp_cloud: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp_cloud, out);
    out << ", ";
  }

  // member: stamp_odom
  {
    out << "stamp_odom: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp_odom, out);
    out << ", ";
  }

  // member: height_map_size
  {
    out << "height_map_size: ";
    rosidl_generator_traits::value_to_yaml(msg.height_map_size, out);
    out << ", ";
  }

  // member: voxel_map_size
  {
    out << "voxel_map_size: ";
    rosidl_generator_traits::value_to_yaml(msg.voxel_map_size, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VoxelHeightMapState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp, out);
    out << "\n";
  }

  // member: stamp_cloud
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp_cloud: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp_cloud, out);
    out << "\n";
  }

  // member: stamp_odom
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp_odom: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp_odom, out);
    out << "\n";
  }

  // member: height_map_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height_map_size: ";
    rosidl_generator_traits::value_to_yaml(msg.height_map_size, out);
    out << "\n";
  }

  // member: voxel_map_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "voxel_map_size: ";
    rosidl_generator_traits::value_to_yaml(msg.voxel_map_size, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VoxelHeightMapState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace unitree_go

namespace rosidl_generator_traits
{

[[deprecated("use unitree_go::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const unitree_go::msg::VoxelHeightMapState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::VoxelHeightMapState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::VoxelHeightMapState>()
{
  return "unitree_go::msg::VoxelHeightMapState";
}

template<>
inline const char * name<unitree_go::msg::VoxelHeightMapState>()
{
  return "unitree_go/msg/VoxelHeightMapState";
}

template<>
struct has_fixed_size<unitree_go::msg::VoxelHeightMapState>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_go::msg::VoxelHeightMapState>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_go::msg::VoxelHeightMapState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__TRAITS_HPP_
