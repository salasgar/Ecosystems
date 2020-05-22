#ifndef BIOTOPE_H_INCLUDED
#define BIOTOPE_H_INCLUDED
#include <map>
#include <utility>
#include <set>
//#include <random>
#include <stack>
#include <vector>
#include "pool_of_organisms.hpp"

class Sun_light;
class Temperature;
class Ecosystem;
class Biotope;
class Organism;
class OrganismsPool;
class RandomNumbersGenerator;

class Biotope {
 public:
  Ecosystem* parent_ecosystem_ptr;
  int size_x;
  int size_y;
  int area;
  std::vector<int> free_locs;
  int free_locs_counter;
  std::vector<intLocation> adjacent_locations;
  std::map<std::pair<int, int>, Organism*> organisms_map;
  Sun_light *sun_light;
  Temperature *temperature;
 
 // methods:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  ErrorType evolve();
  Organism* get_organism(intLocation location);
  ErrorType add_organism(Organism* new_organism_ptr, intLocation location);
  ErrorType move_organism(intLocation old_location, intLocation new_location);
  intLocation get_random_location();
  intLocation get_one_free_location();
  std::vector<intLocation> get_free_locations(int number_of_locations);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius, int number_of_attempts);
  ErrorType get_free_adjacent_location(intLocation &free_location, intLocation center);
  int get_num_organisms();
};

class Sun_light {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  float get_value(floatLocation location);
  Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
};

class Temperature {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  float get_value(intLocation location);
  void update();
};


#endif  // BIOTOPE_H_INCLUDED
