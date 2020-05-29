//
//  pool_of_organisms.cpp
//  Ecosystem
//
//  Created by Juan Luis Salas García on 15/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#include "pool_of_organisms.hpp"

// ****************** OrganismsPool *********************
void Organisms_pool::_create_more_organisms() {
  this->organisms_pool.push_back(std::vector<Base_organism>(this->buffer_size));
  for (auto &o : this->organisms_pool.back()) {
    this->available_organisms.push(&o);
  }
};

Organisms_pool::Organisms_pool() {
  this->buffer_size = 100000;
  this->_create_more_organisms();
};

Base_organism* Organisms_pool::get_new(intLocation location, Base_ecosystem* parent_ecosystem_ptr) {
  if (this->available_organisms.empty()) {
    this->_create_more_organisms();
  };
  Base_organism* organism_ptr = this->available_organisms.top();
  this->available_organisms.pop();
  organism_ptr->reset(location, parent_ecosystem_ptr);
  return organism_ptr;
};

void Organisms_pool::set_available(Base_organism *organism_ptr) {
  this->available_organisms.push(organism_ptr);
};

