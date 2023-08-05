//
// Created by Phillip Keldenich on 2019-09-23.
//

#ifndef CGSHOP2020_VERIFIER_SYMBOL_EXPORT_H
#define CGSHOP2020_VERIFIER_SYMBOL_EXPORT_H

// handle export (and theoretically, import) of symbols
#if defined(_WIN32) || defined(__WIN32__)

// use declspec(dllexport) on Windows
#ifdef cgshop2020_verifier_module_EXPORTS // this is defined by cmake when building the shared lib
#define CGSHOP2020_EXPORTED_SYMBOL __declspec(dllexport)
#else
#define CGSHOP2020_EXPORTED_SYMBOL __declspec(dllimport)
#endif

#elif defined(__GNUC__) && __GNUC__ >= 4

// for reasonable GCC/clang versions on Unix, use the visibility attribute
#define CGSHOP2020_EXPORTED_SYMBOL  __attribute__((__visibility__ ("default")))

#else
#define CGSHOP2020_EXPORTED_SYMBOL
#endif

#endif //CGSHOP2020_VERIFIER_SYMBOL_EXPORT_H
