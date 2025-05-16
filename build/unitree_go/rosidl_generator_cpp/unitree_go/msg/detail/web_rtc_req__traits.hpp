// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/WebRtcReq.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/web_rtc_req__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const WebRtcReq & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: topic
  {
    out << "topic: ";
    rosidl_generator_traits::value_to_yaml(msg.topic, out);
    out << ", ";
  }

  // member: api_id
  {
    out << "api_id: ";
    rosidl_generator_traits::value_to_yaml(msg.api_id, out);
    out << ", ";
  }

  // member: parameter
  {
    out << "parameter: ";
    rosidl_generator_traits::value_to_yaml(msg.parameter, out);
    out << ", ";
  }

  // member: priority
  {
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const WebRtcReq & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: topic
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "topic: ";
    rosidl_generator_traits::value_to_yaml(msg.topic, out);
    out << "\n";
  }

  // member: api_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "api_id: ";
    rosidl_generator_traits::value_to_yaml(msg.api_id, out);
    out << "\n";
  }

  // member: parameter
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "parameter: ";
    rosidl_generator_traits::value_to_yaml(msg.parameter, out);
    out << "\n";
  }

  // member: priority
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const WebRtcReq & msg, bool use_flow_style = false)
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
  const unitree_go::msg::WebRtcReq & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::WebRtcReq & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::WebRtcReq>()
{
  return "unitree_go::msg::WebRtcReq";
}

template<>
inline const char * name<unitree_go::msg::WebRtcReq>()
{
  return "unitree_go/msg/WebRtcReq";
}

template<>
struct has_fixed_size<unitree_go::msg::WebRtcReq>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<unitree_go::msg::WebRtcReq>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<unitree_go::msg::WebRtcReq>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__TRAITS_HPP_
