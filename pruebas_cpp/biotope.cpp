#include <chrono>
#include <random>
#include <iostream>
#include <numeric>
#include "biotope.hpp"
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
  : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem),
    data({-10, 10, 30, 30, 10, -10})
{
  // El tamaño de la matriz es 0x6, es decir, que hay 5 zonas climáticas que dependen únicamente de la latitud y no de la longitud.
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

Biotope::Biotope(Ecosystem* parent_ecosystem) {
  this->parent_ecosystem_ptr = parent_ecosystem;
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  this->size_x = BIOTOPE_SIZE_X;
  this->size_y = BIOTOPE_SIZE_Y;
  this->area = this->size_x * this->size_y;
  this->free_locs = vector<int> (this->biotope.size_x * this->biotope.size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          parent_ecosystem->random_nums_gen.eng);
  this->free_locs_counter = 0;
};

ErrorType Biotope::evolve() {
  // Update those biotope features that need to be updated:
  this->temperature->update();
  return No_error;
};

Organism* Biotope::get_organism(tLocation location) {
  return this->organisms_map[location];
};

ErrorType Biotope::add_organism(Organism* new_organism_ptr, tLocation location) {
  // if(his->organisms_map[location] = null) ???
  this->organisms_map[location] = new_organism_ptr;
  return No_error;
};

ErrorType Biotope::move_organism(tLocation old_location, tLocation new_location) {
  // if(his->organisms_map[new_location] = null) ???
  // if(his->organisms_map[old_location] != null) ???
  organisms_map[new_location] = organisms_map[old_location];
  organisms_map[old_location] = nullptr;
  organisms_map[new_location]->change_location_to(new_location);
  return No_error;
};

int Biotope::get_num_organisms() {
  return (int)this->organisms_map.size();
};

tLocation Biotope::get_random_location() {
  this->free_locs_counter++;
  this->free_locs_counter %= this->area;
  if(this->free_locs_counter = 0)
    shuffle(this->free_locs.begin(), this->free_locs.end(),
            parent_ecosystem->random_nums_gen.eng);
  int location_int = this->free_locs[this->free_locs_counter];
  return tLocation(
    location_int / this->biotope.size_y;
    location_int % this->biotope.size_y;
  );
};

vector<tLocation> Biotope::get_free_locations(int number_of_locations) {
  if(number_of_locations + this->get_num_organisms() > this->area)
    number_of_locations = this->area - this->get;
  vector<tLocation> free_locations; // to do: reserve memory for number_of_locations locations
  for(int i=0; i<number_of_locations; i++) {
    tLocation loc = this->get_random_location();
    while(organisms_map[loc]) != nullptr)
      loc = this->get_random_location();
    free_locations.back(loc);
  };
  return free_locations;
};
