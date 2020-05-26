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
  int proportional_mutation(int base_value);
  int proportional_mutation(int base_value, float maximum_proportion);
  int proportional_mutation(int base_value, float maximum_proportion, int minimum_value);
  int proportional_mutation(int base_value, float maximum_proportion, int minimum_value, int maximum_value);
  float proportional_mutation(float base_value);
  float proportional_mutation(float base_value, float maximum_proportion);
  float proportional_mutation(float base_value, float maximum_proportion, float minimum_value);
  float proportional_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
  int uniform_mutation(int base_value);
  int uniform_mutation(int base_value, float maximum_proportion);
  int uniform_mutation(int base_value, float maximum_proportion, int minimum_value);
  int uniform_mutation(int base_value, float maximum_proportion, int minimum_value, int maximum_value);
  float uniform_mutation(float base_value);
  float uniform_mutation(float base_value, float maximum_proportion);
  float uniform_mutation(float base_value, float maximum_proportion, float minimum_value);
  float uniform_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
};

// Can I do this?
void make_instance_of_class(class my_class) {
  my_class my_object;
  my_object.do_something();
};

// Can I do this?
void make_instance_of_class_2(class my_class, my_class my_object) {
  my_class* my_object_ptr;
  my_object_ptr = &my_object;
  my_object_ptr->do_something();
};


#endif  // BASIC_TOOLS_H_INCLUDED


/* TO DO:
 read http://www.cplusplus.com/doc/oldtutorial/polymorphism/
*/
