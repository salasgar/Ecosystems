#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>

typedef std::pair<int, int> tLocation;

class Organism;
class Ecosystem;
template <class T> class Feature;
template <class T> class Feature2D;
class Biotope;
class OrganismsPool;
class RandomNumbersGenerator;

template <class T>
class Feature {
 public:
  T value;
  Feature();
  T get_value();
  void set_value(T new_value);
  void update();
  void mutate();
};

template <class T>
class Feature2D : Feature<T**> {
 public:
  Feature2D();
  T get_value(tLocation location);
  void set_value(T new_value, tLocation location);
};

namespace biotope {

  class Sun_light : Feature2D<float> {
    float get_value(tLocation location);
    Sun_light();
    void set_value(float new_value, tLocation location);
  };

};

namespace plant_A {

  class Energy_reserve : Feature <float> {
    Energy_reserve();
    void update();
  };

};

namespace plant_B {

  class Energy_reserve : Feature <float> {
    Energy_reserve();
    void update();
  };

};

typedef float tipo_gordo[1000];

class feature_de_tipo_gordo : Feature<tipo_gordo*> {  // Como el tipo ocupa mucho, usamos un puntero al tipo ese
 public:
  tipo_gordo* get_value();
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
  Biotope();
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
};

#endif  // ECOSYSTEM_H_INCLUDED
