cmake_minimum_required(VERSION 3.27)
project(dmx512_simulator C)
set(CMAKE_C_STANDARD 99)

include(FetchContent)
set(FETCHCONTENT_QUIET FALSE)
set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(BUILD_GAMES    OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    raylib
    GIT_REPOSITORY "https://github.com/raysan5/raylib.git"
    GIT_TAG "5.5"
    GIT_PROGRESS TRUE
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(raylib)

add_executable(dmx512_simulator src/main.c)
target_include_directories(dmx512_simulator PRIVATE vendor/clay)
target_link_libraries(dmx512_simulator PRIVATE raylib)

if (UNIX AND NOT APPLE)
    target_link_libraries(dmx512_simulator PRIVATE m)
endif()
