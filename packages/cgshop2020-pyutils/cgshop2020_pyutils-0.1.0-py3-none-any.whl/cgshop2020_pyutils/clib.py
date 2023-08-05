"""
This file contains stuff needed to use the C++-cores.
It is to some degree ugly hackery, so be warned.
"""

import ctypes
import os
import subprocess
import platform

__CPP_CORE_SUPPORTED = True


def is_cgal_cpp_core_supported():
    return __CPP_CORE_SUPPORTED


def disable_cgal_cpp_support():
    print("Disabling C++ CGAL features.")
    print("You cannot use the verification functionality or TrivialTriangulationSolver.")
    print("Some other functionality such as parsing is replaced by pure Python.")
    global __CPP_CORE_SUPPORTED
    __CPP_CORE_SUPPORTED = False


# root folders of binaries
__here = os.path.dirname(os.path.realpath(__file__))
__cpp_core_folder = os.path.join(__here, "cpp_core")
cmake_bin = os.path.join(__cpp_core_folder, "bin", "python_interface")
precompiled_bin = os.path.join(__cpp_core_folder, "binaries")

# system specific paths to lib
__paths = {
    "Linux": [
        os.path.join(cmake_bin, "libcgshop2020_verifier_module.so"),
        os.path.join(precompiled_bin, "linux-x86_64", "libcgshop2020_verifier_module.so")
    ],
    "Darwin": [
        os.path.join(cmake_bin, "libcgshop2020_verifier_module.so"),
        os.path.join(precompiled_bin, "osx", "libcgshop2020_verifier_module.so")
    ],
    "Windows": [
        os.path.join(cmake_bin, "libcgshop2020_verifier_module.dll"),
        os.path.join(precompiled_bin, "osx", "libcgshop2020_verifier_module.dll")
    ]
}


def try_to_load_clib(paths):
    os_name = platform.system()
    if os_name not in paths:
        print("Your platform", os_name, "does not seem to be supported, yet.")
        return None
    for path in paths[os_name]:
        try:
            if os.path.exists(path):
                lib = ctypes.cdll.LoadLibrary(path)
                # print("Using C++-module from", path)
                return lib
        except OSError as ose:
            pass
    return None


def compile_cpp_core():
    print("Compiling the C++ core.")
    print("You need to have CMake, a C++ compiler, CGAL and Boost installed.")
    source_folder = os.path.join(__here, "cpp_core")
    bin_folder = os.path.join(source_folder, "bin")
    cmake_cmd_1 = "cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -S " + str(
        source_folder) + " -B " + str(bin_folder)
    cmake_cmd_2 = "cmake --build " + str(
        bin_folder) + " --target cgshop2020_verifier_module --config RelWithDebInfo"
    cmake_cmd_3 = "cmake --build " + str(
        bin_folder) + " --target cgshop2020_trivial_triangulation_solver_module --config RelWithDebInfo"
    try:
        ret_code = subprocess.check_call(cmake_cmd_1, stderr=subprocess.STDOUT,
                                         shell=True)
        ret_code = subprocess.check_call(cmake_cmd_2, stderr=subprocess.STDOUT,
                                         shell=True)
        ret_code = subprocess.check_call(cmake_cmd_3, stderr=subprocess.STDOUT,
                                         shell=True)
        print("You have to reload the module for the new c++-core to be loaded.")
    except subprocess.CalledProcessError as cpe:
        print(cpe)


_CLIB = try_to_load_clib(__paths)
if _CLIB:
    print("Enabled C++ CGAL support. You should have full functionality.")
else:
    disable_cgal_cpp_support()
