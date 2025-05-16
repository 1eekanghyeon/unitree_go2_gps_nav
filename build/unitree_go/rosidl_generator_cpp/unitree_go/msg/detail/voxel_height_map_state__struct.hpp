// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from unitree_go:msg/VoxelHeightMapState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_HPP_
#define UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__unitree_go__msg__VoxelHeightMapState __attribute__((deprecated))
#else
# define DEPRECATED__unitree_go__msg__VoxelHeightMapState __declspec(deprecated)
#endif

namespace unitree_go
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VoxelHeightMapState_
{
  using Type = VoxelHeightMapState_<ContainerAllocator>;

  explicit VoxelHeightMapState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stamp = 0.0;
      this->stamp_cloud = 0.0;
      this->stamp_odom = 0.0;
      this->height_map_size = 0ul;
      this->voxel_map_size = 0ul;
    }
  }

  explicit VoxelHeightMapState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stamp = 0.0;
      this->stamp_cloud = 0.0;
      this->stamp_odom = 0.0;
      this->height_map_size = 0ul;
      this->voxel_map_size = 0ul;
    }
  }

  // field types and members
  using _stamp_type =
    double;
  _stamp_type stamp;
  using _stamp_cloud_type =
    double;
  _stamp_cloud_type stamp_cloud;
  using _stamp_odom_type =
    double;
  _stamp_odom_type stamp_odom;
  using _height_map_size_type =
    uint32_t;
  _height_map_size_type height_map_size;
  using _voxel_map_size_type =
    uint32_t;
  _voxel_map_size_type voxel_map_size;

  // setters for named parameter idiom
  Type & set__stamp(
    const double & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__stamp_cloud(
    const double & _arg)
  {
    this->stamp_cloud = _arg;
    return *this;
  }
  Type & set__stamp_odom(
    const double & _arg)
  {
    this->stamp_odom = _arg;
    return *this;
  }
  Type & set__height_map_size(
    const uint32_t & _arg)
  {
    this->height_map_size = _arg;
    return *this;
  }
  Type & set__voxel_map_size(
    const uint32_t & _arg)
  {
    this->voxel_map_size = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> *;
  using ConstRawPtr =
    const unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__unitree_go__msg__VoxelHeightMapState
    std::shared_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__unitree_go__msg__VoxelHeightMapState
    std::shared_ptr<unitree_go::msg::VoxelHeightMapState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VoxelHeightMapState_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->stamp_cloud != other.stamp_cloud) {
      return false;
    }
    if (this->stamp_odom != other.stamp_odom) {
      return false;
    }
    if (this->height_map_size != other.height_map_size) {
      return false;
    }
    if (this->voxel_map_size != other.voxel_map_size) {
      return false;
    }
    return true;
  }
  bool operator!=(const VoxelHeightMapState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VoxelHeightMapState_

// alias to use template instance with default allocator
using VoxelHeightMapState =
  unitree_go::msg::VoxelHeightMapState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_HEIGHT_MAP_STATE__STRUCT_HPP_
