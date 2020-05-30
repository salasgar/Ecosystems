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

int Error(std::string error_name = "Unknown error") {
  cout << error_name;
  int d = 0;
  return 1/d;
};

typedef enum {No_error, Error_Organism_not_found, Error_No_free_location_found} ErrorType;

// ------------------------------------------------------------------------
//         i n t L o c a t i o n           f l o a t L o c a t i o n
// ------------------------------------------------------------------------

class intLocation : public std::pair<int, int> {
public:
  intLocation();
  intLocation(int x, int y);
  int x() { return this->first; };
  int y() { return this->second; };
  operator string() {
    return "(" + std::to_string(this->first) + ", " + std::to_string(this->second) + ")";
    
  };
};

intLocation::intLocation() {
  this->first = 0;
  this->second = 0;
};

intLocation::intLocation(int x, int y) {
  this->first = x;
  this->second = y;
};

class floatLocation : public std::pair<float, float> {
public:
  floatLocation();
  floatLocation(float x, float y);
  float x() { return this->first; };
  float y() { return this->second; };
  operator string() {
    return "(" + std::to_string(this->first) + ", " + std::to_string(this->second) + ")";
    
  };
};

floatLocation::floatLocation() {
  this->first = 0;
  this->second = 0;
};

floatLocation::floatLocation(float x, float y) {
  this->first = x;
  this->second = y;
};

std::string to_string(intLocation A) {
  return string(A);
};

string operator +(string a, intLocation B)  {
  return a + string(B);
};

string operator +(intLocation A, string b)  {
  return string(A) + b;
};

intLocation operator +(intLocation a, intLocation b)  {
  intLocation temp = intLocation(a.x()+b.x(), a.y()+b.y());
  return temp;
};


intLocation operator -(intLocation a, intLocation b)  {
  intLocation temp = intLocation(a.x()-b.x(), a.y()-b.y());
  return temp;
};

intLocation operator *(int k, intLocation A)  {
  intLocation temp = intLocation(k * A.x(), k * A.y());
  return temp;
};

intLocation operator *(intLocation A, int k)  {
  return k * A;
};

int operator *(intLocation a, intLocation b)  {
  int temp = a.x() * b.x() + a.y() * b.y();
  return temp;
};

int chess_module(intLocation A) {
  return A.x() + A.y();
};

int taxi_module(intLocation A) {
  return std::max(A.x(), A.y());
};

float euclidean_module(intLocation A) {
  return std::sqrt(A * A);
};

int chess_distance(intLocation A, intLocation B) {
  return chess_module(A - B);
};

int taxi_distance(intLocation A, intLocation B) {
  return taxi_module(A - B);
};

float euclidean_distance(intLocation A, intLocation B) {
  return euclidean_module(A - B);
};

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

#endif  // BASIC_TOOLS_HPP_INCLUDED
