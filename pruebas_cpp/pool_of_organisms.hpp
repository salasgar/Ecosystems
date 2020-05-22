//
//  pool_of_organisms.hpp
//  Ecosystem
//
//  Created by Juan Luis Salas García on 15/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#ifndef pool_of_organisms_hpp
#define pool_of_organisms_hpp

#include "basic_tools.hpp"


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

#include <stdio.h>

#endif /* pool_of_organisms_hpp */
