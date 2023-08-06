//
// Created by Dominik Krupke on 2019-09-13.
//

#ifndef MIN_CONVEX_PARTITION_VERIFIER_INSTANCE_H
#define MIN_CONVEX_PARTITION_VERIFIER_INSTANCE_H
#include <cstddef>
#include <vector>
#include <initializer_list>
#include <iterator>
#include "cgal.h"

namespace cgshop2020_verifier {
class Instance {
 public:
  using Point = cgshop2020_verifier::cgal::Point;
  using Index = std::size_t;
  using NumberType = double;

  Index add_point(NumberType x, NumberType y)
  {
    auto id = points.size();
    points.emplace_back(x, y);
    return id;
  }

  void add_points(std::initializer_list<std::pair<double,double>> points) {
    for(auto p : points) {
      this->add_point(p.first, p.second);
    }
  }

  const Point& at(Index index) const
  {
    return points.at(index);
  }

  size_t size() const
  {
    return points.size();
  }

  auto begin() const noexcept {
    return points.begin();
  }

  auto end() const noexcept {
    return points.end();
  }

 private:
  std::vector<Point> points;
};
}

#endif //MIN_CONVEX_PARTITION_VERIFIER_INSTANCE_H
