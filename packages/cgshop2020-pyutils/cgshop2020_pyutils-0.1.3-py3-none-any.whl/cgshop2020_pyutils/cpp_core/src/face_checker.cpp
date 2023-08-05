//
// Created by Dominik Krupke on 2019-09-17.
//

#include "cgshop2020_verifier/face_checker.h"
#include "cgshop2020_verifier/point_hash.h"
#include <initializer_list>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arr_extended_dcel.h>
#include <unordered_map>
#include <boost/range/iterator_range.hpp>
#include <boost/iterator/transform_iterator.hpp>
#include <boost/functional/hash.hpp>
#include <boost/optional.hpp>
#include <boost/range/adaptors.hpp>
namespace cgshop2020_verifier {
namespace {
//Local CGAL Configuration
struct NoData {};
using VertexData = Instance::Index;
using Traits = CGAL::Arr_segment_traits_2<cgal::Kernel>;
using Point = Traits::Point_2;
using Segment = Traits::Segment_2;
using DCEL = CGAL::Arr_extended_dcel<Traits, VertexData, NoData, NoData>;
using Arrangement = CGAL::Arrangement_2<Traits, DCEL>;
using VertexMap = std::unordered_map<Point, VertexData, PointHash>;
using Circulator = Arrangement::Ccb_halfedge_const_circulator;
using Vertex = Arrangement::Vertex_const_handle;
using Hole_iterator = Arrangement::Hole_const_iterator;
using Isolated_vertex_iterator = Arrangement::Isolated_vertex_const_iterator;

/// Transform a solution Edge to a Segment.
struct SegmentTransformation {
  SegmentTransformation() noexcept : instance(nullptr) {}
  explicit SegmentTransformation(const Instance *instance) noexcept : instance(instance) {}

  Segment operator()(const Solution::Edge &e) const
  {
    Point pi = instance->at(e.get_i());
    Point pj = instance->at(e.get_j());
    return Segment{pi, pj};
  }

  const Instance *instance;
};

class SolutionAsCgalArrangement : public Arrangement {
 public:
  auto faces() const
  {
    return boost::make_iterator_range(this->faces_begin(), this->faces_end());
  }

  auto vertices() //const would return a const range.
  {
    return boost::make_iterator_range(this->vertices_begin(), this->vertices_end());
  }

  auto bounded_faces() const
  {
    using boost::adaptors::filtered;
    auto bounded_faces = faces() | filtered([](auto const &f) { return !f.is_unbounded(); });
    return bounded_faces;
  }

  void build_arrangement(const Instance &instance, const Solution &solution)
  {
    Arrangement::clear();

    // unfortunately, due to copyability/default-constructibility, lambdas do not work here
    SegmentTransformation trans{&instance};
    CGAL::insert(*this,
                 boost::make_transform_iterator(solution.begin(), trans),
                 boost::make_transform_iterator(solution.end(), trans));

    label_vertices(instance);
  }

 private:
  VertexMap make_vertex_map(const Instance &instance) const
  {
    VertexMap map;
    Instance::Index idx = 0;
    for (const auto &p : instance) {
      map[p] = idx;
      ++idx;
    }
    return map;
  }

  /// Label vertices with their index.
  void label_vertices(const Instance &instance)
  {
    VertexMap m = make_vertex_map(instance);
    for (auto &v: this->vertices()) {
      v.set_data(m[v.point()]);
    }
  }

};
}
}
class cgshop2020_verifier::FaceChecker::FaceCheckerImpl {
 public:

  ErrorInfo check(const Solution &solution, const Instance &instance)
  {
    arrangement.build_arrangement(instance, solution);

    for (auto check_method : {&FaceCheckerImpl::check_outer_connectivity,
                              &FaceCheckerImpl::check_outer_convexity,
                              &FaceCheckerImpl::check_bounded_convexity,
                              &FaceCheckerImpl::check_bounded_emptiness}) {
      auto err = (this->*check_method)();
      if (err && err->is_error()) {
        return err;
      }
    }

    return {};
  }

  long get_objective_value() const {
    return objective_value;
  }

 private:
  ErrorInfo report_disconnected(Circulator h1,
                                Circulator h2) const
  {
    auto v1 = h1->source();
    auto v2 = h2->source();
    Index v1i = v1->data();
    Index v2i = v2->data();
    return std::make_unique<DisconnectedOuterBoundaryErrorInformation>(v1i, v2i);
  }

  ErrorInfo report_outer_nonconvex(Vertex v) const
  {
    Index vi = v->data();
    return std::make_unique<NonConvexOuterBoundaryErrorInformation>(vi);
  }

  ErrorInfo report_bounded_nonconvex(Vertex v) const
  {
    Index vi = v->data();
    return std::make_unique<NonConvexBoundedFaceErrorInformation>(vi);
  }

  ErrorInfo report_bounded_nonempty(Vertex containing, Vertex contained) const
  {
    using Error = VertexWithinBoundedFaceErrorInformation;
    return std::make_unique<Error>(containing->data(), contained->data());
  }

  ErrorInfo check_outer_connectivity() const
  {
    const auto &uf = arrangement.unbounded_face();
    if (std::distance(uf->holes_begin(), uf->holes_end()) == 1) {
      return {};
    }
    Hole_iterator holes = uf->holes_begin();
    Circulator h1, h2;
    h1 = *holes++;
    h2 = *holes;
    return report_disconnected(h1, h2);
  }

  using ReportMethod = ErrorInfo (FaceCheckerImpl::*)(Vertex) const;

  ErrorInfo walk_ccb(Circulator c, CGAL::Orientation wrong, ReportMethod report_method) const
  {
    Circulator hole_circ = c;
    Circulator hole_prev = c;
    --hole_prev;
    do {
      if (CGAL::orientation(hole_prev->source()->point(),
                            hole_prev->target()->point(),
                            hole_circ->target()->point()) == wrong) {
        return (this->*report_method)(hole_prev->target());
      }
      hole_prev = hole_circ++;
    } while (hole_circ != c);
    return {};
  }

  ErrorInfo check_outer_convexity() const
  {
    const auto &uf = arrangement.unbounded_face();
    // as we are using a hole circulator, we are walking in clockwise! order, so expect COLLINEAR/RIGHT_TURN
    Hole_iterator holes = uf->holes_begin();
    return walk_ccb(*holes, CGAL::LEFT_TURN, &FaceCheckerImpl::report_outer_nonconvex);
  }

  ErrorInfo check_bounded_convexity() const
  {
    long n = 0;
    for (const auto &face : arrangement.bounded_faces()) {
      auto err = walk_ccb(face.outer_ccb(), CGAL::RIGHT_TURN, &FaceCheckerImpl::report_bounded_nonconvex);
      if (err && err->is_error()) {
        return err;
      }
      ++n;
    }
    objective_value = n;
    return {};
  }

  ErrorInfo check_bounded_emptiness() const
  {
    for (const auto &face : arrangement.bounded_faces()) {
      Vertex face_v = face.outer_ccb()->source();
      if (face.holes_begin() != face.holes_end()) {
        Hole_iterator holes = face.holes_begin();
        Vertex hole_v = (*holes)->source();
        return report_bounded_nonempty(face_v, hole_v);
      }
      if (face.isolated_vertices_begin() != face.isolated_vertices_end()) {
        Isolated_vertex_iterator hole_i = face.isolated_vertices_begin();
        Vertex hole_v = hole_i;
        return report_bounded_nonempty(face_v, hole_v);
      }
    }
    return {};
  }

  SolutionAsCgalArrangement arrangement;
  mutable long objective_value; // I guess this is ugly. Maybe remove constness?
};
namespace cgshop2020_verifier {
std::unique_ptr<ErrorInformation>
FaceChecker::operator()(Instance &instance, Solution &solution)
{
  FaceCheckerImpl checker;
  auto error = checker.check(solution, instance);
  objective_value = checker.get_objective_value();
  return error;
}

boost::optional<BaseChecker::ObjectiveValue> FaceChecker::get_objective() const
{
  return this->objective_value;
}
} // namespace cgshop2020_verifier
