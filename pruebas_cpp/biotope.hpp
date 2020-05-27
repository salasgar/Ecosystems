#ifndef BIOTOPE_H_INCLUDED
#define BIOTOPE_H_INCLUDED
#include <map>
#include <utility>
#include <set>
//#include <random>
#include <stack>
#include <vector>
#include <typeinfo>
#include "basic_tools.hpp"
#include "pool_of_organisms.hpp"

class Sun_light;
class Temperature;

class Biotope : public Base_biotope {
 public:
  int size_x;
  int size_y;
  int area;
  std::vector<int> free_locs;
  int free_locs_counter;
  std::vector<intLocation> adjacent_locations;
  std::map<intLocation, Base_organism*> organisms_map;
  Sun_light *sun_light;
  Temperature *temperature;
 
 // methods:
  Biotope(Base_ecosystem* parent_ecosystem_ptr);
  ErrorType evolve();
  Base_organism* get_organism(intLocation location);
  ErrorType add_organism(Base_organism* new_organism_ptr, intLocation location);
  ErrorType move_organism(intLocation old_location, intLocation new_location);
  intLocation get_random_location();
  intLocation get_one_free_location();
  std::vector<intLocation> get_free_locations(int number_of_locations);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius, int number_of_attempts);
  ErrorType get_free_adjacent_location(intLocation &free_location, intLocation center);
  ErrorType get_adjacent_organism_of_type(intLocation &org_loc, intLocation center, std::type_info org_type);
  int get_num_organisms();
};

class Sun_light {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Base_ecosystem *parent_ecosystem_ptr;
 public:
  float get_value(floatLocation location);
  Sun_light(Biotope &parent_biotope, Base_ecosystem &parent_ecosystem);
};

class Temperature {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Base_ecosystem *parent_ecosystem_ptr;
 public:
  Temperature(Biotope &parent_biotope, Base_ecosystem &parent_ecosystem);
  float get_value(intLocation location);
  void update();
};


#endif  // BIOTOPE_H_INCLUDED
