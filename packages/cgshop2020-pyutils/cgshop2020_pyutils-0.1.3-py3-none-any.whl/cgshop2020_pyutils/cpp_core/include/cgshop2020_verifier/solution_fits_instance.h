//
// Created by Dominik Krupke on 2019-09-17.
//

#ifndef MIN_CONVEX_PARTITION_VERIFIER_COMPLETENESS_H
#define MIN_CONVEX_PARTITION_VERIFIER_COMPLETENESS_H
#include <algorithm>
#include "cgshop2020_verifier/solution.h"
#include "cgshop2020_verifier/instance.h"
#include "error_informations.h"
#include "base_checker.h"
#include "loop_edge_checker.h"
#include "index_range_checker.h"
#include "double_edge_checker.h"
#include "missing_vertex_checker.h"

namespace cgshop2020_verifier {

class SolutionFitsInstanceChecker: public CheckerPipe {
/// Checks if the solutions fits the instance.
/// This checker pretty fast and should be at the beginning of a checking-chain.
public:

SolutionFitsInstanceChecker() {
  this->add_checker<LoopEdgeChecker>();
  this->add_checker<IndexRangeChecker>();
  this->add_checker<DoubleEdgeChecker>();
  this->add_checker<MissingVertexChecker>();
}
};
} // namespace cgshop2020_verifier

#endif //MIN_CONVEX_PARTITION_VERIFIER_COMPLETENESS_H
