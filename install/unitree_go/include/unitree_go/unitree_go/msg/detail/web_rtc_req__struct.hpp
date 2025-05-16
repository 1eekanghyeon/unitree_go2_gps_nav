// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from unitree_go:msg/WebRtcReq.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__STRUCT_HPP_
#define UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__unitree_go__msg__WebRtcReq __attribute__((deprecated))
#else
# define DEPRECATED__unitree_go__msg__WebRtcReq __declspec(deprecated)
#endif

namespace unitree_go
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WebRtcReq_
{
  using Type = WebRtcReq_<ContainerAllocator>;

  explicit WebRtcReq_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->topic = "";
      this->api_id = 0ll;
      this->parameter = "";
      this->priority = 0;
    }
  }

  explicit WebRtcReq_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : topic(_alloc),
    parameter(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->topic = "";
      this->api_id = 0ll;
      this->parameter = "";
      this->priority = 0;
    }
  }

  // field types and members
  using _id_type =
    int64_t;
  _id_type id;
  using _topic_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _topic_type topic;
  using _api_id_type =
    int64_t;
  _api_id_type api_id;
  using _parameter_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _parameter_type parameter;
  using _priority_type =
    uint8_t;
  _priority_type priority;

  // setters for named parameter idiom
  Type & set__id(
    const int64_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__topic(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->topic = _arg;
    return *this;
  }
  Type & set__api_id(
    const int64_t & _arg)
  {
    this->api_id = _arg;
    return *this;
  }
  Type & set__parameter(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->parameter = _arg;
    return *this;
  }
  Type & set__priority(
    const uint8_t & _arg)
  {
    this->priority = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    unitree_go::msg::WebRtcReq_<ContainerAllocator> *;
  using ConstRawPtr =
    const unitree_go::msg::WebRtcReq_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::WebRtcReq_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::WebRtcReq_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__unitree_go__msg__WebRtcReq
    std::shared_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__unitree_go__msg__WebRtcReq
    std::shared_ptr<unitree_go::msg::WebRtcReq_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WebRtcReq_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->topic != other.topic) {
      return false;
    }
    if (this->api_id != other.api_id) {
      return false;
    }
    if (this->parameter != other.parameter) {
      return false;
    }
    if (this->priority != other.priority) {
      return false;
    }
    return true;
  }
  bool operator!=(const WebRtcReq_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WebRtcReq_

// alias to use template instance with default allocator
using WebRtcReq =
  unitree_go::msg::WebRtcReq_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__WEB_RTC_REQ__STRUCT_HPP_
