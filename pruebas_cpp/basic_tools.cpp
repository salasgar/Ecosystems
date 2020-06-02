
#ifndef BASIC_TOOLS_CPP_INCLUDED
#define BASIC_TOOLS_CPP_INCLUDED

#include "basic_tools.hpp"

using namespace std;

int error(std::string error_name = "Unknown error") {
  cout << error_name;
  int d = 0;
  return 1/d;
};

// ************************************************************************
//         i n t L o c a t i o n           f l o a t L o c a t i o n
// ************************************************************************


intLocation::intLocation() {
  this->first = 0;
  this->second = 0;
};

intLocation::intLocation(int x, int y) {
  this->first = x;
  this->second = y;
};

int intLocation::x()  { return this->first; };

int intLocation::y()  { return this->second; };

intLocation::operator floatLocation() {
  return floatLocation(this->x(), this->y());
};

intLocation::operator string()  {
   return "(" + std::to_string(this->first) + ", " + std::to_string(this->second) + ")";
};

floatLocation::floatLocation() {
  this->first = 0;
  this->second = 0;
};

floatLocation::floatLocation(float x, float y) {
  this->first = x;
  this->second = y;
};

float floatLocation::x()  { return this->first; };

float floatLocation::y()  { return this->second; };

floatLocation::operator intLocation() {
  return intLocation((int)std::lround(this->x()), (int)std::lround(this->y()));
};

floatLocation::operator string()  {
   return "(" + std::to_string(this->first) + ", " + std::to_string(this->second) + ")";
};

string operator +(string a, intLocation B)  {
  return a + string(B);
};

string operator +(intLocation A, string b)  {
  return string(A) + b;
};

intLocation operator +(intLocation a, intLocation b)  {
  return intLocation(a.x()+b.x(), a.y()+b.y());
};


intLocation operator -(intLocation a, intLocation b)  {
  return intLocation(a.x()-b.x(), a.y()-b.y());
};

intLocation operator *(int k, intLocation A)  {
  return intLocation(k * A.x(), k * A.y());
};

intLocation operator *(intLocation A, int k)  {
  return k * A;
};

int operator *(intLocation a, intLocation b)  {
  return a.x() * b.x() + a.y() * b.y();
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

// ************************************************************************
//              R A N D O M   N U M B E R S   G E N E R A T O R
// ************************************************************************


RandomNumbersGenerator::RandomNumbersGenerator() :
eng((std::random_device())()) {
  std::uniform_real_distribution<float> distribution(- 0.01, 0.01);
  cout << "Just after initializing eng: " << distribution(eng) << endl;
  cout << "and after this: " << this->proportional_mutation_float(100.02, 0.5) << endl;
};

void RandomNumbersGenerator::set_seed(int seed) {
  this->eng.seed(seed);
};

int RandomNumbersGenerator::get_uniform_rand_int(int min, int max) {
  std::uniform_int_distribution<int> distribution(min, max);
  return distribution(this->eng);
};

long RandomNumbersGenerator::get_uniform_rand_long(long min, long max) {
  std::uniform_int_distribution<long> distribution(min, max);
  return distribution(this->eng);
};

float RandomNumbersGenerator::get_uniform_rand_float(float min, float max) {
  std::uniform_real_distribution<float> distribution(min, max);
  return distribution(this->eng);
};

intLocation RandomNumbersGenerator::get_rand_intLocation(int radius) {
  return intLocation(
    this->get_uniform_rand_int(-radius, radius),
    this->get_uniform_rand_int(-radius, radius)
  );
};

//  ************************** MUTATIONS ***************************

/*
int RandomNumbersGenerator::proportional_mutation(int base_value) {
  return this->proportional_mutation(base_value, 0.01);
};
*/

long RandomNumbersGenerator::proportional_mutation_long(long base_value, float maximum_proportion = 0.01) {
  return std::lround(this->proportional_mutation_float((float) base_value, maximum_proportion));
};

long RandomNumbersGenerator::proportional_mutation_long_min(long base_value, float maximum_proportion, long minimum_value) {
  return std::max(minimum_value, this->proportional_mutation_long(base_value, maximum_proportion));
};

long RandomNumbersGenerator::proportional_mutation_long_min_max(long base_value, float maximum_proportion, long minimum_value, long maximum_value) {
  return std::min(maximum_value, this->proportional_mutation_long_min(base_value, maximum_proportion, minimum_value));
};

/*
float RandomNumbersGenerator::proportional_mutation(float base_value){
  return this->proportional_mutation(base_value, 0.01);
};
*/

float auxiliary_function_for_proportional_mutation(float base_value, float x) {
 if (x<0) {
    return base_value / (1 - x);
  } else {
    return base_value * (1 + x);
  };
};

// with this method of mutation, it's equally probable for the value to increase or to decrease:
float RandomNumbersGenerator::proportional_mutation_float(float base_value, float maximum_proportion = 0.01) {
  
  
  std::uniform_real_distribution<float> distribution(
    - maximum_proportion,
    maximum_proportion
  );
  float x = distribution(this->eng);
  return auxiliary_function_for_proportional_mutation(base_value, x);
};

// with this method of mutation, it's more probable for the value to increase than to decrease:
float RandomNumbersGenerator::proportional_mutation_float_up(float base_value, float maximum_proportion) {
  std::uniform_real_distribution<float> distribution(
    base_value / (1 + maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

// with this method of mutation, it's more probable for the value to decrease than to increase:
float RandomNumbersGenerator::proportional_mutation_float_down(float base_value, float maximum_proportion) {
  std::uniform_real_distribution<float> distribution(
    base_value * (1 - maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

float RandomNumbersGenerator::proportional_mutation_float_min(float base_value, float maximum_proportion, float minimum_value) {
  return std::max(minimum_value, this->proportional_mutation_float(base_value, maximum_proportion));
};

float RandomNumbersGenerator::proportional_mutation_float_min_max(float base_value, float maximum_proportion, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->proportional_mutation_float_min(base_value, maximum_proportion, minimum_value));
};

/*
long RandomNumbersGenerator::uniform_mutation(long base_value) {
  return this->uniform_mutation(base_value, 1);
};
*/

long RandomNumbersGenerator::uniform_mutation_long(long base_value, float maximum_increment = 1) {
  return this->get_uniform_rand_long(base_value - maximum_increment, maximum_increment);
};

long RandomNumbersGenerator::uniform_mutation_long_min(long base_value, float maximum_increment, long minimum_value) {
  return std::max(minimum_value, this->uniform_mutation_long(base_value, maximum_increment));
};

long RandomNumbersGenerator::uniform_mutation_long_min_max(long base_value, float maximum_increment, long minimum_value, long maximum_value) {
  return std::min(maximum_value, this->uniform_mutation_long_min(base_value, maximum_increment, minimum_value));
};

/*
float RandomNumbersGenerator::uniform_mutation(float base_value){
  return this->uniform_mutation(base_value, 1.0);
};
*/

float RandomNumbersGenerator::uniform_mutation_float(float base_value, float maximum_increment = 1.0) {
  std::uniform_real_distribution<float> distribution(
    base_value - maximum_increment,
    base_value + maximum_increment
  );

  return distribution(this->eng);
};

float RandomNumbersGenerator::uniform_mutation_float_min(float base_value, float maximum_increment, float minimum_value) {
  return std::max(minimum_value, this->uniform_mutation_float(base_value, maximum_increment));
};

float RandomNumbersGenerator::uniform_mutation_float_min_max(float base_value, float maximum_increment, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->uniform_mutation_float_min(base_value, maximum_increment, minimum_value));
};

bool RandomNumbersGenerator::true_with_probability(float probability) {
  std::uniform_real_distribution<float> distribution(0.0, 1.0);
  return (distribution(this->eng) < probability);
};

AdjacentLocationsPool::AdjacentLocationsPool() {};

void AdjacentLocationsPool::initialize(std::default_random_engine* engine_ptr) {
  this->eng_ptr = engine_ptr;
  this->number_of_stored_permutations = 50; // 50 is more than enough
  this->counter = 0;
  this->adjacent_locations.resize(this->number_of_stored_permutations);
  std::vector<intLocation> locations = {
    intLocation(-1, -1),
    intLocation(-1,  0),
    intLocation(-1,  1),
    intLocation( 0, -1),
    intLocation( 0,  1),
    intLocation( 1, -1),
    intLocation( 1,  0),
    intLocation( 1,  1)
  };
  for(int i = 0; i < this->number_of_stored_permutations; i++) {
    shuffle(locations.begin(), locations.end(), *(this->eng_ptr));
    this->adjacent_locations[i] = locations;
  };
};

std::vector<intLocation> AdjacentLocationsPool::get_next() {
  this->counter = (this->counter + 1) % this->number_of_stored_permutations;
  return this->adjacent_locations[this->counter];
};

#endif  // BASIC_TOOLS_CPP_INCLUDED
