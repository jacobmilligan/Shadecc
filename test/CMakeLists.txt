project(spirv_wrapper_test)
cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_CXX_STANDARD 14)

file(GLOB_RECURSE shader_sources ${CMAKE_CURRENT_SOURCE_DIR}/build/*.cpp)

add_executable(${PROJECT_NAME} main.cpp ${shader_sources})
target_link_libraries(${PROJECT_NAME} spirv_wrapper)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../shadecc/include)