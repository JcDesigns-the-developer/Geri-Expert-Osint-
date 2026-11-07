cmake_minimum_required(VERSION 3.24)
project(raven_core VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(raven_core STATIC src/evidence.cpp)
target_include_directories(raven_core PUBLIC include)
if(MSVC)
  target_compile_options(raven_core PRIVATE /W4 /permissive-)
else()
  target_compile_options(raven_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

add_executable(raven_core_tests tests/evidence_tests.cpp)
target_link_libraries(raven_core_tests PRIVATE raven_core)
enable_testing()
add_test(NAME raven_core_tests COMMAND raven_core_tests)
