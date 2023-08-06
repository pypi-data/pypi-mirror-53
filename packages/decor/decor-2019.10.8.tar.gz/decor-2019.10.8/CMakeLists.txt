cmake_minimum_required(VERSION 3.12)
project(decor)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

include(ExternalProject)

find_package(Qt5Core REQUIRED)

if (CMAKE_BUILD_TYPE MATCHES Release)
    add_definitions(-DQT_NO_DEBUG_OUTPUT)
else ()
    add_definitions(-DDECOR_DEBUG)
endif ()

add_library(
        distortion
        STATIC
        src/spline.cpp
        src/spline.h
        src/bispev.c
        src/bispev.h
        src/distortion.c
        src/distortion.h
        src/geodistortion.cpp
        src/geodistortion.h
)
target_link_libraries(
        distortion
        Qt5::Core
)

if (DECOR_BUILD_PYTHON)
    find_package(PythonLibs 3 REQUIRED)
    add_library(
            _decor
            SHARED
            src/bispev.c
            src/bispev.h
            src/distortion.c
            src/distortion.h
            src/bitmask.c
            src/bitmask.h
            src/decormodule.c
    )
    target_link_libraries(
            _decor
            ${PYTHON_LIBRARIES}
    )
    target_link_directories(
            _decor
            PUBLIC
            ${PYTHON_LIBRARIES}
    )
    target_include_directories(
            _decor
            PUBLIC
            ${PYTHON_INCLUDE_DIRS}
    )
endif ()

include(tests/tests.cmake)
