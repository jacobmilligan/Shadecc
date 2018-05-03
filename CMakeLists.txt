project(spirv_wrapper)
cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_CXX_STANDARD 14)

set(src_list spirv_wrapper/spirv_wrapper.cpp)

# Output binaries and libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/shadecc/bin/${CMAKE_SYSTEM_NAME})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/shadecc/libs/${CMAKE_SYSTEM_NAME})

add_library(${PROJECT_NAME} SHARED ${src_list})

target_include_directories(${PROJECT_NAME} PUBLIC spirv_wrapper)

# Setup SPIRV-Cross
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/deps/SPIRV-Cross)
set(spirv-cross_libraries spirv-cross-glsl spirv-cross-hlsl spirv-cross-cpp spirv-cross-msl spirv-cross-core)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/SPIRV-Cross)
target_link_libraries(${PROJECT_NAME} PRIVATE ${spirv-cross_libraries})

# Setup glslang
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/deps/glslang)
set(glslang_libraries glslang HLSL OSDependent OGLCompiler SPIRV glslang-default-resource-limits)
target_link_libraries(${PROJECT_NAME} PRIVATE ${glslang_libraries})
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/glslang)

add_subdirectory(test)
