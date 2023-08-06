//
// Created by Dominik Krupke on 2019-09-13.
//

#ifndef MIN_CONVEX_PARTITION_VERIFIER_SOLUTION_H
#define MIN_CONVEX_PARTITION_VERIFIER_SOLUTION_H
#include "cgshop2020_verifier/instance.h"
namespace cgshop2020_verifier {
class Solution {
 public:
  class Edge {
   public:
    Edge() : i{0}, j{0}
    {
      /* pass */
    }
    Edge(Instance::Index i, Instance::Index j) :
        i{std::min(i, j)}, j{std::max(i, j)}
    {
      /* pass */
    }

    Instance::Index get_i() const { return i; }
    Instance::Index get_j() const { return j; }

    explicit operator std::tuple<Instance::Index, Instance::Index>() const
    {
      return this->to_tuple();
    }

    std::tuple<Instance::Index, Instance::Index> to_tuple() const {
      return {this->get_i(), this->get_j()};
    }

    bool operator<(const Edge &e) const
    {
      return this->to_tuple() < e.to_tuple();
    }

    bool operator==(const Edge &e) const
    {
      return e.get_i() == this->get_i() && e.get_j() == this->get_j();
    }

   private:
    Instance::Index i, j;
  };

  void add_edge(Instance::Index i, Instance::Index j)
  {
    this->edges.emplace_back(i, j);
  }

  void add_edges(std::initializer_list<std::pair<Instance::Index,Instance::Index>> edges) {
    for(auto e : edges) {
      this->add_edge(e.first, e.second);
    }
  }

  Edge at(size_t idx) const {
    return this->edges.at(idx);
  }

  auto begin() {
    return this->edges.begin();
  }

  auto begin() const {
    return this->edges.cbegin();
  }

  auto end() const {
    return this->edges.cend();
  }

  auto end() {
    return this->edges.end();
  }

  size_t size() const
  {
    return edges.size();
  }

  void make_unique() noexcept;

 private:
  std::vector<Edge> edges;
};
}

#endif //MIN_CONVEX_PARTITION_VERIFIER_SOLUTION_H
