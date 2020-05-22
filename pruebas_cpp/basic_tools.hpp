#ifndef BASIC_TOOLS_H_INCLUDED
#define BASIC_TOOLS_H_INCLUDED

#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
#include "organism.hpp"

typedef enum {No_error, Error_Organism_not_found, Error_No_free_location_found} ErrorType;

template <T>
class Location : public std::pair<T, T> {
  Location<T>& operator+=(const Location<T>& B);
  Location<T> operator+(Location<T> A, const Location<T>& B);
  T x();
  T y();
};

typedef Location<int> intLocation;
typedef Location<float> floatLocation;

#endif  // BASIC_TOOLS_H_INCLUDED


