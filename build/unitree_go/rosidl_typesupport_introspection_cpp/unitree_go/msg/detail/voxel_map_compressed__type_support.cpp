// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from unitree_go:msg/VoxelMapCompressed.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "unitree_go/msg/detail/voxel_map_compressed__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace unitree_go
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void VoxelMapCompressed_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) unitree_go::msg::VoxelMapCompressed(_init);
}

void VoxelMapCompressed_fini_function(void * message_memory)
{
  auto typed_message = static_cast<unitree_go::msg::VoxelMapCompressed *>(message_memory);
  typed_message->~VoxelMapCompressed();
}

size_t size_function__VoxelMapCompressed__origin(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__VoxelMapCompressed__origin(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__VoxelMapCompressed__origin(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__VoxelMapCompressed__origin(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__VoxelMapCompressed__origin(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__VoxelMapCompressed__origin(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__VoxelMapCompressed__origin(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__VoxelMapCompressed__width(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__VoxelMapCompressed__width(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<int16_t, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__VoxelMapCompressed__width(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<int16_t, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__VoxelMapCompressed__width(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int16_t *>(
    get_const_function__VoxelMapCompressed__width(untyped_member, index));
  auto & value = *reinterpret_cast<int16_t *>(untyped_value);
  value = item;
}

void assign_function__VoxelMapCompressed__width(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int16_t *>(
    get_function__VoxelMapCompressed__width(untyped_member, index));
  const auto & value = *reinterpret_cast<const int16_t *>(untyped_value);
  item = value;
}

size_t size_function__VoxelMapCompressed__data(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VoxelMapCompressed__data(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void * get_function__VoxelMapCompressed__data(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__VoxelMapCompressed__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__VoxelMapCompressed__data(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__VoxelMapCompressed__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__VoxelMapCompressed__data(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

void resize_function__VoxelMapCompressed__data(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember VoxelMapCompressed_message_member_array[7] = {
  {
    "stamp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, stamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "frame_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, frame_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "resolution",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, resolution),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "origin",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, origin),  // bytes offset in struct
    nullptr,  // default value
    size_function__VoxelMapCompressed__origin,  // size() function pointer
    get_const_function__VoxelMapCompressed__origin,  // get_const(index) function pointer
    get_function__VoxelMapCompressed__origin,  // get(index) function pointer
    fetch_function__VoxelMapCompressed__origin,  // fetch(index, &value) function pointer
    assign_function__VoxelMapCompressed__origin,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "width",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, width),  // bytes offset in struct
    nullptr,  // default value
    size_function__VoxelMapCompressed__width,  // size() function pointer
    get_const_function__VoxelMapCompressed__width,  // get_const(index) function pointer
    get_function__VoxelMapCompressed__width,  // get(index) function pointer
    fetch_function__VoxelMapCompressed__width,  // fetch(index, &value) function pointer
    assign_function__VoxelMapCompressed__width,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "src_size",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, src_size),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "data",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::VoxelMapCompressed, data),  // bytes offset in struct
    nullptr,  // default value
    size_function__VoxelMapCompressed__data,  // size() function pointer
    get_const_function__VoxelMapCompressed__data,  // get_const(index) function pointer
    get_function__VoxelMapCompressed__data,  // get(index) function pointer
    fetch_function__VoxelMapCompressed__data,  // fetch(index, &value) function pointer
    assign_function__VoxelMapCompressed__data,  // assign(index, value) function pointer
    resize_function__VoxelMapCompressed__data  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers VoxelMapCompressed_message_members = {
  "unitree_go::msg",  // message namespace
  "VoxelMapCompressed",  // message name
  7,  // number of fields
  sizeof(unitree_go::msg::VoxelMapCompressed),
  VoxelMapCompressed_message_member_array,  // message members
  VoxelMapCompressed_init_function,  // function to initialize message memory (memory has to be allocated)
  VoxelMapCompressed_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t VoxelMapCompressed_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &VoxelMapCompressed_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace unitree_go


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<unitree_go::msg::VoxelMapCompressed>()
{
  return &::unitree_go::msg::rosidl_typesupport_introspection_cpp::VoxelMapCompressed_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, unitree_go, msg, VoxelMapCompressed)() {
  return &::unitree_go::msg::rosidl_typesupport_introspection_cpp::VoxelMapCompressed_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
