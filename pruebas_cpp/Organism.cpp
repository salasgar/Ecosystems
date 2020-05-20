#include <chrono>
#include <random>
#include <iostream>
#include <numeric>
#include "Organism.hpp"
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

// plant_A: plantas que viven en sitios con POCA luz

Plant_A::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope),
data(initial_value)
{};

void Plant_A::Energy_reserve::update() {
  this->data += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(parent_organism_ptr->location));
};

bool Plant_A::decide_procreate() {
  return this->energy_reserve.get_value() > 200;
};

// plant_B: plantas que viven en sitio con MUCHA luz

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

void Organism::reset(pair<int, int> location,
                     Ecosystem* parent_ecosystem_ptr) {
  this->next = nullptr;
  this->prev = nullptr;
  this->location = location;
  this->parent_ecosystem_ptr = parent_ecosystem_ptr;
  this->is_alive = true;
  const int MAX_AGE = 2000;
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

Herbivore::Herbivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

Carnivore::Carnivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};
