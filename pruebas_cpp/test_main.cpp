#include <iostream>
#include "ecosystem.hpp"

void test_organism() {
  Organism o;
  
}

void test_1() {
  Ecosystem e;
  for (int i=0; i<1000; i++) {
    e.evolve();
  }
  std::cout << e.get_num_organisms() << std::endl;
}

int main(int argc, char* argv[]) {
  //test_1();
  test_organism();
}
