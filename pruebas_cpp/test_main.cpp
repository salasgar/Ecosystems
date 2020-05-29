#include <iostream>
#include "classes.hpp"

void test_organism() {
  Organism o;
  
}

void test_1() {
  Ecosystem e;
  for (int i=0; i<1000; i++) {
    e.evolve();
  }
  //assert (e.get_num_organisms() == 108739);
}

int main(int argc, char* argv[]) {
  //test_1();
  test_organism();
}
