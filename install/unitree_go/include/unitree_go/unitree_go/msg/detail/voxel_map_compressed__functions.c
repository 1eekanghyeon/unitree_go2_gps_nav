// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from unitree_go:msg/VoxelMapCompressed.idl
// generated code does not contain a copyright notice
#include "unitree_go/msg/detail/voxel_map_compressed__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
unitree_go__msg__VoxelMapCompressed__init(unitree_go__msg__VoxelMapCompressed * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    unitree_go__msg__VoxelMapCompressed__fini(msg);
    return false;
  }
  // resolution
  // origin
  // width
  // src_size
  // data
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->data, 0)) {
    unitree_go__msg__VoxelMapCompressed__fini(msg);
    return false;
  }
  return true;
}

void
unitree_go__msg__VoxelMapCompressed__fini(unitree_go__msg__VoxelMapCompressed * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // resolution
  // origin
  // width
  // src_size
  // data
  rosidl_runtime_c__uint8__Sequence__fini(&msg->data);
}

bool
unitree_go__msg__VoxelMapCompressed__are_equal(const unitree_go__msg__VoxelMapCompressed * lhs, const unitree_go__msg__VoxelMapCompressed * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stamp
  if (lhs->stamp != rhs->stamp) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frame_id), &(rhs->frame_id)))
  {
    return false;
  }
  // resolution
  if (lhs->resolution != rhs->resolution) {
    return false;
  }
  // origin
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->origin[i] != rhs->origin[i]) {
      return false;
    }
  }
  // width
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->width[i] != rhs->width[i]) {
      return false;
    }
  }
  // src_size
  if (lhs->src_size != rhs->src_size) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
unitree_go__msg__VoxelMapCompressed__copy(
  const unitree_go__msg__VoxelMapCompressed * input,
  unitree_go__msg__VoxelMapCompressed * output)
{
  if (!input || !output) {
    return false;
  }
  // stamp
  output->stamp = input->stamp;
  // frame_id
  if (!rosidl_runtime_c__String__copy(
      &(input->frame_id), &(output->frame_id)))
  {
    return false;
  }
  // resolution
  output->resolution = input->resolution;
  // origin
  for (size_t i = 0; i < 3; ++i) {
    output->origin[i] = input->origin[i];
  }
  // width
  for (size_t i = 0; i < 3; ++i) {
    output->width[i] = input->width[i];
  }
  // src_size
  output->src_size = input->src_size;
  // data
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

unitree_go__msg__VoxelMapCompressed *
unitree_go__msg__VoxelMapCompressed__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelMapCompressed * msg = (unitree_go__msg__VoxelMapCompressed *)allocator.allocate(sizeof(unitree_go__msg__VoxelMapCompressed), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(unitree_go__msg__VoxelMapCompressed));
  bool success = unitree_go__msg__VoxelMapCompressed__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
unitree_go__msg__VoxelMapCompressed__destroy(unitree_go__msg__VoxelMapCompressed * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    unitree_go__msg__VoxelMapCompressed__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
unitree_go__msg__VoxelMapCompressed__Sequence__init(unitree_go__msg__VoxelMapCompressed__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelMapCompressed * data = NULL;

  if (size) {
    data = (unitree_go__msg__VoxelMapCompressed *)allocator.zero_allocate(size, sizeof(unitree_go__msg__VoxelMapCompressed), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = unitree_go__msg__VoxelMapCompressed__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        unitree_go__msg__VoxelMapCompressed__fini(&data[i - 1]);
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
unitree_go__msg__VoxelMapCompressed__Sequence__fini(unitree_go__msg__VoxelMapCompressed__Sequence * array)
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
      unitree_go__msg__VoxelMapCompressed__fini(&array->data[i]);
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

unitree_go__msg__VoxelMapCompressed__Sequence *
unitree_go__msg__VoxelMapCompressed__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__VoxelMapCompressed__Sequence * array = (unitree_go__msg__VoxelMapCompressed__Sequence *)allocator.allocate(sizeof(unitree_go__msg__VoxelMapCompressed__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = unitree_go__msg__VoxelMapCompressed__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
unitree_go__msg__VoxelMapCompressed__Sequence__destroy(unitree_go__msg__VoxelMapCompressed__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    unitree_go__msg__VoxelMapCompressed__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
unitree_go__msg__VoxelMapCompressed__Sequence__are_equal(const unitree_go__msg__VoxelMapCompressed__Sequence * lhs, const unitree_go__msg__VoxelMapCompressed__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!unitree_go__msg__VoxelMapCompressed__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
unitree_go__msg__VoxelMapCompressed__Sequence__copy(
  const unitree_go__msg__VoxelMapCompressed__Sequence * input,
  unitree_go__msg__VoxelMapCompressed__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(unitree_go__msg__VoxelMapCompressed);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    unitree_go__msg__VoxelMapCompressed * data =
      (unitree_go__msg__VoxelMapCompressed *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!unitree_go__msg__VoxelMapCompressed__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          unitree_go__msg__VoxelMapCompressed__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!unitree_go__msg__VoxelMapCompressed__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
