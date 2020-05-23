#include <chrono>
//#include <random>
#include <iostream>
#include <numeric>
#include "organism.hpp"
#include "math.h"
#define _USE_MATH_DEFINES

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

// class Organism:

void Organism::reset(pair<int, int> location,
                     Ecosystem* parent_ecosystem_ptr) {
  this->next = nullptr;
  this->prev = nullptr;
  this->location = location;
  this->parent_ecosystem_ptr = parent_ecosystem_ptr;
  this->is_alive = true;
  // const int MAX_AGE = 2000;
};

void Organism::act() {};

void Organism::do_die() {
  this->parent_ecosystem_ptr->kill_and_remove_organism(this);
};

void Organism::unlink() {
  if (this->next != nullptr)
    this->next->prev = this->prev;
  if (this->prev != nullptr)
    this->prev->next = this->next;
};

void Organism::change_location_to(intLocation new_location) {
  this->location = new_location;
};

void Organism::do_procreate() {
  if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) = NoError) {
      Organism* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
    };
  };
};

void Organism::mutate() {
  
};

// plant_A: plants that can live with little sunlight

// class Plant_A::Energy_reserve
Plant_A::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope),
data(initial_value)
{};

Plant_A::Energy_reserve::get_value() {
  return data;
}

void Plant_A::Energy_reserve::update() {
  this->data += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(parent_organism_ptr->location));
};
// end of definition of Plant_A::Energy_reserve

Plant_A::Plant_A() {
  this->minimum_energy_reserve_for_procreating = initial_minimum_energy_reserve_for_procreating;
}

bool Plant_A::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

// plant_B: plants that need much sunlight

Plant_B::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope), data(initial_value) {};

void Plant_B::Energy_reserve::update() {
  this->data += -25 + 34 * (this->parent_biotope_ptr->sun_light->get_value(parent_organism_ptr->location));
};

Plant_B::Plant_B(Biotope *parentBiotope) : energy_reserve(parentBiotope, this, 1000.0), age(0) {};

void Plant_B::do_age() {
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  };
};

void Plant_B::act() {
  this->do_age();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
};


Herbivore::Herbivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

Carnivore::Carnivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};
