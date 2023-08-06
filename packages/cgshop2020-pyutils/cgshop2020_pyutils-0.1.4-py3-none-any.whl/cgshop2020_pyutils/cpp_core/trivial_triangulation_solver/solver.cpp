//
// Created by Phillip Keldenich on 2019-09-24.
//

#include "solver.h"
#include <CGAL/Delaunay_triangulation_2.h>
#include <CGAL/Triangulation_vertex_base_with_info_2.h>
#include <boost/iterator/zip_iterator.hpp>
#include <boost/iterator/counting_iterator.hpp>
#include <boost/range/iterator_range.hpp>

namespace cgshop2020_verifier {
namespace impl {
namespace {
using Index = Instance::Index;
using VertexInfo = Index;
using GeometryTraits = cgal::Kernel;
using VertexDataStructure = CGAL::Triangulation_vertex_base_with_info_2<VertexInfo, GeometryTraits>;
using FaceDataStructure = CGAL::Triangulation_face_base_2<GeometryTraits>;
using TriangulationDataStructure = CGAL::Triangulation_data_structure_2<VertexDataStructure, FaceDataStructure>;
using Triangulation = CGAL::Delaunay_triangulation_2<GeometryTraits, TriangulationDataStructure>;
using Vertex = Triangulation::Vertex_handle;

void add_edge_to_solution(Solution& s, const Triangulation& t, Vertex v1, Vertex v2) {
  auto infv = t.infinite_vertex();
  if(v1 != infv && v2 != infv) {
    Index i = v1->info();
    Index j = v2->info();
    s.add_edge(i, j);
  }
}

auto make_point_range_zip(const cgshop2020_verifier::Instance &instance) {
  auto points_begin = instance.begin();
  auto points_end = instance.end();
  auto count_begin = boost::make_counting_iterator(Index{0});
  auto count_end = boost::make_counting_iterator(Index{instance.size()});
  auto zip_begin = boost::make_zip_iterator(boost::make_tuple(points_begin, count_begin));
  auto zip_end = boost::make_zip_iterator(boost::make_tuple(points_end, count_end));
  return std::make_pair(zip_begin, zip_end);
}

Solution iterate_faces(const Triangulation& triangulation) {
  Solution result;
  auto face_range = boost::make_iterator_range(triangulation.all_faces_begin(), triangulation.all_faces_end());
  for(const auto& f : face_range) {
    auto p1 = f.vertex(0);
    auto p2 = f.vertex(1);
    auto p3 = f.vertex(2);
    impl::add_edge_to_solution(result, triangulation, p1, p2);
    impl::add_edge_to_solution(result, triangulation, p2, p3);
    impl::add_edge_to_solution(result, triangulation, p3, p1);
  }
  result.make_unique();
  return result;
}

}
}
}

auto cgshop2020_verifier::TrivialTriangulationSolver::operator()(const cgshop2020_verifier::Instance &instance)
  -> Solution
{
  // create the triangulation, using bulk insertion with info
  auto range = impl::make_point_range_zip(instance);
  impl::Triangulation triangulation(range.first, range.second);
  return impl::iterate_faces(triangulation);
}
