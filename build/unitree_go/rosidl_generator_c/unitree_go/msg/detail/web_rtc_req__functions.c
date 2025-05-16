// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from unitree_go:msg/WebRtcReq.idl
// generated code does not contain a copyright notice
#include "unitree_go/msg/detail/web_rtc_req__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `topic`
// Member `parameter`
#include "rosidl_runtime_c/string_functions.h"

bool
unitree_go__msg__WebRtcReq__init(unitree_go__msg__WebRtcReq * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // topic
  if (!rosidl_runtime_c__String__init(&msg->topic)) {
    unitree_go__msg__WebRtcReq__fini(msg);
    return false;
  }
  // api_id
  // parameter
  if (!rosidl_runtime_c__String__init(&msg->parameter)) {
    unitree_go__msg__WebRtcReq__fini(msg);
    return false;
  }
  // priority
  return true;
}

void
unitree_go__msg__WebRtcReq__fini(unitree_go__msg__WebRtcReq * msg)
{
  if (!msg) {
    return;
  }
  // id
  // topic
  rosidl_runtime_c__String__fini(&msg->topic);
  // api_id
  // parameter
  rosidl_runtime_c__String__fini(&msg->parameter);
  // priority
}

bool
unitree_go__msg__WebRtcReq__are_equal(const unitree_go__msg__WebRtcReq * lhs, const unitree_go__msg__WebRtcReq * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // topic
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->topic), &(rhs->topic)))
  {
    return false;
  }
  // api_id
  if (lhs->api_id != rhs->api_id) {
    return false;
  }
  // parameter
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->parameter), &(rhs->parameter)))
  {
    return false;
  }
  // priority
  if (lhs->priority != rhs->priority) {
    return false;
  }
  return true;
}

bool
unitree_go__msg__WebRtcReq__copy(
  const unitree_go__msg__WebRtcReq * input,
  unitree_go__msg__WebRtcReq * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // topic
  if (!rosidl_runtime_c__String__copy(
      &(input->topic), &(output->topic)))
  {
    return false;
  }
  // api_id
  output->api_id = input->api_id;
  // parameter
  if (!rosidl_runtime_c__String__copy(
      &(input->parameter), &(output->parameter)))
  {
    return false;
  }
  // priority
  output->priority = input->priority;
  return true;
}

unitree_go__msg__WebRtcReq *
unitree_go__msg__WebRtcReq__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__WebRtcReq * msg = (unitree_go__msg__WebRtcReq *)allocator.allocate(sizeof(unitree_go__msg__WebRtcReq), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(unitree_go__msg__WebRtcReq));
  bool success = unitree_go__msg__WebRtcReq__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
unitree_go__msg__WebRtcReq__destroy(unitree_go__msg__WebRtcReq * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    unitree_go__msg__WebRtcReq__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
unitree_go__msg__WebRtcReq__Sequence__init(unitree_go__msg__WebRtcReq__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__WebRtcReq * data = NULL;

  if (size) {
    data = (unitree_go__msg__WebRtcReq *)allocator.zero_allocate(size, sizeof(unitree_go__msg__WebRtcReq), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = unitree_go__msg__WebRtcReq__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        unitree_go__msg__WebRtcReq__fini(&data[i - 1]);
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
unitree_go__msg__WebRtcReq__Sequence__fini(unitree_go__msg__WebRtcReq__Sequence * array)
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
      unitree_go__msg__WebRtcReq__fini(&array->data[i]);
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

unitree_go__msg__WebRtcReq__Sequence *
unitree_go__msg__WebRtcReq__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  unitree_go__msg__WebRtcReq__Sequence * array = (unitree_go__msg__WebRtcReq__Sequence *)allocator.allocate(sizeof(unitree_go__msg__WebRtcReq__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = unitree_go__msg__WebRtcReq__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
unitree_go__msg__WebRtcReq__Sequence__destroy(unitree_go__msg__WebRtcReq__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    unitree_go__msg__WebRtcReq__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
unitree_go__msg__WebRtcReq__Sequence__are_equal(const unitree_go__msg__WebRtcReq__Sequence * lhs, const unitree_go__msg__WebRtcReq__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!unitree_go__msg__WebRtcReq__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
unitree_go__msg__WebRtcReq__Sequence__copy(
  const unitree_go__msg__WebRtcReq__Sequence * input,
  unitree_go__msg__WebRtcReq__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(unitree_go__msg__WebRtcReq);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    unitree_go__msg__WebRtcReq * data =
      (unitree_go__msg__WebRtcReq *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!unitree_go__msg__WebRtcReq__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          unitree_go__msg__WebRtcReq__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!unitree_go__msg__WebRtcReq__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
