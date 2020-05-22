
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

