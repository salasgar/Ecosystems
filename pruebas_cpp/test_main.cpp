
#include <chrono>
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
  for (int i=0; i<10000; i++) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    cout << "cycle " << ecosystem.cycle << endl;
    cout << "num organisms: " << ecosystem.get_num_organisms() << endl;
    ecosystem.evolve();
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Elapsed time = " <<
                 std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() <<
                 "[ms]" << std::endl;
  };
};

void test_random_engine() {
  std::default_random_engine eng((std::random_device())());
  std::uniform_real_distribution<float> distribution(- 0.01, 0.01);
  cout << distribution(eng) << endl;
  cout << distribution(eng) << endl;
  cout << distribution(eng) << endl;
  cout << distribution(eng) << endl;
};

class PruebaRandomEngine {
 public:
  std::default_random_engine eng;
  std::uniform_real_distribution<float> distribution;
  PruebaRandomEngine() : eng((std::random_device())()), distribution(0, 100000000) {
    cout << "Constructor of PruebaRandomEngine" << endl;
    
  };
  float get() {
    int arr[5] = {2, 7, 10, 300, 5000};
    shuffle(begin(arr), end(arr), this->eng);
    this->distribution = std::uniform_real_distribution<float>(arr[0], arr[1]);
    cout << "[" << arr[0] << ", " << arr[1] << "] -> ";
    return this->distribution(this->eng);
  };
};

void test_ecosystem_initalize() {
  Ecosystem ecosystem;
  ecosystem.initialize();
};

void test_3() {
  Ecosystem ecosystem;
   ecosystem.initialize();
   ecosystem.create_new_organisms(PLANT_A, 20);
   ecosystem.create_new_organisms(PLANT_B, 20);
   ecosystem.create_new_organisms(HERBIVORE, 20);
   ecosystem.create_new_organisms(CARNIVORE, 20);
   for (int i=0; i<1000; i++) {
     std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
     cout << "cycle " << ecosystem.cycle << endl;
     cout << "num organisms: " << ecosystem.get_num_organisms() << endl;
     ecosystem.evolve();
     ecosystem.keep_number_of_organism_above(PLANT_A, 100);
     ecosystem.keep_number_of_organism_above(PLANT_B, 100);
     ecosystem.keep_number_of_organism_above(HERBIVORE, 100);
     ecosystem.keep_number_of_organism_above(CARNIVORE, 100);
     std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
     std::cout << "Elapsed time = " <<
                  std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() <<
                  "[ms]" << std::endl;
   };
};

int main(int argc, char* argv[]) {
  //test_location();
  test_2();
  //test_organism();
  //test_ecosystem_initalize();

};
