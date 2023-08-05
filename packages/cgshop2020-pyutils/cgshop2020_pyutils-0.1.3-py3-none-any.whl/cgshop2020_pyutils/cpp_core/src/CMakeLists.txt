add_library(cgshop2020_verifier
	instance.cpp solution.cpp
	intersections.cpp face_checker.cpp
	error_information.cpp
	../include/cgshop2020_verifier/error_informations.h
	../include/cgshop2020_verifier/double_edge_checker.h
	../include/cgshop2020_verifier/base_checker.h
	../include/cgshop2020_verifier/index_range_checker.h
	../include/cgshop2020_verifier/missing_vertex_checker.h
	../include/cgshop2020_verifier/loop_edge_checker.h
	../include/cgshop2020_verifier/full_checker.h)

target_link_libraries(cgshop2020_verifier ${THIRD_PARTY_LIBS})
set_visibility(cgshop2020_verifier)
set_target_properties(cgshop2020_verifier PROPERTIES POSITION_INDEPENDENT_CODE On)
