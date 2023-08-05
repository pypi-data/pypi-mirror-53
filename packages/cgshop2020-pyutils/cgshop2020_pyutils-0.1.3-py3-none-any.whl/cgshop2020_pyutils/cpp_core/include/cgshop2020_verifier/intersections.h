//
// Created by Dominik Krupke on 2019-09-17.
//

#ifndef MIN_CONVEX_PARTITION_VERIFIER_INTERSECTIONS_H
#define MIN_CONVEX_PARTITION_VERIFIER_INTERSECTIONS_H

#include "solution.h"
#include "instance.h"
#include "base_checker.h"
namespace cgshop2020_verifier {
class IntersectionChecker : public BaseChecker {
 public:

  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override;

};

}
#endif //MIN_CONVEX_PARTITION_VERIFIER_INTERSECTIONS_H
