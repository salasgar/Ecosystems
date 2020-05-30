
#include "basic_tools.hpp"
#include "classes.hpp"

void test_location () {
  intLocation A(3, 5), B(6, 9), C;
  floatLocation D(6, 9);
  
  cout << "C" << string(C) << "\n";
  cout << "C" + C + "\n";
  cout << "D" + D + "\n";
  cout << "A" + floatLocation(A) + "\n";
  cout << "B - A = " << string(B - A) << "\n";
  cout << "B - A = " + (B - A) + "\n";
  cout << "d(A, B) = " << euclidean_distance(A, B) << "\n";
};

/*
void test_organism() {
  //Organism o;
  
};

void test_1() {
  Ecosystem e;
  for (int i=0; i<1000; i++) {
    e.evolve();
  };
  //assert (e.get_num_organisms() == 108739);
};
*/

void test_2() {
  Ecosystem ecosystem;
  ecosystem.create_new_organisms(PLANT_A, 5);
  ecosystem.create_new_organisms(PLANT_B, 5);
  ecosystem.create_new_organisms(HERBIVORE, 5);
  ecosystem.create_new_organisms(CARNIVORE, 5);
};


int main(int argc, char* argv[]) {
  //test_location();
  test_2();
  //test_organism();
};
