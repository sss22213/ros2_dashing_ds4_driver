cmake_minimum_required(VERSION 3.5)
project(ds4_driver)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
#find_package(laser_obs_msg REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

include_directories(
  include
)

# declare the message files to generate code for
set(msg_files
  "msg/Feedback.msg"
  "msg/Report.msg"
  "msg/Status.msg"
  "msg/Trackpad.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
    ${msg_files}
    DEPENDENCIES builtin_interfaces
    DEPENDENCIES std_msgs
    DEPENDENCIES sensor_msgs
)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

#add_executable(laser_tracker src/laser_tracker.cpp)
#ament_export_include_directories(include)
#ament_export_libraries(${PROJECT_NAME})
#ament_target_dependencies(laser_tracker "sensor_msgs" "rclcpp" "std_msgs" "laser_obs_msg")

#
#target_include_directories(laser_tracker PUBLIC
#  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
#  $<INSTALL_INTERFACE:include>)

#install(TARGETS ds4_driver
#  EXPORT export_${PROJECT_NAME}
#  DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install the python module for this package
ament_python_install_package(${PROJECT_NAME})
# Install python scripts
install(PROGRAMS scripts/controller.py DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS scripts/controller_ros.py DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS scripts/ds4_driver_node.py DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS scripts/logger.py DESTINATION lib/${PROJECT_NAME})
# install(PROGRAMS scripts/src/* DESTINATION lib/${PROJECT_NAME}/src)
# glob
#set(CUR ${PROJECT_NAME}/scripts)
#file(GLOB files ${PROJECT_NAME}/scripts)
#foreach(file IN LISTS files)
#    install(PROGRAMS scripts/${file} DESTINATION lib/${PROJECT_NAME})
    ## message(STATUS scripts/${file})
#endforeach(file)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
