// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "unitree_go/msg/detail/voxel_height_map_state__struct.h"
#include "unitree_go/msg/detail/voxel_height_map_state__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool unitree_go__msg__voxel_height_map_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[59];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("unitree_go.msg._voxel_height_map_state.VoxelHeightMapState", full_classname_dest, 58) == 0);
  }
  unitree_go__msg__VoxelHeightMapState * ros_message = _ros_message;
  {  // stamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "stamp");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->stamp = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // stamp_cloud
    PyObject * field = PyObject_GetAttrString(_pymsg, "stamp_cloud");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->stamp_cloud = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // stamp_odom
    PyObject * field = PyObject_GetAttrString(_pymsg, "stamp_odom");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->stamp_odom = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // height_map_size
    PyObject * field = PyObject_GetAttrString(_pymsg, "height_map_size");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->height_map_size = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // voxel_map_size
    PyObject * field = PyObject_GetAttrString(_pymsg, "voxel_map_size");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->voxel_map_size = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * unitree_go__msg__voxel_height_map_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VoxelHeightMapState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("unitree_go.msg._voxel_height_map_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VoxelHeightMapState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  unitree_go__msg__VoxelHeightMapState * ros_message = (unitree_go__msg__VoxelHeightMapState *)raw_ros_message;
  {  // stamp
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->stamp);
    {
      int rc = PyObject_SetAttrString(_pymessage, "stamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // stamp_cloud
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->stamp_cloud);
    {
      int rc = PyObject_SetAttrString(_pymessage, "stamp_cloud", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // stamp_odom
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->stamp_odom);
    {
      int rc = PyObject_SetAttrString(_pymessage, "stamp_odom", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // height_map_size
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->height_map_size);
    {
      int rc = PyObject_SetAttrString(_pymessage, "height_map_size", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // voxel_map_size
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->voxel_map_size);
    {
      int rc = PyObject_SetAttrString(_pymessage, "voxel_map_size", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
