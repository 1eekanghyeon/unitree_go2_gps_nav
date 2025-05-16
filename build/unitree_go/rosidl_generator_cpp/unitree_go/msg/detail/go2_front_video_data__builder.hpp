// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from unitree_go:msg/Go2FrontVideoData.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__BUILDER_HPP_
#define UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "unitree_go/msg/detail/go2_front_video_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace unitree_go
{

namespace msg
{

namespace builder
{

class Init_Go2FrontVideoData_data
{
public:
  explicit Init_Go2FrontVideoData_data(::unitree_go::msg::Go2FrontVideoData & msg)
  : msg_(msg)
  {}
  ::unitree_go::msg::Go2FrontVideoData data(::unitree_go::msg::Go2FrontVideoData::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::unitree_go::msg::Go2FrontVideoData msg_;
};

class Init_Go2FrontVideoData_resolution
{
public:
  explicit Init_Go2FrontVideoData_resolution(::unitree_go::msg::Go2FrontVideoData & msg)
  : msg_(msg)
  {}
  Init_Go2FrontVideoData_data resolution(::unitree_go::msg::Go2FrontVideoData::_resolution_type arg)
  {
    msg_.resolution = std::move(arg);
    return Init_Go2FrontVideoData_data(msg_);
  }

private:
  ::unitree_go::msg::Go2FrontVideoData msg_;
};

class Init_Go2FrontVideoData_time_frame
{
public:
  Init_Go2FrontVideoData_time_frame()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Go2FrontVideoData_resolution time_frame(::unitree_go::msg::Go2FrontVideoData::_time_frame_type arg)
  {
    msg_.time_frame = std::move(arg);
    return Init_Go2FrontVideoData_resolution(msg_);
  }

private:
  ::unitree_go::msg::Go2FrontVideoData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::unitree_go::msg::Go2FrontVideoData>()
{
  return unitree_go::msg::builder::Init_Go2FrontVideoData_time_frame();
}

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__BUILDER_HPP_
