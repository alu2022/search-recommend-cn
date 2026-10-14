cmake_minimum_required(VERSION 3.10)
project(search_recommend_cn CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Step 2 will add the indexer / searcher targets here, for example:
#   add_executable(indexer src/indexer.cpp)
#   add_executable(searcher src/searcher.cpp)
#
# Keep this file so `cmake -S cpp -B build` already has a valid project.
add_custom_target(placeholder COMMENT "C++ indexer/searcher will be added in step 2")
