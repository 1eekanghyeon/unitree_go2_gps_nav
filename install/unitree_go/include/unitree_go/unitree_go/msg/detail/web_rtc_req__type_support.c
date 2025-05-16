// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/WebRtcReq.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/web_rtc_req__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/web_rtc_req__functions.h"
#include "unitree_go/msg/detail/web_rtc_req__struct.h"


// Include directives for member types
// Member `topic`
// Member `parameter`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__WebRtcReq__init(message_memory);
}

void unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_fini_function(void * message_memory)
{
  unitree_go__msg__WebRtcReq__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_member_array[5] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__WebRtcReq, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "topic",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__WebRtcReq, topic),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "api_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__WebRtcReq, api_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "parameter",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__WebRtcReq, parameter),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "priority",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__WebRtcReq, priority),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_members = {
  "unitree_go__msg",  // message namespace
  "WebRtcReq",  // message name
  5,  // number of fields
  sizeof(unitree_go__msg__WebRtcReq),
  unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_member_array,  // message members
  unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_type_support_handle = {
  0,
  &unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, WebRtcReq)() {
  if (!unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__WebRtcReq__rosidl_typesupport_introspection_c__WebRtcReq_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
