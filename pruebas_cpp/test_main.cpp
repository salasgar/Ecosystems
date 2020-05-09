#include <iostream>
#include "ecosystem.h"

int main(int argc, char* argv[]) {
  Ecosystem e;
  for (int i=0; i<100; i++) {
    e.evolve();
  }
}