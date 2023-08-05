//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_MISSING_VERTEX_CHECKER_H
#define CGSHOP2020_VERIFIER_MISSING_VERTEX_CHECKER_H
#include "base_checker.h"
#include <set>

namespace cgshop2020_verifier {
class MissingVertexChecker : public BaseChecker {
 public:

  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    std::set<Instance::Index> used_vertex_indices = this->collect_vertex_indices(solution);
    for (Instance::Index i = 0; i < instance.size(); ++i) {
      if (used_vertex_indices.count(i) <= 0) {
        return std::make_unique<MissingVertexErrorInformation>(i);
      }
    }
    return {};
  }
 private:
  std::set<Instance::Index> collect_vertex_indices(const Solution &solution) const
  {
    std::set<Instance::Index> indices;
    for (const auto &edge: solution) {
      indices.insert(edge.get_i());
      indices.insert(edge.get_j());
    }
    return indices;
  }
};
}
#endif //CGSHOP2020_VERIFIER_MISSING_VERTEX_CHECKER_H
