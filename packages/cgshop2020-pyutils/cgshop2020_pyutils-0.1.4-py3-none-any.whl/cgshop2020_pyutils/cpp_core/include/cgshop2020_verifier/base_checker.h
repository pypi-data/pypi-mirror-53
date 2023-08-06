//
// Created by Dominik Krupke on 20.09.19.
//

#ifndef CGSHOP2020_VERIFIER_BASE_CHECKER_H
#define CGSHOP2020_VERIFIER_BASE_CHECKER_H

#include "error_informations.h"
namespace cgshop2020_verifier {

class BaseChecker {
 public:
  virtual std::unique_ptr<ErrorInformation>
  operator()(Instance &instance, Solution &solution) = 0;
  virtual ~BaseChecker() {}
  using ObjectiveValue = long;
  virtual boost::optional<ObjectiveValue> get_objective() const
  {
    return {};
  }
};

class CheckerPipe : public BaseChecker {
 public:

  template<typename T, typename... Args>
  T &add_checker(Args &&... args)
  {
    std::unique_ptr<T> checker(new T(std::forward<Args>(args)...));
    T &ret = *checker;
    checkers.push_back(std::move(checker));
    return ret;
  }

  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    for (const auto &checker: checkers) {
      auto error = (*checker)(instance, solution);
      if (error && error->is_error()) {
        return error;
      }
    }
    return std::unique_ptr<ErrorInformation>();
  }

  boost::optional<ObjectiveValue> get_objective() const override
  {
    for (const auto &checker: checkers) {
      auto obj = checker->get_objective();
      if (obj) {
        return obj;
      }
    }
    return BaseChecker::get_objective();
  }

 private:
  std::vector<std::unique_ptr<BaseChecker>> checkers;
};

} // namespace cgshop2020_verifier

#endif //CGSHOP2020_VERIFIER_BASE_CHECKER_H
