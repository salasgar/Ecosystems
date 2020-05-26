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
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) = NoError) {
      Organism* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->parent_ecosystem_ptr->subtract_costs_procreate(this, offspring);
    };
  // };
};

void Organism::copy(Organism* model_organism) {
  // nothing to do here yet
};

void Organism::mutate() {
  // nothing to do here yet
};

// plant_A: plants that can live with little sunlight

// class Plant_A::Energy_reserve
Plant_A::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope),
data(initial_value)
{};

Plant_A::Energy_reserve::get_value() {
  return data;
}

void Plant_A::Energy_reserve::update() { // do photosynthesis:
  this->data += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(parent_organism_ptr->location));
};

void Plant_A::Energy_reserve::set_value(float new_value) {
  this->data = new_value;
};
// end of definition of Plant_A::Energy_reserve

Plant_A::Plant_A() {
  this->minimum_energy_reserve_for_procreating = initial_minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = initial_energy_reserve_at_birth;
};

void Plant_A::do_procreate() {
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) = NoError) {
      Organism* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->parent_ecosystem_ptr->subtract_costs_procreate(this, offspring);
    };
  // };
};

void Plant_A::copy(Organism* model_organism) {
  this->minimum_energy_reserve_for_procreating = model_organism->minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = model_organism->energy_reserve_at_birth;
};

void Plant_A::mutate() {
  this->energy_reserve.set_value(this->energy_reserve_at_birth);
  this->energy_reserve_at_birth = this->parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->energy_reserve_at_birth, maximum_proportion = 0.015);
  this->minimum_energy_reserve_for_procreating = this->parent_ecosystem_ptr->random_nums_gen.uniform_mutation(this->minimum_energ_reserve_for_procreating, maximum_increment = 7.5, minimum_value = this->energy_reserve_at_birth);
};

bool Plant_A::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_A::act() {
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
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

bool Plant_B::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_B::act() {
  this->do_age();
  if(not this->is_alive) break;
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
};

Herbivore::Herbivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

Carnivore::Carnivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};
