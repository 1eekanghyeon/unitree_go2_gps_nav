// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice
#include "unitree_go/msg/detail/voxel_height_map_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
unitree_go__msg__VoxelHeightMapState__init(unitree_go__msg__VoxelHeightMapState * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  // stamp_cloud
  // stamp_odom
  // height_map_size
  // voxel_map_size
  return true;
}

void
unitree_go__msg__VoxelHeightMapState__fini(unitree_go__msg__VoxelHeightMapState * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  // stamp_cloud
  // stamp_odom
  // height_map_size
  // voxel_map_size
}

bool
unitree_go__msg__VoxelHeightMapState__are_equal(const unitree_go__msg__VoxelHeightMapState * lhs, const unitree_go__msg__VoxelHeightMapState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stamp
  if (lhs->stamp != rhs->stamp) {
    return false;
  }
  // stamp_cloud
  if (lhs->stamp_cloud != rhs->stamp_cloud) {
    return false;
  }
  // stamp_odom
  if (lhs->stamp_odom != rhs->stamp_odom) {
    return false;
  }
  // height_map_size
  if (lhs->height_map_size != rhs->height_map_size) {
    return false;
  }
  // voxel_map_size
  if (lhs->voxel_map_size != rhs->voxel_map_size) {
    return false;
  }
  return true;
}

bool
unitree_go__msg__VoxelHeightMapState__copy(
  const unitree_go__msg__VoxelHeightMapState * input,
  unitree_go__msg__VoxelHeightMapState * output)
{
  if (!input || !output) {
    return false;
  }
  // stamp
  output->stamp = input->stamp;
  // stamp_cloud
  output->stamp_cloud = input->stamp_cloud;
  // stamp_odom
  output->stamp_odom = input->stamp_odom;
  // height_map_size
  output->height_map_size = input->height_map_size;
  // voxel_map_size
  output->voxel_map_size = input->voxel_map_size;
  return true;
}

unitree_go__msg__VoxelHeightMapState *
unitree_go__msg__VoxelHeightMapState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelHeightMapState * msg = (unitree_go__msg__VoxelHeightMapState *)allocator.allocate(sizeof(unitree_go__msg__VoxelHeightMapState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(unitree_go__msg__VoxelHeightMapState));
  bool success = unitree_go__msg__VoxelHeightMapState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
unitree_go__msg__VoxelHeightMapState__destroy(unitree_go__msg__VoxelHeightMapState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    unitree_go__msg__VoxelHeightMapState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
unitree_go__msg__VoxelHeightMapState__Sequence__init(unitree_go__msg__VoxelHeightMapState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelHeightMapState * data = NULL;

  if (size) {
    data = (unitree_go__msg__VoxelHeightMapState *)allocator.zero_allocate(size, sizeof(unitree_go__msg__VoxelHeightMapState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = unitree_go__msg__VoxelHeightMapState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        unitree_go__msg__VoxelHeightMapState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
unitree_go__msg__VoxelHeightMapState__Sequence__fini(unitree_go__msg__VoxelHeightMapState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      unitree_go__msg__VoxelHeightMapState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

unitree_go__msg__VoxelHeightMapState__Sequence *
unitree_go__msg__VoxelHeightMapState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelHeightMapState__Sequence * array = (unitree_go__msg__VoxelHeightMapState__Sequence *)allocator.allocate(sizeof(unitree_go__msg__VoxelHeightMapState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = unitree_go__msg__VoxelHeightMapState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
unitree_go__msg__VoxelHeightMapState__Sequence__destroy(unitree_go__msg__VoxelHeightMapState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    unitree_go__msg__VoxelHeightMapState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
unitree_go__msg__VoxelHeightMapState__Sequence__are_equal(const unitree_go__msg__VoxelHeightMapState__Sequence * lhs, const unitree_go__msg__VoxelHeightMapState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!unitree_go__msg__VoxelHeightMapState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
unitree_go__msg__VoxelHeightMapState__Sequence__copy(
  const unitree_go__msg__VoxelHeightMapState__Sequence * input,
  unitree_go__msg__VoxelHeightMapState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(unitree_go__msg__VoxelHeightMapState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    unitree_go__msg__VoxelHeightMapState * data =
      (unitree_go__msg__VoxelHeightMapState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!unitree_go__msg__VoxelHeightMapState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          unitree_go__msg__VoxelHeightMapState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!unitree_go__msg__VoxelHeightMapState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
