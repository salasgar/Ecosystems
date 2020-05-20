//
//  pool_of_organisms.cpp
//  Ecosystem
//
//  Created by Juan Luis Salas García on 15/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#include "pool_of_organisms.hpp"

// ****************** OrganismsPool *********************
void OrganismsPool::_create_more_organisms() {
  this->organisms_pool.push_back(std::vector<Organism>(this->buffer_size));
  for (auto &o : this->organisms_pool.back()) {
    this->available_organisms.push(&o);
  }
};

OrganismsPool::OrganismsPool() {
  this->buffer_size = 100000;
  this->_create_more_organisms();
};

Organism* OrganismsPool::get_new(std::pair<int, int> location,
                                 Ecosystem* parent_ecosystem_ptr) {
  if (this->available_organisms.empty()) {
    this->_create_more_organisms();
  };
  Organism* o = this->available_organisms.top();
  this->available_organisms.pop();
  o->reset(location, parent_ecosystem_ptr);
  return o;
};

void OrganismsPool::set_available(Organism *o) {
  this->available_organisms.push(o);
};

RandomNumbersGenerator::RandomNumbersGenerator() :
eng((random_device())()) {
};


void RandomNumbersGenerator::set_seed(int seed) {
  this->eng.seed(seed);
};

int RandomNumbersGenerator::get_uniform_rand_int(int min, int max) {
  uniform_int_distribution<int> distribution(min, max);
  return distribution(this->eng);
};
