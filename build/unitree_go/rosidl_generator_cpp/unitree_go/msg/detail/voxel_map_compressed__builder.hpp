// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from unitree_go:msg/VoxelMapCompressed.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__BUILDER_HPP_
#define UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "unitree_go/msg/detail/voxel_map_compressed__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace unitree_go
{

namespace msg
{

namespace builder
{

class Init_VoxelMapCompressed_data
{
public:
  explicit Init_VoxelMapCompressed_data(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  ::unitree_go::msg::VoxelMapCompressed data(::unitree_go::msg::VoxelMapCompressed::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_src_size
{
public:
  explicit Init_VoxelMapCompressed_src_size(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  Init_VoxelMapCompressed_data src_size(::unitree_go::msg::VoxelMapCompressed::_src_size_type arg)
  {
    msg_.src_size = std::move(arg);
    return Init_VoxelMapCompressed_data(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_width
{
public:
  explicit Init_VoxelMapCompressed_width(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  Init_VoxelMapCompressed_src_size width(::unitree_go::msg::VoxelMapCompressed::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_VoxelMapCompressed_src_size(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_origin
{
public:
  explicit Init_VoxelMapCompressed_origin(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  Init_VoxelMapCompressed_width origin(::unitree_go::msg::VoxelMapCompressed::_origin_type arg)
  {
    msg_.origin = std::move(arg);
    return Init_VoxelMapCompressed_width(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_resolution
{
public:
  explicit Init_VoxelMapCompressed_resolution(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  Init_VoxelMapCompressed_origin resolution(::unitree_go::msg::VoxelMapCompressed::_resolution_type arg)
  {
    msg_.resolution = std::move(arg);
    return Init_VoxelMapCompressed_origin(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_frame_id
{
public:
  explicit Init_VoxelMapCompressed_frame_id(::unitree_go::msg::VoxelMapCompressed & msg)
  : msg_(msg)
  {}
  Init_VoxelMapCompressed_resolution frame_id(::unitree_go::msg::VoxelMapCompressed::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_VoxelMapCompressed_resolution(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

class Init_VoxelMapCompressed_stamp
{
public:
  Init_VoxelMapCompressed_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VoxelMapCompressed_frame_id stamp(::unitree_go::msg::VoxelMapCompressed::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_VoxelMapCompressed_frame_id(msg_);
  }

private:
  ::unitree_go::msg::VoxelMapCompressed msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::unitree_go::msg::VoxelMapCompressed>()
{
  return unitree_go::msg::builder::Init_VoxelMapCompressed_stamp();
}

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__BUILDER_HPP_
