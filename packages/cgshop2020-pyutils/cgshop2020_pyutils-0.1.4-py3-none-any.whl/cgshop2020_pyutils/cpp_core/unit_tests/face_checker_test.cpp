//
// Created by Phillip Keldenich on 2019-09-19.
//

#include <cgshop2020_verifier/face_checker.h>
#include "catch.hpp"

TEST_CASE("FaceChecker on basic instance", "[FaceChecker]") {
  using namespace cgshop2020_verifier;
  cgshop2020_verifier::FaceChecker checker;
  cgshop2020_verifier::Instance instance;
  cgshop2020_verifier::Solution solution;
  instance.add_points({{0.5,1.0}, {1.5,1.0}, {0.0,0.0}, {1.0,0.5}, {2.0,0.0}, {1.0,-1.0}});

  SECTION("Correct solution") {
    solution.add_edges({{0, 2}, {0, 3}, {0, 1}, {2, 5}, {3, 5}, {3, 4}, {4, 5}, {1, 4}});
    auto error = checker(instance, solution);
    bool is_error = error && error->is_error();
    REQUIRE(!is_error);
    REQUIRE(*checker.get_objective() == 3);
  }

  SECTION("Non-convex inner face") {
    solution.add_edges({{0, 2}, {0, 1}, {2, 5}, {3, 5}, {3, 4}, {4, 5}, {1, 4}});
    auto error = checker(instance, solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);

    auto *my_error = dynamic_cast<NonConvexBoundedFaceErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->get_problematic_point_index() == 3);
  }

  SECTION("Non-convex outer face") {
    solution.add_edges({{2, 3}, {3, 5}, {2, 5}, {0, 3}, {3, 4}, {1, 4}, {0, 1}});
    auto error = checker(instance, solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);

    auto *my_error = dynamic_cast<NonConvexOuterBoundaryErrorInformation *>(error.get());
    REQUIRE(my_error);
    REQUIRE(my_error->get_problematic_point_index() == 3);
  }

  SECTION("Disconnected outer boundary") {
    solution.add_edges({{0, 2}, {2, 5}, {5, 0}, {1, 3}, {3, 4}, {4, 1}});
    auto in_component_1 = [] (auto index) { return index == 0 || index == 2 || index == 5; };
    auto in_component_2 = [] (auto index) { return index == 1 || index == 3 || index == 4; };

    auto error = checker(instance, solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);

    auto *my_error = dynamic_cast<DisconnectedOuterBoundaryErrorInformation *>(error.get());
    REQUIRE(my_error);
    auto disconnected = my_error->get_disconnected_pair();
    REQUIRE(((in_component_1(disconnected.first) && in_component_2(disconnected.second)) ||
            (in_component_2(disconnected.first) && in_component_1(disconnected.second))));
  }

  SECTION("Non-empty inner face") {
    instance.add_points({{1.1,0.6}, {1.1,0.4}});
    solution.add_edges({{0, 1}, {1, 4}, {4, 5}, {5, 2}, {2, 0}, {3, 6}, {6, 7}, {7, 3}});
    auto in_outer_component = [] (auto index) {
      return index == 0 || index == 1 || index == 2 || index == 4 || index == 5;
    };
    auto in_inner_component = [] (auto index) {
      return index == 3 || index == 6 || index == 7;
    };

    auto error = checker(instance, solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);

    auto *my_error = dynamic_cast<VertexWithinBoundedFaceErrorInformation *>(error.get());
    REQUIRE(my_error);

    REQUIRE(in_inner_component(my_error->get_contained_point()));
    REQUIRE(in_outer_component(my_error->get_containing_face_point()));
  }
}
