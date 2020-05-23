
#include "basic_tools.hpp"

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
