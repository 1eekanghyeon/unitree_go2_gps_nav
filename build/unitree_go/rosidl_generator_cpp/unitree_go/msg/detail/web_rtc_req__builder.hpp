// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from unitree_go:msg/WebRtcReq.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__BUILDER_HPP_
#define UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "unitree_go/msg/detail/web_rtc_req__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace unitree_go
{

namespace msg
{

namespace builder
{

class Init_WebRtcReq_priority
{
public:
  explicit Init_WebRtcReq_priority(::unitree_go::msg::WebRtcReq & msg)
  : msg_(msg)
  {}
  ::unitree_go::msg::WebRtcReq priority(::unitree_go::msg::WebRtcReq::_priority_type arg)
  {
    msg_.priority = std::move(arg);
    return std::move(msg_);
  }

private:
  ::unitree_go::msg::WebRtcReq msg_;
};

class Init_WebRtcReq_parameter
{
public:
  explicit Init_WebRtcReq_parameter(::unitree_go::msg::WebRtcReq & msg)
  : msg_(msg)
  {}
  Init_WebRtcReq_priority parameter(::unitree_go::msg::WebRtcReq::_parameter_type arg)
  {
    msg_.parameter = std::move(arg);
    return Init_WebRtcReq_priority(msg_);
  }

private:
  ::unitree_go::msg::WebRtcReq msg_;
};

class Init_WebRtcReq_api_id
{
public:
  explicit Init_WebRtcReq_api_id(::unitree_go::msg::WebRtcReq & msg)
  : msg_(msg)
  {}
  Init_WebRtcReq_parameter api_id(::unitree_go::msg::WebRtcReq::_api_id_type arg)
  {
    msg_.api_id = std::move(arg);
    return Init_WebRtcReq_parameter(msg_);
  }

private:
  ::unitree_go::msg::WebRtcReq msg_;
};

class Init_WebRtcReq_topic
{
public:
  explicit Init_WebRtcReq_topic(::unitree_go::msg::WebRtcReq & msg)
  : msg_(msg)
  {}
  Init_WebRtcReq_api_id topic(::unitree_go::msg::WebRtcReq::_topic_type arg)
  {
    msg_.topic = std::move(arg);
    return Init_WebRtcReq_api_id(msg_);
  }

private:
  ::unitree_go::msg::WebRtcReq msg_;
};

class Init_WebRtcReq_id
{
public:
  Init_WebRtcReq_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WebRtcReq_topic id(::unitree_go::msg::WebRtcReq::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_WebRtcReq_topic(msg_);
  }

private:
  ::unitree_go::msg::WebRtcReq msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::unitree_go::msg::WebRtcReq>()
{
  return unitree_go::msg::builder::Init_WebRtcReq_id();
}

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__BUILDER_HPP_
