// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_H_
#define UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VoxelHeightMapState in the package unitree_go.
/**
  * Timestamp (in seconds since epoch)
 */
typedef struct unitree_go__msg__VoxelHeightMapState
{
  double stamp;
  /// Timestamp for the point cloud (in seconds)
  double stamp_cloud;
  /// Timestamp for odometry (in seconds)
  double stamp_odom;
  /// Size of the height map
  uint32_t height_map_size;
  /// Size of the voxel map
  uint32_t voxel_map_size;
} unitree_go__msg__VoxelHeightMapState;

// Struct for a sequence of unitree_go__msg__VoxelHeightMapState.
typedef struct unitree_go__msg__VoxelHeightMapState__Sequence
{
  unitree_go__msg__VoxelHeightMapState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} unitree_go__msg__VoxelHeightMapState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_H_
