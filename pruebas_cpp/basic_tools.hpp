#ifndef BASIC_TOOLS_HPP_INCLUDED
#define BASIC_TOOLS_HPP_INCLUDED

#include <iostream>

#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
#include <string>
#include <stdio.h>
#include <typeinfo>
#include <chrono>
#include "math.h"
#define _USE_MATH_DEFINES
#include <numeric>

using namespace std;

int error(std::string error_name);

typedef enum {No_error, Error_Organism_not_found, Error_No_free_location_found} ErrorType;

// ------------------------------------------------------------------------
//         i n t L o c a t i o n           f l o a t L o c a t i o n
// ------------------------------------------------------------------------

class floatLocation;

class intLocation : public std::pair<int, int> {
public:
  intLocation();
  intLocation(int x, int y);
  int x();
  int y();
  operator floatLocation();
  operator string();
};

class floatLocation : public std::pair<float, float> {
public:
  floatLocation();
  floatLocation(float x, float y);
  float x();
  float y();
  operator intLocation();
  operator string();
};

string operator +(string a, intLocation B);

string operator +(intLocation A, string b);

intLocation operator +(intLocation a, intLocation b);


intLocation operator -(intLocation a, intLocation b);

intLocation operator *(int k, intLocation A);

intLocation operator *(intLocation A, int k);

int operator *(intLocation a, intLocation b);

int chess_module(intLocation A);

int taxi_module(intLocation A);

float euclidean_module(intLocation A);

int chess_distance(intLocation A, intLocation B);

int taxi_distance(intLocation A, intLocation B);

float euclidean_distance(intLocation A, intLocation B);

const intLocation NULL_LOCATION = intLocation(-1000000, -1000000);

const string ENDL = "\n";

// ------------------------------------------------------------------------
//              R A N D O M   N U M B E R S   G E N E R A T O R
// ------------------------------------------------------------------------

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
  long proportional_mutation_long(long base_value, float maximum_proportion);
  long proportional_mutation_long_min(long base_value, float maximum_proportion, long minimum_value);
  long proportional_mutation_long_min_max(long base_value, float maximum_proportion, long minimum_value, long maximum_value);
  //float proportional_mutation(float base_value);
  float proportional_mutation_float(float base_value, float maximum_proportion);
  float proportional_mutation_float_up(float base_value, float maximum_proportion);
  float proportional_mutation_float_down(float base_value, float maximum_proportion);
  float proportional_mutation_float_min(float base_value, float maximum_proportion, float minimum_value);
  float proportional_mutation_float_min_max(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
  //long uniform_mutation(long base_value);
  long uniform_mutation_long(long base_value, float maximum_proportion);
  long uniform_mutation_long_min(long base_value, float maximum_proportion, long minimum_value);
  long uniform_mutation_long_min_max(long base_value, float maximum_proportion, long minimum_value, long maximum_value);
  //float uniform_mutation(float base_value);
  float uniform_mutation_float(float base_value, float maximum_proportion);
  float uniform_mutation_float_min(float base_value, float maximum_proportion, float minimum_value);
  float uniform_mutation_float_min_max(float base_value, float maximum_proportion, float minimum_value, float maximum_value);
  bool true_with_probability(float probability);
};

#endif  // BASIC_TOOLS_HPP_INCLUDED
