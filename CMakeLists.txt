cmake_minimum_required(VERSION 2.8.3)
project(gazebo_world_builder)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -Wall -Wextra")
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  )

find_package(PNG)
include_directories(include)

catkin_package(
	INCLUDE_DIRS include
  CATKIN_DEPENDS
  std_msgs
  )

add_executable(extrudeWorld src/extrudeWorld.cpp src/pbmMapImage.cpp src/quadTree.cpp)

add_dependencies(extrudeWorld ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(extrudeWorld
   ${catkin_LIBRARIES}
   ${PNG_LIBRARIES}
 )

add_executable(getLocations src/getLocations.cpp src/pbmMapImage.cpp)
add_dependencies(getLocations ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(getLocations
   ${catkin_LIBRARIES}
   ${PNG_LIBRARIES}
 )
