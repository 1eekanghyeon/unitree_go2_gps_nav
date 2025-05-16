// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__BUILDER_HPP_
#define UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "unitree_go/msg/detail/voxel_height_map_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace unitree_go
{

namespace msg
{

namespace builder
{

class Init_VoxelHeightMapState_voxel_map_size
{
public:
  explicit Init_VoxelHeightMapState_voxel_map_size(::unitree_go::msg::VoxelHeightMapState & msg)
  : msg_(msg)
  {}
  ::unitree_go::msg::VoxelHeightMapState voxel_map_size(::unitree_go::msg::VoxelHeightMapState::_voxel_map_size_type arg)
  {
    msg_.voxel_map_size = std::move(arg);
    return std::move(msg_);
  }

private:
  ::unitree_go::msg::VoxelHeightMapState msg_;
};

class Init_VoxelHeightMapState_height_map_size
{
public:
  explicit Init_VoxelHeightMapState_height_map_size(::unitree_go::msg::VoxelHeightMapState & msg)
  : msg_(msg)
  {}
  Init_VoxelHeightMapState_voxel_map_size height_map_size(::unitree_go::msg::VoxelHeightMapState::_height_map_size_type arg)
  {
    msg_.height_map_size = std::move(arg);
    return Init_VoxelHeightMapState_voxel_map_size(msg_);
  }

private:
  ::unitree_go::msg::VoxelHeightMapState msg_;
};

class Init_VoxelHeightMapState_stamp_odom
{
public:
  explicit Init_VoxelHeightMapState_stamp_odom(::unitree_go::msg::VoxelHeightMapState & msg)
  : msg_(msg)
  {}
  Init_VoxelHeightMapState_height_map_size stamp_odom(::unitree_go::msg::VoxelHeightMapState::_stamp_odom_type arg)
  {
    msg_.stamp_odom = std::move(arg);
    return Init_VoxelHeightMapState_height_map_size(msg_);
  }

private:
  ::unitree_go::msg::VoxelHeightMapState msg_;
};

class Init_VoxelHeightMapState_stamp_cloud
{
public:
  explicit Init_VoxelHeightMapState_stamp_cloud(::unitree_go::msg::VoxelHeightMapState & msg)
  : msg_(msg)
  {}
  Init_VoxelHeightMapState_stamp_odom stamp_cloud(::unitree_go::msg::VoxelHeightMapState::_stamp_cloud_type arg)
  {
    msg_.stamp_cloud = std::move(arg);
    return Init_VoxelHeightMapState_stamp_odom(msg_);
  }

private:
  ::unitree_go::msg::VoxelHeightMapState msg_;
};

class Init_VoxelHeightMapState_stamp
{
public:
  Init_VoxelHeightMapState_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VoxelHeightMapState_stamp_cloud stamp(::unitree_go::msg::VoxelHeightMapState::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_VoxelHeightMapState_stamp_cloud(msg_);
  }

private:
  ::unitree_go::msg::VoxelHeightMapState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::unitree_go::msg::VoxelHeightMapState>()
{
  return unitree_go::msg::builder::Init_VoxelHeightMapState_stamp();
}

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__BUILDER_HPP_
