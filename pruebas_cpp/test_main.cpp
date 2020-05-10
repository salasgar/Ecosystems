#include <iostream>
#include "ecosystem.h"

int main(int argc, char* argv[]) {
  Ecosystem e;
  for (int i=0; i<1000; i++) {
    e.evolve();
  }
  std::cout << e.get_num_organisms() << std::endl;
}