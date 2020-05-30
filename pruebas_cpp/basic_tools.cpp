
#include "basic_tools.hpp"

using namespace std;

template <class T>
Location<T>::Location(T x, T y) {
  this->first = x;
  this->second = y;
};

template <class T>
Location<T>::Location() {
  this->first = 0;
  this->second = 0;
};

template <class T>
Location<T>& operator+(const Location<T>& A, const Location<T>& B) {
  return Location<T>(A.first + B.first, A.second + B.second);
};
/*
template <>
Location<int>& operator+(const Location<int>& A, const Location<int>& B) {
  return Location<int>(A.first + B.first, A.second + B.second);
};
*/

template <class T>
T Location<T>::x() { return this->first; }

template <class T>
T Location<T>::y() { return this->second; }

template <>
Location<int>::Location() {};

template <>
Location<float>::Location() {};

int chess_distance(intLocation A, intLocation B) {
  return std::max(
    std::abs(A.first - B.first),
    std::abs(A.second - B.second)
  );
};

float euclidean_distance(intLocation A, intLocation B) {
  return std::sqrt(
    pow(A.first - B.first, 2)
    +
    pow(A.second - B.second, 2)
  );
};

int taxi_distance(intLocation A, intLocation B) {
  return (std::abs(A.x() - B.x()) + std::abs(A.y() - B.y()));
};

RandomNumbersGenerator::RandomNumbersGenerator() :
eng((std::random_device())()) {
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

long RandomNumbersGenerator::proportional_mutation(long base_value, float maximum_proportion = 0.01) {
  return std::lround(this->proportional_mutation((float) base_value, maximum_proportion));
};

long RandomNumbersGenerator::proportional_mutation(long base_value, float maximum_proportion, long minimum_value) {
  return std::max(minimum_value, this->proportional_mutation(base_value, maximum_proportion));
};

long RandomNumbersGenerator::proportional_mutation(long base_value, float maximum_proportion, long minimum_value, long maximum_value) {
  return std::min(maximum_value, this->proportional_mutation(base_value, maximum_proportion, minimum_value));
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
float RandomNumbersGenerator::proportional_mutation(float base_value, float maximum_proportion = 0.01) {
  std::uniform_real_distribution<float> distribution(
    - maximum_proportion,
    maximum_proportion
  );
  return auxiliary_function_for_proportional_mutation(base_value, distribution(this->eng));
};

// with this method of mutation, it's more probable for the value to increase than to decrease:
float RandomNumbersGenerator::proportional_mutation_up(float base_value, float maximum_proportion) {
  std::uniform_real_distribution<float> distribution(
    base_value / (1 + maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

// with this method of mutation, it's more probable for the value to decrease than to increase:
float RandomNumbersGenerator::proportional_mutation_down(float base_value, float maximum_proportion) {
  std::uniform_real_distribution<float> distribution(
    base_value * (1 - maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

float RandomNumbersGenerator::proportional_mutation(float base_value, float maximum_proportion, float minimum_value) {
  return std::max(minimum_value, this->proportional_mutation(base_value, maximum_proportion));
};

float RandomNumbersGenerator::proportional_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->proportional_mutation(base_value, maximum_proportion, minimum_value));
};

/*
long RandomNumbersGenerator::uniform_mutation(long base_value) {
  return this->uniform_mutation(base_value, 1);
};
*/

long RandomNumbersGenerator::uniform_mutation(long base_value, float maximum_increment = 1) {
  return this->get_uniform_rand_long(base_value - maximum_increment, maximum_increment);
};

long RandomNumbersGenerator::uniform_mutation(long base_value, float maximum_increment, long minimum_value) {
  return std::max(minimum_value, this->uniform_mutation(base_value, maximum_increment));
};

long RandomNumbersGenerator::uniform_mutation(long base_value, float maximum_increment, long minimum_value, long maximum_value) {
  return std::min(maximum_value, this->uniform_mutation(base_value, maximum_increment, minimum_value));
};

/*
float RandomNumbersGenerator::uniform_mutation(float base_value){
  return this->uniform_mutation(base_value, 1.0);
};
*/

float RandomNumbersGenerator::uniform_mutation(float base_value, float maximum_increment = 1.0) {
  std::uniform_real_distribution<float> distribution(
    base_value - maximum_increment,
    base_value + maximum_increment
  );
  return distribution(this->eng);
};

float RandomNumbersGenerator::uniform_mutation(float base_value, float maximum_increment, float minimum_value) {
  return std::max(minimum_value, this->uniform_mutation(base_value, maximum_increment));
};

float RandomNumbersGenerator::uniform_mutation(float base_value, float maximum_increment, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->uniform_mutation(base_value, maximum_increment, minimum_value));
};

bool RandomNumbersGenerator::true_with_probability(float probability) {
  std::uniform_real_distribution<float> distribution(0.0, 1.0);
  return (distribution(this->eng) < probability);
};


