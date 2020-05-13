#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>

typedef std::pair<int, int> tLocation;
typedef enum {No_error, Error_Organism_not_found, Error_no_free_location_found} ErrorType;

class Organism;
class Ecosystem;
class Biotope;
class Feature;
class OrganismsPool;
class RandomNumbersGenerator;

// ***************** Base class Feature ******************

class Feature { // Base class
 public:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  float cicle_of_next_update; // It doesn't have to be always integer
 public:
  Feature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  virtual void set_initial_value();
  virtual void update();
  virtual float update_once_every();
  virtual void mutate();
  virtual void confine_into_boundaries();
};



class OrganismsPool {
  void _create_more_organisms();
 public:
  int buffer_size;
  std::vector<std::vector<Organism> > organisms_pool;
  std::stack<Organism*> available_organisms;
  Organism* get_new(std::pair<int, int> location,
                    Ecosystem* parent_ecosystem_ptr);
  void set_available(Organism* organism);
  OrganismsPool();
};

class RandomNumbersGenerator {
 public:
  std::default_random_engine eng;
  RandomNumbersGenerator();
  void set_seed(int seed);
  int get_uniform_rand_int(int min, int max);
};

class Biotope {
 public:
  Ecosystem* parent_ecosystem_ptr;
  long int cicle;
  int size_x;
  int size_y;
  std::map<std::pair<int, int>, Organism*> organisms_map;
  std::vector<Feature> Features_list;
 public:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  void add_feature(Feature new_feature);
  ErrorType evolve();
  Organism* get_organism(tLocation location);
  ErrorType add_organism(Organism* new_organism_ptr, tLocation location);
  ErrorType move_organism(tLocation old_location, tLocation new_location);
};

class Ecosystem {
  void _clear_ghost_organisms();
 public:
  Organism* first_organism_node;
  Organism* last_organism_node;
  RandomNumbersGenerator random_nums_gen;
  OrganismsPool organisms_pool;
  int time;
  std::vector<Organism*> ghost_organisms_ptrs;
  Biotope biotope;
  Ecosystem();
  void append_organisms(Organism* organisms);
  void evolve();
  void kill_and_remove_organism(Organism* organism);
  int get_num_organisms();
};

class Organism {
 public:
  Organism* prev;
  Organism* next;
  bool is_alive;
  Ecosystem* parent_ecosystem_ptr;
  std::pair<int, int> location;
  int age;
  int death_age;
  void reset(std::pair<int, int> location,
             Ecosystem* parent_ecosystem_ptr);
  void act();
  void do_age();
  void do_die();
  void unlink();
  void change_location(tLocation old_location, tLocation new_location);
};

#endif  // ECOSYSTEM_H_INCLUDED

// *************** custom features ****************

int Photosynthesis_capacity::get_value() {
  return Ph_capacity;
};

namespace biotope {

  class Sun_light : Feature {
   public:
    std::vector<float> data;
    Biotope *parent_biotope_ptr;
   public:
    float get_value(tLocation location);
    Sun_light(tLocation size_);
  };

  class Temperature : Feature {
   public:
    std::vector<float> data;
    Biotope *parent_biotope_ptr;
   public:
    Temperature(tLocation size_);
    void update();
  };

};

namespace plant_A {
  // Example of feature:

  class Photosynthesis_capacity : Feature {
   public:
    static const int Ph_capacity = 100;
    int get_value();
  };

  class Energy_reserve : OrganismFeature <float> {
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update(Biotope parentBiotope, Organism parentOrganism);
  };

};

namespace plant_B {

  class Energy_reserve : OrganismFeature <float> {
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update(Biotope parentBiotope, Organism parentOrganism);
  };

};
