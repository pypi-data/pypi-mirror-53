//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_LOOP_EDGE_CHECKER_H
#define CGSHOP2020_VERIFIER_LOOP_EDGE_CHECKER_H

#include "base_checker.h"
namespace cgshop2020_verifier {
class LoopEdgeChecker : public BaseChecker {
  /// Make sure that there are no loop edges in the solution.
  /// We could prohibit this in the solution class but checking foreign
  /// solutions would be more difficult because then there could be an error
  /// during instance creation and during checking. This way, only the checker
  /// will raise an error.
 public:
  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    for (const auto &edge: solution) {
      if (edge.get_i() == edge.get_j()) {
        return std::make_unique<LoopEdgeErrorInformation>(edge);
      }
    }
    return std::unique_ptr<ErrorInformation>();
  }
};
}

#endif //CGSHOP2020_VERIFIER_LOOP_EDGE_CHECKER_H
