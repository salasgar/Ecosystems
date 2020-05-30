#ifndef BASIC_TOOLS_H_INCLUDED
#define BASIC_TOOLS_H_INCLUDED

#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
//#include "organism.hpp"

class Base_organism;
class Base_biotope;
class Base_ecosystem;
class Base_organisms_pool;
class RandomNumbersGenerator;

class Organism;
class Biotope;
class Ecosystem;

int Error(std::string error_name = "Unknown error") {
  // print error_name;
  return 1/0;
};

template <class T>
class Location : public std::pair<T, T> {
public:
  Location();
  Location(T x_, T y_);
  T x();
  T y();
};

template <class T>
Location<T>& operator+(const Location<T> &A, const Location<T> &B);

typedef Location<int> intLocation;
typedef Location<float> floatLocation;

const intLocation NULL_LOCATION = intLocation(-1000000, -1000000);

intLocation make_int_location(int x, int y) {
  intLocation loc(x, y);
  return loc;
};

floatLocation make_float_location(float x, float y) {
  floatLocation loc(x, y);
  return loc;
};

intLocation make_int_location(floatLocation fLoc) {
  intLocation loc((int)std::lround(fLoc.x()), (int)std::lround(fLoc.y()));
  return loc;
};

floatLocation make_float_location(intLocation iLoc) {
  floatLocation loc(iLoc.x(), iLoc.y());
  return loc;
};

typedef enum {No_error, Error_Organism_not_found, Error_No_free_location_found} ErrorType;


int chess_distance(intLocation A, intLocation B);

float euclidean_distance(intLocation A, intLocation B);

int taxi_distance(intLocation A, intLocation B);

class RandomNumbersGenerator {
public:
  std::default_random_engine eng;
  RandomNumbersGenerator();
  void set_seed(int seed);
  int get_uniform_rand_int(int min, int max);
  long get_uniform_rand_long(long min, long max);
  float get_uniform_rand_float(float min, float max);
  intLocation get_rand_intLocation(int radius);
  //long proportional_mutation(long base_value);
  long proportional_mutation(long base_value, float maximum_proportion);
  long proportional_mutation(long base_value, float maximum_proportion, long minimum_value);
  long proportional_mutation(long base_value, float maximum_proportion, long minimum_value, long maximum_value);
  //float proportional_mutation(float base_value);
  float proportional_mutation(float base_value, float maximum_proportion);
  float proportional_mutation_up(float base_value, float maximum_proportion);
  float proportional_mutation_down(float base_value, float maximum_proportion);
  float proportional_mutation(float base_value, float maximum_proportion, float minimum_value);
  float proportional_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
  //long uniform_mutation(long base_value);
  long uniform_mutation(long base_value, float maximum_proportion);
  long uniform_mutation(long base_value, float maximum_proportion, long minimum_value);
  long uniform_mutation(long base_value, float maximum_proportion, long minimum_value, long maximum_value);
  //float uniform_mutation(float base_value);
  float uniform_mutation(float base_value, float maximum_proportion);
  float uniform_mutation(float base_value, float maximum_proportion, float minimum_value);
  float uniform_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
  bool true_with_probability(float probability);
};

#endif  // BASIC_TOOLS_H_INCLUDED


/* TO DO:
 read http://www.cplusplus.com/doc/oldtutorial/polymorphism/
*/
