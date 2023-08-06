//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_INDEX_RANGE_CHECKER_H
#define CGSHOP2020_VERIFIER_INDEX_RANGE_CHECKER_H

#include "base_checker.h"
namespace cgshop2020_verifier {
class IndexRangeChecker : public BaseChecker {
 public:
  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    for (const auto &edge: solution) {
      if (!this->is_index_in_range(instance, edge.get_i())) {
        return std::make_unique<BadVertexErrorInformation>(edge.get_i());
      }
      if (!this->is_index_in_range(instance, edge.get_j())) {
        return std::make_unique<BadVertexErrorInformation>(edge.get_j());
      }
    }
    return std::unique_ptr<ErrorInformation>();
  }

 private:
  bool is_index_in_range(Instance &instance, Instance::Index index) const
  {
    return 0 <= index && index < instance.size();
  }
};
}

#endif //CGSHOP2020_VERIFIER_INDEX_RANGE_CHECKER_H
