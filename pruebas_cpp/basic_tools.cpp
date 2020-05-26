
#include "basic_tools.hpp"

using namespace std;

template <T>
Location<T>& Location<T>::operator+=(const Location<T>& B) {
    this->first += B.first;
    this->second += B.second;
    return *this;
};

template <T>
Location<T> Location<T>::operator+(Location<T> A, const Location<T>& B) {
    return A += B;
};

template <T>
T Location<T>::x() { return this->first; }

template <T>
T Location<T>::y() { return this->second; }

template <class T>
T chess_distance(Location<T> A, Location<T> B) {
  return std::max(
    std::abs(A.first - B.first),
    std::abs(A.second - B.second)
  );
};

template <class T>
float euclidean_distance(Location<T> A, Location<T> B) {
  return std::sqrt(
    (A.first - B.first)**2
    +
    (A.second - B.second)**2
  );
};

template <class T>
T taxi_distance(Location<T> A, Location<T> B) {
  return
    std::abs(A.first - B.first)
    +
    std::abs(A.second - B.second);
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

intLocation RandomNumbersGenerator::get_rand_intLocation(int radius) {
  return intLocation(
    this->get_uniform_rand_int(-radius, radius),
    this->get_uniform_rand_int(-radius, radius)
  );
};

int RandomNumberGenerator::proportional_mutation(int base_value) {
  return this->proportional_mutation(base_value, maximum_proportion = 10.0);
};

int RandomNumberGenerator::proportional_mutation(int base_value, float maximum_proportion) {
  return std::lround(this->proportional_mutation((float) base_value, maximum_proportion));
};

int RandomNumberGenerator::proportional_mutation(int base_value, float maximum_proportion, int minimum_value) {
  return std::max(minimum_value, this->proportional_mutation(base_value, maximum_proportion));
};

int RandomNumberGenerator::proportional_mutation(int base_value, float maximum_proportion, int minimum_value, int maximum_value) {
  return std::min(maximum_value, this->proportional_mutation(base_value, maximum_proportion, minimum_value));
};

float RandomNumberGenerator::proportional_mutation(float base_value){
  return this->proportional_mutation(base_value, maximum_proportion = 10.0);
};

float RandomNumberGenerator::proportional_mutation(float base_value, float maximum_proportion) {
  
  float auxiliary_function(float x) {
   if (x<0) {
      return base_value / (1 - x);
    } else {
      return base_value * (1 + x);
    };
  };
  
  std::uniform_distribution<float> distribution(
    - maximum_proportion,
    maximum_proportion
  );
  return auxiliary_function(distribution(this->eng));
};

// alternative ways of changing a value:

float RandomNumberGenerator::proportional_mutation_2(float base_value, float maximum_proportion) {
  std::uniform_distribution<float> distribution(
    base_value / (1 + maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

float RandomNumberGenerator::proportional_mutation_3(float base_value, float maximum_proportion) {
  std::uniform_distribution<float> distribution(
    base_value * (1 - maximum_proportion),
    base_value * (1 + maximum_proportion)
  );
  return distribution(this->eng);
};

float RandomNumberGenerator::proportional_mutation(float base_value, float maximum_proportion, float minimum_value) {
  return std::max(minimum_value, this->proportional_mutation(base_value, maximum_proportion));
};

float RandomNumberGenerator::proportional_mutation(float base_value, float maximum_proportion, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->proportional_mutation(base_value, maximum_proportion, minimum_value));
};

int RandomNumberGenerator::uniform_mutation(int base_value) {
  return this->uniform_mutation(base_value, maximum_increment = 1);
};

int RandomNumberGenerator::uniform_mutation(int base_value, float maximum_increment) {
  return this->get_uniform_rand_int(base_value - maximum_increment, maximum_increment);
};

int RandomNumberGenerator::uniform_mutation(int base_value, float maximum_increment, int minimum_value) {
  return std::max(minimum_value, this->uniform_mutation(base_value, maximum_increment));
};

int RandomNumberGenerator::uniform_mutation(int base_value, float maximum_increment, int minimum_value, int maximum_value) {
  return std::min(maximum_value, this->uniform_mutation(base_value, maximum_increment, minimum_value));
};

float RandomNumberGenerator::uniform_mutation(float base_value){
  return this->uniform_mutation(base_value, maximum_increment = 1.0);
};

float RandomNumberGenerator::uniform_mutation(float base_value, float maximum_increment) {
  std::uniform_distribution<float> distribution(
    base_value - maximum_increment,
    base_value + maximum_increment
  );
  return distribution(this->eng);
};

float RandomNumberGenerator::uniform_mutation(float base_value, float maximum_increment, float minimum_value) {
  return std::max(minimum_value, this->uniform_mutation(base_value, maximum_increment));
};

float RandomNumberGenerator::uniform_mutation(float base_value, float maximum_increment, float minimum_value, float maximum_value)
{
  return std::min(maximum_value, this->uniform_mutation(base_value, maximum_increment, minimum_value));
};

