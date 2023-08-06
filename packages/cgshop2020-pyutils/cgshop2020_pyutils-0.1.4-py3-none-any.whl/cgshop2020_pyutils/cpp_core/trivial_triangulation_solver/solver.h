//
// Created by Phillip Keldenich on 2019-09-24.
//

#ifndef CGSHOP2020_VERIFIER_SOLVER_H
#define CGSHOP2020_VERIFIER_SOLVER_H

#include "cgshop2020_verifier/cgal.h"
#include "cgshop2020_verifier/instance.h"
#include "cgshop2020_verifier/solution.h"

namespace cgshop2020_verifier {
  class TrivialTriangulationSolver {
   public:
    Solution operator()(const Instance& instance);
  };
}

#endif //CGSHOP2020_VERIFIER_SOLVER_H
