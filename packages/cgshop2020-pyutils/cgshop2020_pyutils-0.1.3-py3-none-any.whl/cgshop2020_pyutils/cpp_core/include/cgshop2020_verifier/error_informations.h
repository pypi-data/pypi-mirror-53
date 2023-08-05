//
// Created by Dominik Krupke on 19.09.19.
//

#ifndef CGSHOP2020_VERIFIER_ERROR_INFORMATIONS_H
#define CGSHOP2020_VERIFIER_ERROR_INFORMATIONS_H
#include <string>
#include <iostream>
#include "solution.h"
namespace cgshop2020_verifier {
class ErrorInformation {
 public:
  virtual bool is_error() const { return true; }
  virtual std::string get_error_name() const { return "UNDEFINED_ERROR"; };
  virtual std::string get_error_explanation() const { return ""; };
  virtual ~ErrorInformation() = default;
};

class NoError : public ErrorInformation {
 public:
  static std::string ERROR_NAME() { return "NO_ERROR"; }
  bool is_error() const override { return false; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override { return "No error found."; }
};

class DoubleUsageErrorInformation : public ErrorInformation {
 public:
  explicit DoubleUsageErrorInformation(const Solution::Edge &doublyUsedEdge) : doubly_used_edge(doublyUsedEdge) {}
  static std::string ERROR_NAME() { return "DOUBLE_USAGE_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream buf;
    buf << "Edge ("
        << this->doubly_used_edge.get_i()
        << ", "
        << this->doubly_used_edge.get_j()
        << ") is used multiple times by the solution!";
    return buf.str();
  }

  Solution::Edge doubly_used_edge;
};

class MissingVertexErrorInformation : public ErrorInformation {
  /// A vertex is not covered by the solution.
 public:
  explicit MissingVertexErrorInformation(Instance::Index missingVertexIndex)
      : missing_vertex_index(missingVertexIndex) {}
  static std::string ERROR_NAME() { return "MISSING_VERTEX_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream buf;
    buf << "Vertex with index " << this->missing_vertex_index << " is not contained in solution!";
    return buf.str();
  }
  Instance::Index missing_vertex_index;
};

class BadVertexErrorInformation : public ErrorInformation {
  /// Some index that is not contained in the instance is used by some edge
  /// in the solution.
 public:
  explicit BadVertexErrorInformation(Instance::Index badVertexIdx) : bad_vertex_idx(badVertexIdx) {}

  static std::string ERROR_NAME() { return "BAD_VERTEX_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream buf;
    buf << "Vertex with index " << this->bad_vertex_idx << " does not match any point in the instance!";
    return buf.str();
  }
  Instance::Index bad_vertex_idx;
};

class LoopEdgeErrorInformation : public ErrorInformation {
  /// There is a loop edge which is not allowed.
 public:
  explicit LoopEdgeErrorInformation(const Solution::Edge &loopEdge) : loop_edge(loopEdge) {}

  static std::string ERROR_NAME() { return "LOOP_EDGE_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream buf;
    buf << "Solution contains loop edge (" << this->loop_edge.get_i() << ", " << this->loop_edge.get_j() << ")!";
    return buf.str();
  }

 public:
  Solution::Edge loop_edge;
};

class IntersectionErrorInformation : public ErrorInformation {
 public:
  IntersectionErrorInformation(cgal::Point intersectionPoint,
                               std::vector<Solution::Edge> edges)
      : intersection_point(std::move(intersectionPoint)), edges(std::move(edges)) {}

  static std::string ERROR_NAME() { return "INTERSECTION_ERROR"; }
  std::string get_error_name() const override
  {
    return ERROR_NAME();
  }

  std::string get_error_explanation() const override
  {
    std::stringstream msg;
    msg << "There is an intersection at " << this->intersection_point << "! ";
    msg << "The following edges are involved: ";
    for (const auto &edge: this->edges) {
      msg << "(" << edge.get_i() << "," << edge.get_j() << "), ";
    }
    return msg.str();
  }

 public:
  cgal::Point intersection_point;
  std::vector<Solution::Edge> edges;
};

class NonConvexOuterBoundaryErrorInformation : public ErrorInformation {
 public:
  static std::string ERROR_NAME() { return "NON_CONVEX_OUTER_BOUNDARY_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }

  std::string get_error_explanation() const override
  {
    std::stringstream msg;
    msg << "The outer boundary is not convex at point with index "
        << this->get_problematic_point_index() << "!";
    return msg.str();
  }
  explicit NonConvexOuterBoundaryErrorInformation(Instance::Index problem_index) noexcept :
      m_problematic_index(problem_index) {}

  Instance::Index get_problematic_point_index() const noexcept
  {
    return m_problematic_index;
  }

 private:
  Instance::Index m_problematic_index;
};

class DisconnectedOuterBoundaryErrorInformation : public ErrorInformation {
 public:
  static std::string ERROR_NAME() { return "DISCONNECTED_OUTER_BOUNDARY_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream msg;
    msg << "The outer boundary consists of multiple components! "
        << "The point with index " << this->m_component1_point
        << " and " << this->m_component2_point
        << " are in separate components!";
    return msg.str();
  }

  DisconnectedOuterBoundaryErrorInformation(Instance::Index component1, Instance::Index component2) noexcept :
      m_component1_point(component1),
      m_component2_point(component2) {}

  std::pair<Instance::Index, Instance::Index> get_disconnected_pair() const noexcept
  {
    return {m_component1_point, m_component2_point};
  }

 private:
  Instance::Index m_component1_point;
  Instance::Index m_component2_point;
};

class NonConvexBoundedFaceErrorInformation : public ErrorInformation {
 public:
  static std::string ERROR_NAME() { return "NON_CONVEX_BOUNDED_FACE_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  explicit NonConvexBoundedFaceErrorInformation(Instance::Index problem_index) noexcept :
      m_problematic_index(problem_index) {}

  std::string get_error_explanation() const override
  {
    std::stringstream msg;
    msg << "There is a non-convex face at the point with index "
        << this->get_problematic_point_index() << "!";
    return msg.str();
  }

  Instance::Index get_problematic_point_index() const noexcept
  {
    return m_problematic_index;
  }

 private:
  Instance::Index m_problematic_index;
};

class VertexWithinBoundedFaceErrorInformation : public ErrorInformation {
 public:
  static std::string ERROR_NAME() { return "VERTEX_WITHIN_BOUNDED_FACE_ERROR"; }
  std::string get_error_name() const override { return ERROR_NAME(); }
  std::string get_error_explanation() const override
  {
    std::stringstream msg;
    msg << "The point with index " << this->get_contained_point()
        << " is within the face delimited by, e.g., the point with index "
        << this->get_containing_face_point() << "!";
    return msg.str();
  }
  using Index = Instance::Index;

  VertexWithinBoundedFaceErrorInformation(Index containing_face_point, Index contained_point) noexcept :
      m_containing_face_point(containing_face_point),
      m_contained_point(contained_point) {}

  Index get_contained_point() const noexcept
  {
    return m_contained_point;
  }

  Index get_containing_face_point() const noexcept
  {
    return m_containing_face_point;
  }

 private:
  Index m_containing_face_point;
  Index m_contained_point;
};

} // namespace cgshop2020_verifier

std::ostream &operator<<(std::ostream &os, const cgshop2020_verifier::ErrorInformation &errorInformation);

#endif //CGSHOP2020_VERIFIER_ERROR_INFORMATIONS_H
