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
  std::map<std::pair<int, int>, Organism*> organisms_map;
  Sun_light *sun_light;
  Temperature *temperature;
 public:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  ErrorType evolve();
  Organism* get_organism(tLocation location);
  ErrorType add_organism(Organism* new_organism_ptr, tLocation location);
  ErrorType move_organism(tLocation old_location, tLocation new_location);
  tLocation get_random_location();
  tLocation get_one_free_location();
  std::vector<tLocation> get_free_locations(int number_of_locations);
  int get_num_organisms();
};

class Sun_light {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  float get_value(fLocation location);
  Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
};

class Temperature {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  float get_value(tLocation location);
  void update();
};


#endif  // BIOTOPE_H_INCLUDED
