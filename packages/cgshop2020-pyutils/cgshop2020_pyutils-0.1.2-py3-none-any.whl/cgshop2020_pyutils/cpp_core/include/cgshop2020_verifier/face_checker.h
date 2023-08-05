//
// Created by Dominik Krupke on 2019-09-17.
//

#ifndef MIN_CONVEX_PARTITION_VERIFIER_FACES_H
#define MIN_CONVEX_PARTITION_VERIFIER_FACES_H
#include "cgshop2020_verifier/solution.h"
#include "cgshop2020_verifier/instance.h"
#include "base_checker.h"
namespace cgshop2020_verifier {
class FaceChecker : public BaseChecker {
 public:
  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override;

  using Index = Instance::Index;

  using ErrorInfo = std::unique_ptr<ErrorInformation>;

  boost::optional<ObjectiveValue> get_objective() const override;

 private:

  class FaceCheckerImpl; // Allowing FaceCheckerImpl access to private members. No longer necessary.
  boost::optional<ObjectiveValue> objective_value;
};
}

#endif //MIN_CONVEX_PARTITION_VERIFIER_FACES_H
