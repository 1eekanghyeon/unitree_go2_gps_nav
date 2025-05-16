// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from unitree_go:msg/Go2FrontVideoData.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__STRUCT_H_
#define UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Go2FrontVideoData in the package unitree_go.
/**
  * Time frame as a 64-bit unsigned integer
 */
typedef struct unitree_go__msg__Go2FrontVideoData
{
  uint64_t time_frame;
  /// Resolution as a 16-bit signed integer
  int16_t resolution;
  /// Data as a sequence of bytes (octets)
  rosidl_runtime_c__uint8__Sequence data;
} unitree_go__msg__Go2FrontVideoData;

// Struct for a sequence of unitree_go__msg__Go2FrontVideoData.
typedef struct unitree_go__msg__Go2FrontVideoData__Sequence
{
  unitree_go__msg__Go2FrontVideoData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} unitree_go__msg__Go2FrontVideoData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UNITREE_GO__MSG__DETAIL__GO2_FRONT_VIDEO_DATA__STRUCT_H_
