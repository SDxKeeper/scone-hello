# Copyright (C) 2018-2019 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#
CMAKE_MINIMUM_REQUIRED(VERSION 3.2 FATAL_ERROR)

PROJECT(hello_classification CXX)
set (TARGET_NAME "hello_world")

## to use C++11
set (CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_STANDARD_REQUIRED ON)

FILE(GLOB PROJECT_HEADERS "*.h")
FILE(GLOB PROJECT_SOURCES "*.cpp")
# Create executable file from sources
add_executable(${TARGET_NAME} ${PROJECT_SOURCES} ${PROJECT_HEADERS})


