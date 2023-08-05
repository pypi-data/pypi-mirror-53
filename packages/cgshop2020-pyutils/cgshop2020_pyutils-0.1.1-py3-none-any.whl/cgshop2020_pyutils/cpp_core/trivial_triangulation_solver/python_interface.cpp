//
// Created by Phillip Keldenich on 2019-09-24.
//

#include "solver.h"
#include "symbol_export.h"

extern "C" {
  CGSHOP2020_SOLVER_EXPORTED_SYMBOL
  cgshop2020_verifier::Solution* get_solution_by_triangulation(const cgshop2020_verifier::Instance* instance) noexcept
  {
    cgshop2020_verifier::TrivialTriangulationSolver solver;
    return new cgshop2020_verifier::Solution{solver(*instance)};
  }
}
