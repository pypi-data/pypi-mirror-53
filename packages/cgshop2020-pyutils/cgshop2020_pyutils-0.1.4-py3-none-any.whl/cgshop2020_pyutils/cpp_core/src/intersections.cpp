//
// Created by Dominik Krupke on 2019-09-17.
//

#include "cgshop2020_verifier/intersections.h"
#include "sweep_line/cgal_sweep_line_wrapper.h"
namespace cgshop2020_verifier {
namespace {

using EdgeIndex = size_t;
using SweepLineAlg = details::CgalSweepLineWrapper<EdgeIndex>;

SweepLineAlg
prepare_sweep_line(const Solution &solution, const Instance &instance)
{
  details::CgalSweepLineWrapper<EdgeIndex> sla{};
  for (EdgeIndex i = 0; i < solution.size(); ++i) {
    const auto &e = solution.at(i);
    sla.add_segment(instance.at(e.get_i()), instance.at(e.get_j()), i);
  }
  return sla;
}

template<typename Iterator>
auto get_edges_from_indices(const Solution &s, Iterator begin, Iterator end)
{
  std::vector<Solution::Edge> edges;
  edges.reserve(std::distance(begin, end));
  std::for_each(begin, end, [&](auto i) { edges.push_back(s.at(i)); });
  return edges;
}

struct CollisionInformation {
  std::vector<EdgeIndex> edge_indices;
  cgal::Point point;
};

bool find_first_intersection(SweepLineAlg &alg, CollisionInformation *data)
{
  bool intersection = false;
  alg.set_intersection_callback([&](cgal::Point p, std::vector<size_t> v) {
    intersection = true;
    data->point = std::move(p);
    std::sort(v.begin(), v.end());
    auto it = std::unique(v.begin(), v.end());
    v.resize(std::distance(v.begin(), it));
    data->edge_indices = std::move(v);
    return details::CgalSweepLineWrapper<EdgeIndex>::STOP;
  });
  alg.sweep();
  return intersection;
}
}

std::unique_ptr<ErrorInformation> IntersectionChecker::operator()(Instance &instance, Solution &solution)
{
  auto sla = prepare_sweep_line(/*solution=*/solution, /*instance=*/instance);
  CollisionInformation data;
  if (find_first_intersection(sla, &data)) {
    auto involved_edges = get_edges_from_indices(solution, data.edge_indices.begin(),
                                                 data.edge_indices.end());
    return std::make_unique<IntersectionErrorInformation>(data.point, involved_edges);
  }
  return std::unique_ptr<ErrorInformation>();
}

}
