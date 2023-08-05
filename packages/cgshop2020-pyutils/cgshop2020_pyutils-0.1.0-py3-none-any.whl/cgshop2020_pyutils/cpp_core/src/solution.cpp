//
// Created by Dominik Krupke on 2019-09-13.
//

#include "cgshop2020_verifier/solution.h"

void cgshop2020_verifier::Solution::make_unique() noexcept {
  std::sort(edges.begin(), edges.end());
  edges.erase(std::unique(edges.begin(), edges.end()), edges.end());
}
