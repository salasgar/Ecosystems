#include "classes.hpp"

void test_organism() {
  Organism o;
  
};

void test_1() {
  Ecosystem e;
  for (int i=0; i<1000; i++) {
    e.evolve();
  };
  //assert (e.get_num_organisms() == 108739);
};

void test_2() {
  Ecosystem ecosystem;
  ecosystem.create_new_organisms(PLANT_A, 5000);
  ecosystem.create_new_organisms(PLANT_B, 5000);
  ecosystem.create_new_organisms(HERBIVORE, 5000);
  ecosystem.create_new_organisms(CARNIVORE, 5000);
};

int main(int argc, char* argv[]) {
  //test_1();
  test_organism();
};
