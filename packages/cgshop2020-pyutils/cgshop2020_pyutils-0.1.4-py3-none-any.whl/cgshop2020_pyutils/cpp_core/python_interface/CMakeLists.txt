# extra source files only for the verifier module (C API for use in python)
set(MODULE_SOURCES symbol_export.h python_interface.cpp)

add_library(cgshop2020_verifier_module MODULE ${MODULE_SOURCES})
set_visibility(cgshop2020_verifier_module)
target_link_libraries(cgshop2020_verifier_module cgshop2020_verifier ${THIRD_PARTY_LIBS})
