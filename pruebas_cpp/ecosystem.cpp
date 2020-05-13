#include <chrono>
#include <random>
#include <iostream>
#include <numeric>
#include "ecosystem.h"

using std::pair;
using std::get;
using std::make_pair;
using std::default_random_engine;
using std::random_device;
using std::uniform_int_distribution;
using std::advance;
using std::vector;
using std::cout;
using std::endl;
using std::iota;
using std::begin;
using std::end;

// ***************** Base class Feature ******************

Feature::Feature(
    Biotope &parent_biotope,
    Ecosystem &parent_ecosystem) {
  parent_biotope_ptr = &parent_biotope;
  parent_ecosystem_ptr = &parent_ecosystem;
  set_initial_value();
};

void Feature::update() {
  if(cycle_of_next_update >= parent_ecosystem_ptr->cycle) {
    // Update feature's value.
  };
  cycle_of_next_update += update_once_every();
};
  
void Feature::mutate() {};


// *************** custom features ****************



namespace biotope {

// TO DO: fix these examples:

  Sun_light::Sun_light(Biotope parentBiotope, tLocation size_)
    : Feature (parentBiotope,) {}; // El tamaño de la matriz es 0x0, es decir, que no hay matriz.

  float Sun_light::get_value(Biotope parentBiotope, tLocation location) {
    return 0; // En realidad habría que poner: return (1 + abs(sin(2 * pi * ecosystem.time/365))) * (1 + abs(sin(pi * location.second/biotope.size.y)))
  };
    
  Temperature::Temperature(Biotope parentBiotope, tLocation size_) : BiotopeFeature2D<float>(parentBiotope, tLocation(0, 5)){}; // El tamaño de la matriz es 0x5, es decir, que hay 5 zonas climáticas que dependen únicamente de la latitud y no de la longitud.

  void Temperature::update(Biotope parentBiotope) {
    for(int y=0; y<size.second; y++) {
      // matrix[0][y] += parentBiotope.Features['Sun light'].get_value(0, y) - 0.05 * matrix[0][y];
      // Es decir, que en cada ciclo se pierde un 5% de la temperatura y se gana tanta temperatura como luz solar haya en cada franja climática.
    }
  };
};

namespace plant_A { // plantas que viven en sitios con POCA luz
  
  Energy_reserve::Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value) : OrganismFeature<float>(parentOrganism, initial_value) {};

  void Energy_reserve::update(Biotope parentBiotope, Organism parentOrganism) {
    // value += -10 + 20 * parentBiotope.Features['Sun light'].get_value(parentBiotope, parentOrganism.location);
  };

  int Photosynthesis_capacity::get_value() {
    return Ph_capacity;
  };
};

namespace plant_B { // plantas que viven en sitio con MUCHA luz
   
  Energy_reserve::Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value) : OrganismFeature<float>(parentOrganism, initial_value) {};

  void Energy_reserve::update(Biotope parentBiotope, Organism parentOrganism) {
    // value += -25 + 34 * parentBiotope.Features['Sun light'].get_value(parentBiotope, parentOrganism.location);
  };

};



void OrganismsPool::_create_more_organisms() {
  this->organisms_pool.push_back(vector<Organism>(this->buffer_size));
  for (auto &o : this->organisms_pool.back()) {
    this->available_organisms.push(&o);
  }
};

OrganismsPool::OrganismsPool() {
  this->buffer_size = 100000;
  this->_create_more_organisms();
};

Organism* OrganismsPool::get_new(pair<int, int> location,
                                 Ecosystem* parent_ecosystem_ptr) {
  if (this->available_organisms.empty()) {
    this->_create_more_organisms();
  }
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

Biotope::Biotope(Ecosystem* parent_ecosystem) {
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  size_x = BIOTOPE_SIZE_X;
  size_y = BIOTOPE_SIZE_Y;
  parent_ecosystem_ptr = parent_ecosystem;
};

void Biotope::add_feature(Feature new_feature) {
  biotope_features_list.push_back(new_feature);
};

ErrorType Biotope::evolve() {
  for(int i=0; i<biotope_features_list.size(); i++) {
    biotope_features_list[i].update();
  };
  return No_error;
};

Organism* Biotope::get_organism(tLocation location) {
  return organisms_map[location];
};

ErrorType Biotope::add_organism(Organism* new_organism_ptr, tLocation location) {
  organisms_map[location] = new_organism_ptr;
  return No_error;
};

ErrorType Biotope::move_organism(tLocation old_location, tLocation new_location) {
  organisms_map[new_location] = organisms_map[old_location];
  organisms_map[old_location] = nullptr;
  organisms_map[new_location]->change_location(old_location, new_location);
  return No_error;
};

void Ecosystem::_clear_ghost_organisms() {
  for (auto &ghost_organism_ptr : this->ghost_organisms_ptrs) {
    this->organisms_pool.set_available(ghost_organism_ptr);
  };
  this->ghost_organisms_ptrs.clear();
};

Ecosystem::Ecosystem() : biotope(this) {
  this->random_nums_gen.set_seed(0);
  this->cycle = 0;
  const int INITIAL_NUM_ORGANISMS = 200000;
  this->first_organism_node = nullptr;
  this->last_organism_node = nullptr;
  vector<int> free_locs(this->biotope.size_x * this->biotope.size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          this->random_nums_gen.eng);
  int free_loc_int, loc_x, loc_y;
  for (int i=0; i < INITIAL_NUM_ORGANISMS; i++) {
    free_loc_int = free_locs.back();
    free_locs.pop_back();
    loc_x = free_loc_int / this->biotope.size_y;
    loc_y = free_loc_int % this->biotope.size_y;
    Organism* o = this->organisms_pool.get_new(make_pair(loc_x, loc_y), this);
    this->append_organisms(o);
  }
}

void Ecosystem::add_feature(Feature new_feature) {
  ecosystem_features_list.push_back(new_feature);
};

void Ecosystem::append_organisms(Organism* organism) {
  if (this->first_organism_node == nullptr) {
    this->first_organism_node = organism;
  }
  while (organism != nullptr) {
    organism->prev = this->last_organism_node;
    if (this->last_organism_node != nullptr)
      this->last_organism_node->next = organism;
    this->last_organism_node = organism;
    this->biotope.organisms_map[organism->location] = organism;
    organism = organism->next;
  }
}

void Ecosystem::evolve() {
  this->_clear_ghost_organisms();
  this->biotope.evolve();
  for(int i=0; i < ecosystem_features_list.size(); i++){
    ecosystem_features_list[i].update();
  }
  Organism* organism = this->first_organism_node;
  while (organism != nullptr) {
    if (organism->is_alive) {
      organism->act();
    }
    organism = organism->next;
  }
  this->cycle += 1;
}


void Ecosystem::kill_and_remove_organism(Organism* organism) {
    organism->is_alive = false;
    biotope.organisms_map.erase(organism->location);
    organism->unlink();
    this->ghost_organisms_ptrs.push_back(organism);
}

int Ecosystem::get_num_organisms() {
  return (int)this->biotope.organisms_map.size();
}

void Organism::reset(pair<int, int> location,
                     Ecosystem* parent_ecosystem_ptr) {
  this->next = nullptr;
  this->prev = nullptr;
  this->location = location;
  this->parent_ecosystem_ptr = parent_ecosystem_ptr;
  this->is_alive = true;
  this->age = 0;
  const int MAX_AGE = 2000;
  this->death_age =
    this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_int(
      1, MAX_AGE);
}

void Organism::act() {
  this->do_age();
}

void Organism::do_age() {
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  }
}

void Organism::do_die() {
    this->parent_ecosystem_ptr->kill_and_remove_organism(this);
}

void Organism::unlink() {
  if (this->next != nullptr)
    this->next->prev = this->prev;
  if (this->prev != nullptr)
    this->prev->next = this->next;
}
