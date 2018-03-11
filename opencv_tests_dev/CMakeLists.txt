cmake_minimum_required (VERSION 2.8)

project(points)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(cv_points points.cpp)

target_link_libraries(cv_points ${OpenCV_LIBS})
