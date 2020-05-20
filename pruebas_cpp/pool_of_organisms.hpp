//
//  pool_of_organisms.hpp
//  Ecosystem
//
//  Created by Juan Luis Salas García on 15/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#ifndef pool_of_organisms_hpp
#define pool_of_organisms_hpp

#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
#include "Organism.hpp"

typedef std::pair<int, int> tLocation;
typedef std::pair<float, float> fLocation;
typedef enum {No_error, Error_Organism_not_found, Error_no_free_location_found} ErrorType;

class Organism;
class Ecosystem;



/*******************************
 Utils classes
 ********************************
 */
class OrganismsPool {
  void _create_more_organisms();
public:
  int buffer_size;
  std::vector<std::vector<Organism> > organisms_pool;
  std::stack<Organism*> available_organisms;
  Organism* get_new(std::pair<int, int> location,
                    Ecosystem* parent_ecosystem_ptr);
  void set_available(Organism* organism);
  OrganismsPool();
};

class RandomNumbersGenerator {
public:
  std::default_random_engine eng;
  RandomNumbersGenerator();
  void set_seed(int seed);
  int get_uniform_rand_int(int min, int max);
};






#include <stdio.h>

#endif /* pool_of_organisms_hpp */
