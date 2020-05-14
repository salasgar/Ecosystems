#include <chrono>
#include <random>
#include <iostream>
#include <numeric>
#include "ecosystem.h"
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

Sun_light::Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem)
  : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem) {}; // El tamaño de la matriz es 0x0, es decir, que no hay matriz.

float Sun_light::get_value(fLocation location) {
  return (1 + abs(sin(2 * M_PI * parent_ecosystem_ptr->cycle / 365.0))) * (1 + abs(sin(M_PI * location.second / float(parent_biotope_ptr->size_y))));
};
  
Temperature::Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem)
  : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem)  {
  data = {-10, 10, 30, 30, 10, -10}; // El tamaño de la matriz es 0x6, es decir, que hay 5 zonas climáticas que dependen únicamente de la latitud y no de la longitud.
};

float Temperature::get_value(tLocation location) {
  float y_float = float((data.size() - 1) * location.second)/this->parent_biotope_ptr->size_y;
  int y_int = int(std::trunc(y_float));
  y_float -= y_int;
  return data[y_int]*(1-y_float) + data[y_int + 1] * y_float;
};

void Temperature::update() {
  for(int y=0; y<data.size(); y++) {
    data[y] *= 0.95; // cada ciclo se pierde un 5% de la temperatura
    data[y] += parent_biotope_ptr->sun_light->get_value(
      fLocation(
        0,
        y * parent_biotope_ptr->size_y / (data.size()-1)
      )
    ); // y se gana tanta temperatura como luz solar haya en cada franja climática.
   }
};

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

Herbivore::Herbivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

Carnivore::Carnivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};




// ****************** OrganismsPool *********************
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

Biotope::Biotope(Ecosystem* parent_ecosystem) {
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  this->size_x = BIOTOPE_SIZE_X;
  this->size_y = BIOTOPE_SIZE_Y;
  this->parent_ecosystem_ptr = parent_ecosystem;
};

ErrorType Biotope::evolve() {
  this->temperature->update();
  return No_error;
};

Organism* Biotope::get_organism(tLocation location) {
  return this->organisms_map[location];
};

ErrorType Biotope::add_organism(Organism* new_organism_ptr, tLocation location) {
  this->organisms_map[location] = new_organism_ptr;
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
