//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_DOUBLE_EDGE_CHECKER_H
#define CGSHOP2020_VERIFIER_DOUBLE_EDGE_CHECKER_H

#include "base_checker.h"
namespace cgshop2020_verifier {
class DoubleEdgeChecker: public BaseChecker {
 public:
  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    std::vector<Solution::Edge> edges{solution.begin(), solution.end()};
    std::sort(edges.begin(), edges.end());
    auto pos = std::adjacent_find(edges.begin(), edges.end());
    if (pos != edges.end()) {
      return std::make_unique<DoubleUsageErrorInformation>(*pos);
    }
    return std::unique_ptr<ErrorInformation>();
  }
};
}

#endif //CGSHOP2020_VERIFIER_DOUBLE_EDGE_CHECKER_H
