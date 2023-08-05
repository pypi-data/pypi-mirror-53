//
// Created by Phillip Keldenich on 2019-09-17.
//

#ifndef CGSHOP2020_VERIFIER_POINT_HASH_H
#define CGSHOP2020_VERIFIER_POINT_HASH_H

#include "cgshop2020_verifier/instance.h"

namespace cgshop2020_verifier {
  struct PointHash {
    std::size_t operator()(const Instance::Point& point) const noexcept {
      double x = CGAL::to_double(point.x());
      double y = CGAL::to_double(point.y());
      std::size_t h = 13;
      boost::hash_combine(h, std::hash<double>{}(x));
      boost::hash_combine(h, std::hash<double>{}(y));
      return h;
    }
  };
}

#endif //CGSHOP2020_VERIFIER_POINT_HASH_H
