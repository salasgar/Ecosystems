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
class Base_class_feature;
template <class T> class Feature;
template <class T> class OrganismFeature;
class OrganismsPool;
class RandomNumbersGenerator;

// ***************** Base class Feature ******************

class Base_class_feature { // Base class
 public:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  float cycle_of_next_update; // It doesn't have to be always integer
 public:
  Base_class_feature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  virtual void set_initial_value();
  virtual void update();
  virtual float update_once_every();
  // virtual void confine_into_boundaries();
};

template <class T>
class Feature : public Base_class_feature {
 public:
  Feature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  virtual T get_value();
  virtual T get_value(tLocation location);
};

template <class T>
class OrganismFeature : public Feature<T> {
 public:
  Organism *parent_organism_ptr;
  OrganismFeature(Organism &parent_organism, Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  virtual void mutate();
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
  int size_x;
  int size_y;
  std::map<std::pair<int, int>, Organism*> organisms_map;
  std::map<std::string, Base_class_feature> biotope_features_list;
 public:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  void add_feature(Base_class_feature new_feature);
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
  long int cycle;
  std::vector<Organism*> ghost_organisms_ptrs;
  Biotope biotope;
  std::vector<Base_class_feature> ecosystem_features_list;
 public:
  Ecosystem();
  void add_feature(Base_class_feature new_feature);
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
  std::vector<Base_class_feature> ecosystem_features_list;
 public:
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


namespace biotope {

  class Sun_light : Feature<float> {
   public:
    std::vector<float> data;
   public:
    float get_value(tLocation location);
    Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  };

  class Temperature : Feature<float> {
   public:
    std::vector<float> data;
  public:
    Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
    float get_value(tLocation location);
    void update();
  };

};

namespace plant_A {
  // Example of feature:

  class Photosynthesis_capacity : OrganismFeature<float> {
   public:
    static const int Ph_capacity = 100;
    float get_value();
  };

  class Energy_reserve : OrganismFeature<float> {
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update(Biotope parentBiotope, Organism parentOrganism);
  };

};

namespace plant_B {

  class Energy_reserve : OrganismFeature<float> {
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update(Biotope parentBiotope, Organism parentOrganism);
  };

};
