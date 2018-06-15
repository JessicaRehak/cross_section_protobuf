cmake_minimum_required(VERSION 3.7)
set (CMAKE_CXX_STANDARD 14)
project(xsec_protoc)

set (GCC_COVERAGE_COMPILE_FLAGS "-coverage -fprofile-arcs -ftest-coverage -lprotoc")
set (GCC_COVERAGE_LINK_FLAGS    "-coverage -lgcov")
set (CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}" )
set (CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}" )

file(GLOB_RECURSE sources "src/*.cpp" "src/*.cc")
set(testing_sources ${sources})
list(FILTER sources EXCLUDE REGEX ".(/tests/).")

include(FindProtobuf)
find_package(Protobuf REQUIRED)
enable_testing()
find_package(GTest REQUIRED)
set(GMOCK_BOTH_LIBRARIES "/usr/lib/libgmock.so;/usr/lib/libgmock_main.so")

include_directories(${GTEST_INCLUDE_DIRS}
	${CMAKE_SOURCE_DIR}/inc
	${CMAKE_SOURCE_DIR}/inc/igl
	${Protobuf_INCLUDE_DIRS})

add_executable(xsec ${sources})
add_executable(xsec_test ${testing_sources})

target_compile_definitions(xsec_test PUBLIC -DTEST)

add_test(NAME tests COMMAND xpt_test)

target_link_libraries(xsec
	${Protobuf_LIBRARIES})

target_link_libraries(xsec_test
	${GTEST_BOTH_LIBRARIES}
	${GMOCK_BOTH_LIBRARIES}
	${Protobuf_LIBRARIES})

