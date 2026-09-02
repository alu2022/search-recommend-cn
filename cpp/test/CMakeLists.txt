cmake_minimum_required(VERSION 3.10)
project(add3 CXX C)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# 基础编译选项（保持原有）
add_compile_options(-fPIC)

# 定义输出根目录（bin）
set(OUTPUT_ROOT_DIR "${PROJECT_BINARY_DIR}/bin")
# 定义库输出目录：bin/lib
set(LIB_OUTPUT_DIR "${OUTPUT_ROOT_DIR}/lib")
# 定义头文件输出目录：bin/include
set(INCLUDE_OUTPUT_DIR "${OUTPUT_ROOT_DIR}/include")

# 1. 创建动态库（保持原有源码）
add_library(${PROJECT_NAME} SHARED 
    src/add3.cpp
)

# 2. 设置库的输出路径到 bin/lib，同时规范 SONAME（避免之前的依赖问题）
set_target_properties(${PROJECT_NAME} PROPERTIES 
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    # 核心修改：库输出到 bin/lib
    LIBRARY_OUTPUT_DIRECTORY "${LIB_OUTPUT_DIR}"
    # 可选：规范库名（生成 libadd3.so，符合Linux标准）
    OUTPUT_NAME "add3"
    # 可选：设置SONAME版本（如需要带版本号，可加这行）
    # SOVERSION 1
)

# 3. 复制头文件到 bin/include（编译时自动执行）
# 先创建 include 目录（避免目录不存在）
file(MAKE_DIRECTORY "${INCLUDE_OUTPUT_DIR}")
# 复制 include 目录下的所有头文件到 bin/include
file(COPY 
    ${CMAKE_CURRENT_SOURCE_DIR}/src/  # 源目录（你的头文件所在）
    DESTINATION "${INCLUDE_OUTPUT_DIR}"   # 目标目录
    FILES_MATCHING PATTERN "*.h"          # 只复制 .h 头文件
)

# 4. 头文件目录配置（保持原有，供链接时使用）
target_include_directories(${PROJECT_NAME} PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}/include  # 源码头文件目录
    ${INCLUDE_OUTPUT_DIR}                # 复制后的头文件目录（可选，冗余但兼容）
)