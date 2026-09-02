cmake_minimum_required(VERSION 3.10)
project(test CXX C)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

add_executable(${PROJECT_NAME} 
    src/main.cpp 
    src/add.cpp
)
target_include_directories(${PROJECT_NAME} 
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/add3/include  # 第三方库头文件（仅自身用）
)

target_link_directories(${PROJECT_NAME} 
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/add3/lib  # add3.so 所在目录
)
target_link_libraries(${PROJECT_NAME} 
    PRIVATE add3
)