cmake_minimum_required(VERSION 3.10)
# 以utf8编译, for msvc
add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
project(MiraiCP_debug LANGUAGES CXX)
set(SRC_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src)


file(GLOB MIRAICP_CPP_PATH ${SRC_PATH}/include/*.cpp)
file(GLOB MIRAICP_COMMON_PATH ${SRC_PATH}/common/*.cpp)
file(GLOB LOADER_PATH ${SRC_PATH}/libloader/*.cpp)
file(GLOB PLUGIN_PATH ${SRC_PATH}/plugin/*.cpp)
set(3RD_PATH
    ${SRC_PATH}/3rd_include/
    ${SRC_PATH}/3rd_include/utf8
    ${SRC_PATH}/3rd_include/utf8/utf8
)


# -- jni required --
set(JAVA_AWT_LIBRARY NotNeeded)
#set(JAVA_JVM_LIBRARY NotNeeded)
set(JAVA_AWT_INCLUDE_PATH NotNeeded)
find_package(JNI REQUIRED)
if (JNI_FOUND)
    message(STATUS "FOUND JNI IN ${JAVA_INCLUDE_PATH}")
    set(JNI_PATH
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
set_target_properties(MiraiCP_plugin PROPERTIES
        PREFIX lib
        OUTPUT_NAME MyMiraiCPPlugin)
target_include_directories(MiraiCP_plugin PUBLIC
        ${SRC_PATH}/include
        ${SRC_PATH}/common
        ${3RD_PATH}
        )
target_compile_options(MiraiCP_plugin PUBLIC -Wall)
# -- end --


# -- MiraiCP libLoader --
add_library(Loader
        SHARED
        ${LOADER_PATH}
        ${MIRAICP_COMMON_PATH}
        )
target_include_directories(Loader PUBLIC
        ${JNI_PATH}
        ${3RD_PATH}
        ${SRC_PATH}/include
        ${SRC_PATH}/common
        ${SRC_PATH}
        )
target_compile_options(Loader PUBLIC -DMIRAICP_LIB_LOADER)
if (UNIX)
    target_compile_options(Loader PUBLIC -rdynamic)
endif (UNIX)
# -- end --
