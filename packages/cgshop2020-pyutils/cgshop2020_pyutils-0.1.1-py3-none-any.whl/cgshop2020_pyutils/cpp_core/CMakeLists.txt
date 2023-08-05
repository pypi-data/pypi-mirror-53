cmake_minimum_required(VERSION 3.6)
project(cgshop2020_verifier CXX)

set(CMAKE_CXX_STANDARD 14) # C++ 2014
set(CGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE On) # Silence CGAL warning

# We only need boost thread if CGAL needs/uses it.
# Provide an option to not link against it.
option(CGSHOP2020_NO_BOOST_THREAD "Do NOT link against Boost thread (works with C++11 and later). Defaults to OFF, meaning linking against Boost thread." Off)

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall") # Enable all warnings for compilers supporting -Wall
endif()

# add our include directory to header search paths
include_directories("${CMAKE_CURRENT_LIST_DIR}/include")


# find libraries
find_package(CGAL REQUIRED COMPONENTS Core)
set(THIRD_PARTY_LIBS CGAL::CGAL CGAL::CGAL_Core)

if(NOT CGSHOP2020_NO_BOOST_THREAD)
	find_package(Boost REQUIRED COMPONENTS thread)
	set(THIRD_PARTY_LIBS ${THIRD_PARTY_LIBS} Boost::thread)
else()
	find_package(Boost REQUIRED)
	set(THIRD_PARTY_LIBS ${THIRD_PARTY_LIBS} Boost::boost)
endif()

# function for setting up properties on our static/shared library targets
function(set_visibility TARGET)
	set_target_properties(${TARGET} PROPERTIES
		C_VISIBILITY_PRESET hidden
		CXX_VISIBILITY_PRESET hidden
		VISIBILITY_INLINES_HIDDEN On)

	if(WIN32 AND CGSHOP2020_NO_BOOST_THREAD)
		target_compile_definitions(${TARGET} PRIVATE "-DBOOST_ALL_NO_LIB=1")
	endif()
endfunction()

# include source directory (contains library target)
add_subdirectory("src")
add_subdirectory("unit_tests")
add_subdirectory("python_interface")
add_subdirectory("trivial_triangulation_solver")