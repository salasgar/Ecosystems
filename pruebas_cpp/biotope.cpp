#include <chrono>
//#include <random>
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


Sun_light::Sun_light(Biotope &parent_biotope, Base_ecosystem &parent_ecosystem)
  : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem) {}; // El tamaño de la matriz es 0x0, es decir, que no hay matriz.

float Sun_light::get_value(floatLocation location) {
  return (1 + abs(sin(2 * M_PI * parent_ecosystem_ptr->cycle / 365.0))) * (1 + abs(sin(M_PI * location.second / float(parent_biotope_ptr->size_y))));
};
  
Temperature::Temperature(Biotope &parent_biotope, Base_ecosystem &parent_ecosystem)
  : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem),
    data({-10, 10, 30, 30, 10, -10})
{
  // El tamaño de la matriz es 0x6, es decir, que hay 5 zonas climáticas que dependen únicamente de la latitud y no de la longitud.
};

float Temperature::get_value(intLocation location) {
  float y_float = float((data.size() - 1) * location.second)/this->parent_biotope_ptr->size_y;
  int y_int = int(std::trunc(y_float));
  y_float -= y_int;
  return data[y_int]*(1-y_float) + data[y_int + 1] * y_float;
};

void Temperature::update() {
  floatLocation loc(3.2, 3.3);
  
  for(int y=0; y<data.size(); y++) {
    data[y] *= 0.95; // cada ciclo se pierde un 5% de la temperatura
    floatLocation loc(
      0.0,
      float(y * parent_biotope_ptr->size_y) / (data.size()-1)
    );
    data[y] += parent_biotope_ptr->sun_light->get_value(loc); // y se gana tanta temperatura como luz solar haya en cada franja climática.
   }
};

Biotope::Biotope(Base_ecosystem* parent_ecosystem) {
  this->parent_ecosystem_ptr = parent_ecosystem;
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  this->size_x = BIOTOPE_SIZE_X;
  this->size_y = BIOTOPE_SIZE_Y;
  this->area = this->size_x * this->size_y;
  this->free_locs = std::vector<int> (this->size_x * this->size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng);
  this->free_locs_counter = 0;
  this->adjacent_locations = std::vector<intLocation> {
    make_int_location(-1, -1),
    make_int_location(-1,  0),
    make_int_location(-1,  1),
    make_int_location( 0, -1),
    make_int_location( 0,  1),
    make_int_location( 1, -1),
    make_int_location( 1,  0),
    make_int_location( 1,  1)
  };
};

ErrorType Biotope::evolve() {
  // Update those biotope features that need to be updated:
  this->temperature->update();
  return No_error;
};

Base_organism* Biotope::get_organism(intLocation location) {
  // TO DO: Check whether location belongs to this world or not
  return this->organisms_map[location];
};

ErrorType Biotope::add_organism(Base_organism* new_organism_ptr, intLocation location) {
  // if(his->organisms_map[location] == nullptr) ???
  this->organisms_map[location] = new_organism_ptr;
  return No_error;
};

ErrorType Biotope::move_organism(intLocation old_location, intLocation new_location) {
  // if(his->organisms_map[new_location] == nullptr) ???
  // if(his->organisms_map[old_location] != nullptr) ???
  organisms_map[new_location] = organisms_map[old_location];
  organisms_map[old_location] = nullptr;
  organisms_map[new_location]->change_location_to(new_location);
  return No_error;
};

int Biotope::get_num_organisms() {
  return (int)this->organisms_map.size();
};

intLocation Biotope::get_random_location() {
  this->free_locs_counter++;
  this->free_locs_counter %= this->area;
  if(this->free_locs_counter == 0)
    shuffle(this->free_locs.begin(), this->free_locs.end(),
            parent_ecosystem_ptr->random_nums_gen.eng);
  int packed_location = this->free_locs[this->free_locs_counter];
  return make_int_location(
                           packed_location / this->size_y,
                           packed_location % this->size_y
  );
};

vector<intLocation> Biotope::get_free_locations(int number_of_locations) {
  if(number_of_locations + this->get_num_organisms() > this->area)   // should it return error ??
    number_of_locations = this->area - this->get_num_organisms();
  vector<intLocation> free_locations;
  free_locations.reserve(number_of_locations); // reserve memory for number_of_locations locations
  for(int i=0; i<number_of_locations; i++) {
    intLocation loc = this->get_random_location();
    while(this->organisms_map[loc] != nullptr)
      loc = this->get_random_location();
    free_locations.push_back(loc);
  };
  return free_locations;
};

intLocation Biotope::get_one_free_location() {
  if(this->get_num_organisms() < this->area) {
    intLocation loc = this->get_random_location();
    while(organisms_map[loc] != nullptr)
      loc = this->get_random_location();
    return loc;
  }
  else {
    return make_int_location(1/0, 1/0); // return Error;
  };
};

ErrorType Biotope::get_free_location_close_to(intLocation &free_location, intLocation center, int radius) {
  // Use this method only with small radiuses. Otherwise, it's very time-consuming.
  std::vector<intLocation> free_locations_found = {};
  for(int x = center.x() - radius;
      x <= center.x() + radius;
      x++) {
    for(int y = center.y() - radius;
        y <= center.y() + radius;
        y++) {
      if(this->organisms_map[intLocation(x, y)] == nullptr)
        free_locations_found.push_back(intLocation(x, y));
    };
  };
  if(free_locations_found.size() == 0) {
    return Error_No_free_location_found;
  } else {
    free_location = free_locations_found[
      this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_int(0, free_locations_found.size())
    ];
    return No_error;
  };
};

ErrorType Biotope::get_free_location_close_to(intLocation &free_location, intLocation center, int radius, int number_of_attempts) {
  // This method is assumed to be used by some organisms in order to move themselves to another location. For organisms that jump very far away each time, it's very time-consuming to collect every single empty location within such a large radius, just to randomly chose one of them. That's why they should try a number of times and resign from moving if they don't find a place to do it in those attempts:
  for(int i=0; i<number_of_attempts; i++) {
    intLocation new_location = center + this->parent_ecosystem_ptr->random_nums_gen.get_rand_intLocation(radius);
    if(this->organisms_map[new_location] == nullptr) {
      free_location = new_location;
      return No_error;
    };
  };
  return Error_No_free_location_found;
};

ErrorType Biotope::get_free_adjacent_location(intLocation &free_location, intLocation center) {
  shuffle(
    this->adjacent_locations.begin(),
    this->adjacent_locations.end(),
    this->parent_ecosystem_ptr->random_nums_gen.eng
  );
  for(intLocation location : this->adjacent_locations) {
    if(this->organisms_map[center + location] == nullptr) {
      free_location = center + location;
      return No_error;
    };
  };
  return Error_No_free_location_found;
};

ErrorType Biotope::get_adjacent_organism_of_type(intLocation &org_loc, intLocation center, std::type_info org_type) {
  shuffle(
    this->adjacent_locations.begin(),
    this->adjacent_locations.end(),
    this->parent_ecosystem_ptr->random_nums_gen.eng
  );
  for(intLocation location : this->adjacent_locations) {
    if(this->organisms_map[center + location] != nullptr) {
      if(typeid(*(this->organisms_map[center + location])) == org_type) {
        org_loc = center + location;
        return No_error;
      };
    };
  };
  return Error_No_free_location_found;
};

