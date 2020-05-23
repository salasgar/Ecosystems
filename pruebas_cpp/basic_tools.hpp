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

template <class T>
class Location : public std::pair<T, T> {
  Location<T>& operator+=(const Location<T>& B);
  Location<T> operator+(Location<T> A, const Location<T>& B);
  T x();
  T y();
};

typedef Location<int> intLocation;
typedef Location<float> floatLocation;

template <class T>
T chess_distance(Location<T> A, Location<T> B);

template <class T>
float euclidean_distance(Location<T> A, Location<T> B);

template <class T>
T taxi_distance(Location<T> A, Location<T> B);

class RandomNumbersGenerator {
public:
  std::default_random_engine eng;
  RandomNumbersGenerator();
  void set_seed(int seed);
  int get_uniform_rand_int(int min, int max);
  intLocation get_rand_intLocation(int radius);
};

#endif  // BASIC_TOOLS_H_INCLUDED


/* TO DO:
 read http://www.cplusplus.com/doc/oldtutorial/polymorphism/
*/
