//
// Created by Dominik Krupke on 19.09.19.
//

#include <cgshop2020_verifier/intersections.h>
#include "catch.hpp"

using namespace cgshop2020_verifier;
TEST_CASE("Testing IntersectionChecker on some simple cases.", "[IntersectionChecker]")
{
  SECTION("Giving IntersectionChecker a good solution.") {
    IntersectionChecker checker;
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
    auto error = checker( /*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(!is_error);
  }

  SECTION("Giving IntersectionChecker an instance with a classic intersection") {
    IntersectionChecker checker;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 3);
    solution.add_edge(3, 2);
    solution.add_edge(2, 0);
    auto error = checker(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<IntersectionErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->intersection_point == cgal::Point{0.5, 0.5});
    REQUIRE(my_error->edges.size() == 2);
  }

  SECTION("Giving IntersectionChecker an instance with a point on a segment") {
    IntersectionChecker checker;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    instance.add_point(2.0, 0.0);
    Solution solution;
    solution.add_edge(0, 4);
    solution.add_edge(1, 3);
    solution.add_edge(3, 2);
    solution.add_edge(2, 0);
    auto error = checker(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<IntersectionErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->edges.size() == 2);
  }

  SECTION("Giving IntersectionChecker an instance with an overlapping segment") {
    IntersectionChecker checker;
    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    instance.add_point(2.0, 0.0);
    Solution solution;
    solution.add_edge(0, 4);
    solution.add_edge(3, 2);
    solution.add_edge(2, 0);
    solution.add_edge(4, 1);
    auto error = checker(/*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    auto *my_error = dynamic_cast<IntersectionErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->edges.size() == 2);
  }
}