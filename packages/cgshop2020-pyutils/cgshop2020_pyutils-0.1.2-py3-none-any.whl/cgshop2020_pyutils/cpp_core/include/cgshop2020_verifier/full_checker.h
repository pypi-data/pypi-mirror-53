//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_FULL_CHECKER_H
#define CGSHOP2020_VERIFIER_FULL_CHECKER_H

#include "base_checker.h"
#include "loop_edge_checker.h"
#include "index_range_checker.h"
#include "missing_vertex_checker.h"
#include "intersections.h"
#include "double_edge_checker.h"
#include "face_checker.h"
namespace cgshop2020_verifier {

class SolutionChecker: public CheckerPipe {
/// Checks if the solutions fits the instance.
/// This checker pretty fast and should be at the beginning of a checking-chain.
 public:

  SolutionChecker() {
    this->add_checker<LoopEdgeChecker>();
    this->add_checker<IndexRangeChecker>();
    this->add_checker<DoubleEdgeChecker>();
    this->add_checker<MissingVertexChecker>();
    this->add_checker<IntersectionChecker>();
    face_checker = &this->add_checker<FaceChecker>();
  }

 private:
  FaceChecker* face_checker;
};
} // namespace cgshop2020_verifier
#endif //CGSHOP2020_VERIFIER_FULL_CHECKER_H
