//
// Created by Dominik Krupke on 19.09.19.
//

#include <cgshop2020_verifier/solution_fits_instance.h>
#include <cgshop2020_verifier/full_checker.h>
#include "catch.hpp"

TEST_CASE("Testing SolutionFitsInstanceChecker on some simple cases.", "[SolutionFitsInstance]")
{
  using namespace cgshop2020_verifier;
  SECTION("Giving SolutionFitsInstanceChecker a simple feasible solution for a simple instance.") {
    SolutionChecker sfic;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(2, 3);
    solution.add_edge(3, 0);
    auto error = sfic(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(!is_error);
    REQUIRE(*sfic.get_objective() == 1);
  }

  SECTION("Giving SolutionFitsInstanceChecker a solution that misses a vertex.") {
    SolutionFitsInstanceChecker sfic;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    auto error = sfic(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<MissingVertexErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->missing_vertex_index == 3);
  }

  SECTION("Giving SolutionFitsInstanceChecker a solution with a loop edge.") {
    SolutionFitsInstanceChecker sfic;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(2, 2);
    solution.add_edge(2, 3);
    solution.add_edge(3, 0);
    auto error = sfic(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<LoopEdgeErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->loop_edge == Solution::Edge{2, 2});
  }

  SECTION("Giving SolutionFitsInstanceChecker a solution with an index out of range.") {
    SolutionFitsInstanceChecker sfic;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(1, 4);
    auto error = sfic(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<BadVertexErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->bad_vertex_idx == 4);
  }

  SECTION("Giving SolutionFitsInstanceChecker a solution with an edge used multiple times.") {
    SolutionFitsInstanceChecker sfic;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(2, 3);
    solution.add_edge(1, 2);
    solution.add_edge(3, 0);
    auto error = sfic(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<DoubleUsageErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->doubly_used_edge == Solution::Edge{1, 2});
  }
}