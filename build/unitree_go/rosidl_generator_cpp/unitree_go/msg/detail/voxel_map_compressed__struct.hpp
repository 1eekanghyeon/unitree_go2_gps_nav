// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from unitree_go:msg/VoxelMapCompressed.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__STRUCT_HPP_
#define UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__unitree_go__msg__VoxelMapCompressed __attribute__((deprecated))
#else
# define DEPRECATED__unitree_go__msg__VoxelMapCompressed __declspec(deprecated)
#endif

namespace unitree_go
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VoxelMapCompressed_
{
  using Type = VoxelMapCompressed_<ContainerAllocator>;

  explicit VoxelMapCompressed_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stamp = 0.0;
      this->frame_id = "";
      this->resolution = 0.0;
      std::fill<typename std::array<double, 3>::iterator, double>(this->origin.begin(), this->origin.end(), 0.0);
      std::fill<typename std::array<int16_t, 3>::iterator, int16_t>(this->width.begin(), this->width.end(), 0);
      this->src_size = 0ull;
    }
  }

  explicit VoxelMapCompressed_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    origin(_alloc),
    width(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stamp = 0.0;
      this->frame_id = "";
      this->resolution = 0.0;
      std::fill<typename std::array<double, 3>::iterator, double>(this->origin.begin(), this->origin.end(), 0.0);
      std::fill<typename std::array<int16_t, 3>::iterator, int16_t>(this->width.begin(), this->width.end(), 0);
      this->src_size = 0ull;
    }
  }

  // field types and members
  using _stamp_type =
    double;
  _stamp_type stamp;
  using _frame_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frame_id_type frame_id;
  using _resolution_type =
    double;
  _resolution_type resolution;
  using _origin_type =
    std::array<double, 3>;
  _origin_type origin;
  using _width_type =
    std::array<int16_t, 3>;
  _width_type width;
  using _src_size_type =
    uint64_t;
  _src_size_type src_size;
  using _data_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__stamp(
    const double & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__frame_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frame_id = _arg;
    return *this;
  }
  Type & set__resolution(
    const double & _arg)
  {
    this->resolution = _arg;
    return *this;
  }
  Type & set__origin(
    const std::array<double, 3> & _arg)
  {
    this->origin = _arg;
    return *this;
  }
  Type & set__width(
    const std::array<int16_t, 3> & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__src_size(
    const uint64_t & _arg)
  {
    this->src_size = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> *;
  using ConstRawPtr =
    const unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__unitree_go__msg__VoxelMapCompressed
    std::shared_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__unitree_go__msg__VoxelMapCompressed
    std::shared_ptr<unitree_go::msg::VoxelMapCompressed_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VoxelMapCompressed_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->frame_id != other.frame_id) {
      return false;
    }
    if (this->resolution != other.resolution) {
      return false;
    }
    if (this->origin != other.origin) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->src_size != other.src_size) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const VoxelMapCompressed_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VoxelMapCompressed_

// alias to use template instance with default allocator
using VoxelMapCompressed =
  unitree_go::msg::VoxelMapCompressed_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace unitree_go

#endif  // UNITREE_GO__MSG__DETAIL__VOXEL_MAP_COMPRESSED__STRUCT_HPP_
