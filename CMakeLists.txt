cmake_minimum_required(VERSION 3.14)
project(MiraiCP_debug LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (WIN32)
    # See Warning C4668
    add_compile_definitions(WIN32_LEAN_AND_MEAN)
endif ()

if (MSVC)
    message("MSVC detected")
    # 以utf8编译, for msvc; EHa参数启用标准 C++ stack unwinding; 启用多线程编译；禁止无返回值的函数；禁用两个与dll export相关的warning
    add_compile_options(/W4 /EHa /std:c++17 /MP /we4715 /wd4251 /wd4275 /Zc:__cplusplus)
else ()
    # 禁止无返回值的函数
    add_compile_options(-Wall -Werror=return-type)
    # hide symbol
    add_link_options(-fvisibility=hidden)
endif ()

#
add_compile_definitions(JSON_HAS_CPP_17 JSON_MultipleHeaders=ON)

if (MSVC)
    add_compile_options(/EHs /MP)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Debug)
endif ()

set(SRC_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src)

file(GLOB MIRAICP_CPP_PATH ${SRC_PATH}/sdk/*.cpp)
file(GLOB MIRAICP_COMMON_PATH ${SRC_PATH}/common/*.cpp)
file(GLOB LOADER_PATH ${SRC_PATH}/libloader/*.cpp)
file(GLOB_RECURSE PLUGIN_PATH ${SRC_PATH}/plugin/*.cpp)
file(GLOB INCLUDE_PATH ${CMAKE_SOURCE_DIR}/include)
set(
        3RD_PATH
        ${CMAKE_CURRENT_SOURCE_DIR}/3rd_include/
        ${CMAKE_CURRENT_SOURCE_DIR}/3rd_include/json
        ${CMAKE_CURRENT_SOURCE_DIR}/3rd_include/json/nlohmann
        ${CMAKE_CURRENT_SOURCE_DIR}/3rd_include/utf8
        ${CMAKE_CURRENT_SOURCE_DIR}/3rd_include/utf8/utf8
)

# -- jni required --
set(JAVA_AWT_LIBRARY NotNeeded)
set(JAVA_AWT_INCLUDE_PATH NotNeeded)
find_package(JNI REQUIRED)
if (JNI_FOUND)
    message(STATUS "FOUND JNI IN ${JAVA_INCLUDE_PATH}")
    set(
            JNI_PATH
            ${JAVA_INCLUDE_PATH}
            ${JAVA_INCLUDE_PATH2}
    )
else ()
    message(STATUS "Cannot find JNI")
endif ()
# -- end --

# -- miraicp plugin --
add_library(
        MiraiCP_plugin
        SHARED
        ${PLUGIN_PATH}
        ${MIRAICP_CPP_PATH}
        ${MIRAICP_COMMON_PATH}
)
set_target_properties(
        MiraiCP_plugin PROPERTIES
        PREFIX lib
        OUTPUT_NAME MyMiraiCPPlugin
)
target_include_directories(
        MiraiCP_plugin PUBLIC
        ${INCLUDE_PATH}/sdk
        ${INCLUDE_PATH}/common
        ${SRC_PATH}/common
        ${SRC_PATH}/sdk
        ${3RD_PATH}
)
target_compile_definitions(MiraiCP_plugin PUBLIC MIRAICP_LIB_SDK)
target_compile_options(MiraiCP_plugin PUBLIC -Wall)
# -- end --

# -- MiraiCP libLoader --
add_library(
        Loader
        SHARED
        ${LOADER_PATH}
        ${MIRAICP_COMMON_PATH}
)
set_target_properties(
        Loader PROPERTIES
        PREFIX lib
        OUTPUT_NAME Loader
)
target_include_directories(
        Loader PUBLIC
        ${JNI_PATH}
        ${3RD_PATH}
        ${INCLUDE_PATH}/libloader
        ${INCLUDE_PATH}/common
        ${SRC_PATH}/common
        ${SRC_PATH}/libloader
)

add_dependencies(Loader MiraiCP_plugin)
target_compile_definitions(Loader PUBLIC MIRAICP_LIB_LOADER)
if (MSVC)
    target_compile_options(Loader PUBLIC /utf8 /EHs /MP)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Debug)
endif ()

# 移植性
set_target_properties(Loader PROPERTIES LINK_SEARCH_START_STATIC 1)
set_target_properties(Loader PROPERTIES LINK_SEARCH_END_STATIC 1)
if (WIN32)
    if (MSVC)
        target_compile_options(Loader PUBLIC /MT)
    else ()
        target_link_libraries(Loader PUBLIC -static)
    endif (MSVC)
endif (WIN32)
if (UNIX)
    target_link_libraries(Loader -static-libstdc++ -static-libgcc)
endif (UNIX)
# -- end --
