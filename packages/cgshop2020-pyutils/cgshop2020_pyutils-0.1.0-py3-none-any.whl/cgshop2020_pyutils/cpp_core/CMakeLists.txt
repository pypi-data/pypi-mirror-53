cmake_minimum_required(VERSION 3.6)
project(cgshop2020_verifier CXX)

set(CMAKE_CXX_STANDARD 14) # C++ 2014
set(CGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE On) # Silence CGAL warning

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall") # Enable all warnings for compilers supporting -Wall
endif()

# add our include directory to header search paths
include_directories("${CMAKE_CURRENT_LIST_DIR}/include")


# find libraries
find_package(CGAL REQUIRED COMPONENTS Core)
find_package(Boost REQUIRED COMPONENTS thread)

# function for setting up properties on our static/shared library targets
function(set_visibility TARGET)
	set_target_properties(${TARGET} PROPERTIES
		C_VISIBILITY_PRESET hidden
		CXX_VISIBILITY_PRESET hidden
		VISIBILITY_INLINES_HIDDEN On)
endfunction()

# include source directory (contains library target)
add_subdirectory("src")
add_subdirectory("unit_tests")
add_subdirectory("python_interface")
add_subdirectory("trivial_triangulation_solver")