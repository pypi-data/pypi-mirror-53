//
// Created by Dominik Krupke on 2019-09-17.
//

#ifndef CGSHOP2020_VERIFIER_CGAL_SWEEP_LINE_WRAPPER_H
#define CGSHOP2020_VERIFIER_CGAL_SWEEP_LINE_WRAPPER_H
#include <vector>
#include <functional>
#include "cgshop2020_verifier/cgal.h"
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arr_consolidated_curve_data_traits_2.h>
#include <boost/range/iterator_range_core.hpp>
#include <CGAL/Surface_sweep_2.h>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arr_consolidated_curve_data_traits_2.h>
#include <CGAL/Surface_sweep_2/Intersection_points_visitor.h>
#include <boost/range/iterator_range_core.hpp>
#include <boost/range/join.hpp>
#include "cgal_sweep_line_wrapper.h"
namespace cgshop2020_verifier {
namespace details {

template<typename EdgeData>
class CgalSweepLineWrapper {
 public:
  enum ProceedCommand { CONTINUE, STOP };

  using IntersectionCallback = std::function<ProceedCommand(cgal::Point, std::vector<EdgeData>)>;

  using SegmentTrait = CGAL::Arr_segment_traits_2<cgal::Kernel>;
  using Segment = CGAL::Arr_segment_traits_2<cgal::Kernel>::X_monotone_curve_2;
  using SegmentWithDataTrait = CGAL::Arr_consolidated_curve_data_traits_2<SegmentTrait,
                                                                          EdgeData>;
  using SegmentWithData = typename SegmentWithDataTrait::X_monotone_curve_2;
  void add_segment(cgal::Point a, cgal::Point b, EdgeData data)
  {
    segments.emplace_back(Segment{a, b}, data);
  }

  /**
   * Set the function that should be called on found intersections.
   * @param ic (Point, std::vector<EdgeData>)->Proceed Command
   *            Is called on a found intersection. The return value decides if
   *            the sweep is continued or aborted. The first parameter is the
   *            position of the intersection. The other parameter states the
   *            data of the involved edges.
   */
  void set_intersection_callback(IntersectionCallback ic) { this->callback = std::move(ic); }

  void sweep();

 private:

  class Visitor :
      public CGAL::Surface_sweep_2::Default_visitor<Visitor, SegmentWithDataTrait> {
   public:
    using Super = CGAL::Surface_sweep_2::Default_visitor<Visitor, SegmentWithDataTrait>;
    using Point = typename SegmentWithDataTrait::Point_2;
    using Event = typename Super::Event;
    using Subcurve = typename Super::Subcurve;
    using Status_line_iterator = typename Super::Status_line_iterator;

    explicit Visitor(typename CgalSweepLineWrapper::IntersectionCallback &cb) : callback{cb} {}

    virtual ~Visitor() = default;

    /// Called by cgal on events
    bool after_handle_event(Event *event, Status_line_iterator /* iter */, bool /* flag */)
    {
      if (event->is_intersection() || event->is_weak_intersection() || event->is_overlap()) {
        auto involved_edges = get_involved_edges(event);
        auto c = callback(static_cast<cgal::Point>(event->point()), involved_edges);
        if (c == CgalSweepLineWrapper::ProceedCommand::STOP) {
          this->surface_sweep()->stop_sweep();
        }
      }
      return true;
    }

   private:
    template<typename Curve>
    EdgeData get_segment_info(Curve c)
    {
      auto data = (*c)->last_curve().data();
      return *(data.begin());
    }

    std::vector<EdgeData>
    get_involved_edges(Event *event)
    {
      std::vector<EdgeData> ret;
      auto add = [&](auto begin, auto end) {
        for (auto c = begin; c != end; ++c) {
          auto curve = *c;
          if(curve->is_leaf(curve)) {
            ret.push_back(get_segment_info(c));
          } else {
            std::vector<decltype(curve)> sub_curves;
            curve->all_leaves(std::back_inserter(sub_curves));
            for(auto sc: sub_curves) {
              ret.push_back(get_segment_info(&sc));
            }
          }
        }
      };
      add(event->left_curves_begin(), event->left_curves_end());
      add(event->right_curves_begin(), event->right_curves_end());
      return ret;
    }

    typename CgalSweepLineWrapper::IntersectionCallback &callback;
  };

  std::vector<SegmentWithData> segments;
  IntersectionCallback callback;
};

template<typename EdgeData>
void CgalSweepLineWrapper<EdgeData>::sweep()
{
  using Surface_sweep = CGAL::Surface_sweep_2::Surface_sweep_2<Visitor>;
  Visitor vis{this->callback};
  Surface_sweep sweep(&vis);
  sweep.sweep(this->segments.begin(), this->segments.end());
}

}
}
#endif //CGSHOP2020_VERIFIER_CGAL_SWEEP_LINE_WRAPPER_H
