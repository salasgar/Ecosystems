
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
  ecosystem.initialize();
  ecosystem.create_new_organisms(PLANT_A, 5000);
  ecosystem.create_new_organisms(PLANT_B, 5000);
  ecosystem.create_new_organisms(HERBIVORE, 5000);
  ecosystem.create_new_organisms(CARNIVORE, 5000);
  for (int i=0; i<1000; i++) {
    cout << "cycle " << ecosystem.cycle << ENDL;
    ecosystem.evolve();
  };
};

void test_random_engine() {
  std::default_random_engine eng((std::random_device())());
  std::uniform_real_distribution<float> distribution(- 0.01, 0.01);
  cout << distribution(eng) << ENDL;
  cout << distribution(eng) << ENDL;
  cout << distribution(eng) << ENDL;
  cout << distribution(eng) << ENDL;
};


int main(int argc, char* argv[]) {
  //test_location();
  test_2();
  //test_organism();
  //Ecosystem ecosystem;
  //ecosystem.initialize();

};
