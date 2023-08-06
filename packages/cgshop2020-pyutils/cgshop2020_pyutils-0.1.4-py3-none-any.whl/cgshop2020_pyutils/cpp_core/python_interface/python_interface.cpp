//
// Created by Phillip Keldenich on 2019-09-23.
//

#include "symbol_export.h"
#include "cgshop2020_verifier/solution.h"
#include "cgshop2020_verifier/instance.h"
#include "cgshop2020_verifier/full_checker.h"
#include <cstddef>
#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <algorithm>

using Index = cgshop2020_verifier::Instance::Index;

extern "C" {
  struct Point {
    double x;
    double y;
  };

  struct Edge {
    std::uint64_t i;
    std::uint64_t j;
  };

  // we mark these functions noexcept so that no exceptions can escape into C-land or the python interpreter;
  // exceptions should only occur on programming errors or out-of-memory conditions that we cannot handle.
  // this way, any exception escaping trigger std::terminate instead.
  CGSHOP2020_EXPORTED_SYMBOL cgshop2020_verifier::Solution* new_solution() noexcept {
    return new cgshop2020_verifier::Solution{};
  }

  CGSHOP2020_EXPORTED_SYMBOL cgshop2020_verifier::Instance* new_instance() noexcept {
    return new cgshop2020_verifier::Instance{};
  }

  CGSHOP2020_EXPORTED_SYMBOL void delete_solution(cgshop2020_verifier::Solution* solution) noexcept {
    delete solution;
  }

  CGSHOP2020_EXPORTED_SYMBOL void delete_instance(cgshop2020_verifier::Instance* instance) noexcept {
    delete instance;
  }

  CGSHOP2020_EXPORTED_SYMBOL std::uint64_t add_point_to_instance(cgshop2020_verifier::Instance* instance,
                                                               double x, double y) noexcept
  {
    return instance->add_point(x, y);
  }

  CGSHOP2020_EXPORTED_SYMBOL void add_edge_to_solution(cgshop2020_verifier::Solution* solution,
                                                       std::uint64_t p1, std::uint64_t p2)
  {
    solution->add_edge(Index{p1}, Index{p2});
  }

  CGSHOP2020_EXPORTED_SYMBOL std::uint64_t num_edges_in_solution(const cgshop2020_verifier::Solution* solution) noexcept {
    return solution->size();
  }

  CGSHOP2020_EXPORTED_SYMBOL std::uint64_t num_points_in_instance(const cgshop2020_verifier::Instance* instance) noexcept {
    return instance->size();
  }

  CGSHOP2020_EXPORTED_SYMBOL Point get_point_of_instance(const cgshop2020_verifier::Instance* instance,
                                                         std::uint64_t index) noexcept
  {
    const auto& p = instance->at(Index{index});
    return {CGAL::to_double(p.x()), CGAL::to_double(p.y())};
  }

  CGSHOP2020_EXPORTED_SYMBOL Edge get_edge_of_solution(const cgshop2020_verifier::Solution* solution,
                                                       std::uint64_t index) noexcept
  {
    const auto& e = solution->at(Index{index});
    return {e.get_i(), e.get_j()};
  }

  struct VerificationResult {
    const char* message;
    std::int64_t objective;
  };

  static const char* const empty_error_str = "";

  static char* message_from_error(const cgshop2020_verifier::ErrorInformation& err) {
    std::string errmsg = err.get_error_explanation();
    auto len = errmsg.length();
    char* buffer = new char[len + 1];
    std::copy_n(errmsg.begin(), len, buffer);
    buffer[len] = '\0';
    return buffer;
  }

  CGSHOP2020_EXPORTED_SYMBOL void VerificationResult_destructor(VerificationResult *r) noexcept {
    if(r->message != empty_error_str) {
      delete[] r->message;
    }
  }

  CGSHOP2020_EXPORTED_SYMBOL VerificationResult check_solution(cgshop2020_verifier::Solution* solution,
                                                               cgshop2020_verifier::Instance* instance) noexcept
  {
    cgshop2020_verifier::SolutionChecker checker;
    auto result = checker(*instance, *solution);
    if(result) {
      return VerificationResult{message_from_error(*result), -1};
    } else {
      return VerificationResult{empty_error_str, *checker.get_objective()};
    }
  }

  CGSHOP2020_EXPORTED_SYMBOL void make_solution_unique(cgshop2020_verifier::Solution* solution) noexcept {
    solution->make_unique();
  }
}
