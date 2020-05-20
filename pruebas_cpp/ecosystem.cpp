#include <chrono>
#include <random>
#include <iostream>
#include <numeric>
#include "ecosystem.hpp"
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
  };
};

void Ecosystem::append_organisms(Organism* organism) {
  if (this->first_organism_node == nullptr) {
    this->first_organism_node = organism;
  };
  while (organism != nullptr) {
    organism->prev = this->last_organism_node;
    if (this->last_organism_node != nullptr)
      this->last_organism_node->next = organism;
    this->last_organism_node = organism;
    this->biotope.organisms_map[organism->location] = organism;
    organism = organism->next;
  };
};

void Ecosystem::evolve() {
  this->_clear_ghost_organisms();
  this->biotope.evolve();
  Organism* organism = this->first_organism_node;
  while (organism != nullptr) {
    if (organism->is_alive) {
      organism->act();
    };
    organism = organism->next;
  };
  this->cycle += 1;
};


void Ecosystem::kill_and_remove_organism(Organism* organism) {
    organism->is_alive = false;
    biotope.organisms_map.erase(organism->location);
    organism->unlink();
    this->ghost_organisms_ptrs.push_back(organism);
};

int Ecosystem::get_num_organisms() {
  return (int)this->biotope.organisms_map.size();
};


