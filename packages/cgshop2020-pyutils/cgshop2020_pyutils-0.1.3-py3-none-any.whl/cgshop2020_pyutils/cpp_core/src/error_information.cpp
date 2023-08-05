//
// Created by Dominik Krupke on 20.09.19.
//

#include <cgshop2020_verifier/error_informations.h>

std::ostream &operator<<(std::ostream &os, const cgshop2020_verifier::ErrorInformation &errorInformation)
{
  os << errorInformation.get_error_name();
  os << ": ";
  os << errorInformation.get_error_explanation();
  return os;
}
