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

/*******************************
 Utils classes
 ********************************
 */
class Organisms_pool : public Base_organisms_pool {
  void _create_more_organisms();
public:
  int buffer_size;
  std::vector<std::vector<Base_organism> > organisms_pool;
  std::stack<Base_organism*> available_organisms;
  Base_organism* get_new(intLocation location,
                    Base_ecosystem* parent_ecosystem_ptr);
  void set_available(Base_organism* organism);
  Organisms_pool();
};

#include <stdio.h>

#endif /* pool_of_organisms_hpp */
