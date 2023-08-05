//
// Created by Dominik Krupke on 2019-09-13.
//

#ifndef CPP_CGAL_H
#define CPP_CGAL_H

#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <cstdint>
#include <utility>

namespace cgshop2020_verifier {
namespace cgal {
using Kernel = CGAL::Exact_predicates_exact_constructions_kernel;
using Point = Kernel::Point_2;
using Segment = Kernel::Segment_2;
using Number = Kernel::FT;
using Integer = std::int64_t;
}
}

#endif //CPP_CGAL_H
