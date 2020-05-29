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

void Error(std::string error_name = "Unknown error") {
  // print error_name;
  int err = 1/0;
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

intLocation make_int_location(int x, int y) {
  intLocation loc(x, y);
  return loc;
};

floatLocation make_float_location(float x, float y) {
  floatLocation loc(x, y);
  return loc;
};

intLocation make_int_location(floatLocation fLoc) {
  intLocation loc(std::lround(fLoc.x()), std::lround(fLoc.y()));
  return loc;
};

floatLocation make_float_location(intLocation iLoc) {
  floatLocation loc(iLoc.x(), iLoc.y());
  return loc;
};

typedef enum {No_error, Error_Organism_not_found, Error_No_free_location_found} ErrorType;


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

class Base_biotope {
 public:
  Base_biotope() {};
  Base_ecosystem* parent_ecosystem_ptr;
};

class Base_ecosystem {
 public:
  Base_biotope biotope_ptr;
  long int cycle;
  RandomNumbersGenerator random_nums_gen;
  Base_ecosystem() {};
  void kill_and_remove_organism(Base_organism* organism);
};

class Base_organism {
 public:
  Base_biotope* parent_biotope_ptr;
  Base_ecosystem* parent_ecosystem_ptr;
  Base_organism() {};
  void reset(intLocation location, Base_ecosystem* parent_ecosystem_ptr);
  void change_location_to(intLocation new_location);
};

class Base_organisms_pool {};

#endif  // BASIC_TOOLS_H_INCLUDED


/* TO DO:
 read http://www.cplusplus.com/doc/oldtutorial/polymorphism/
*/
