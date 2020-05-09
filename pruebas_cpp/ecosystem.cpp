#include <chrono>
#include <random>
#include <iostream>
#include "ecosystem.h"

using std::tuple;
using std::get;
using std::make_tuple;
using std::default_random_engine;
using std::random_device;
using std::uniform_int_distribution;
using std::advance;
using std::vector;
using std::cout;
using std::endl;

default_random_engine eng((random_device())());

Biotope::Biotope() {
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  size_x = BIOTOPE_SIZE_X;
  size_y = BIOTOPE_SIZE_Y;
  for (int x = 0; x < this->size_x; x++) {
    for (int y = 0; y < this->size_y; y++) {
        this->free_locs.insert(make_tuple(x, y));
    }
  }
}

tuple<int, int> Biotope::get_random_free_location() {
  uniform_int_distribution<int> distribution(0, this->free_locs.size() - 1);
  auto it = this->free_locs.begin();
  int r = distribution(eng);
  advance(it, r);
  return *it;
}


void Ecosystem::_delete_dead_organisms() {
  for (auto dead_organism_ptr : this->dead_organisms_ptrs) {
    delete dead_organism_ptr;
  }
  this->dead_organisms_ptrs.clear();
}

void Ecosystem::evolve() {
  this->_delete_dead_organisms();
  // Create a vector of current organisms (needed because biotope is a map)
  vector<Organism*> organisms_to_act(this->get_num_organisms(), nullptr);
  int i = 0;
  for (auto kv : this->biotope.organisms_map) {
    organisms_to_act[i] = kv.second;
    i += 1;
  }
  // For each organism, act
  for (auto organism : organisms_to_act) {
    if (organism->is_alive) {;
      organism->act();
    }
  }
  this->time += 1;
}

Ecosystem::Ecosystem() {
  eng.seed(0);
  const int INITIAL_NUM_ORGANISMS = 100;
  for (int i=0; i < INITIAL_NUM_ORGANISMS; i++) {
    tuple<int, int> free_loc = this->biotope.get_random_free_location();
    this->add_organism(new Organism(free_loc, this));
  }
}

int Ecosystem::get_num_organisms() {
  return this->biotope.organisms_map.size();
}

int Ecosystem::get_num_free_locations() {
  return this->biotope.free_locs.size();
}

void Ecosystem::add_organism(Organism* organism_ptr) {
    this->biotope.organisms_map[organism_ptr->location] = organism_ptr;
    this->biotope.free_locs.erase(organism_ptr->location);
}

void Ecosystem::remove_organism(Organism* organism_ptr) {
    this->biotope.organisms_map.erase(organism_ptr->location);
    this->biotope.free_locs.insert(organism_ptr->location);
    this->dead_organisms_ptrs.push_back(organism_ptr);
}

Organism::Organism(tuple<int, int> location,
                   Ecosystem* parent_ecosystem_ptr) :
    location(location), is_alive(true), age(0),
    parent_ecosystem_ptr(parent_ecosystem_ptr) {
  const int MAX_AGE = 500;
  uniform_int_distribution<int> distribution(1, MAX_AGE);
  this->death_age = distribution(eng);
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
    this->is_alive = false;
    this->parent_ecosystem_ptr->remove_organism(this);
}