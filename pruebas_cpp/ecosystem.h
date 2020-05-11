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
class clBaseFeature;
class Biotope;
class OrganismsPool;
class RandomNumbersGenerator;
template <class T> class Feature;
template <class T> class Feature2D;
template <class T> class EcosystemFeature;
template <class T> class EcosystemFeature2D;
template <class T> class BiotopeFeature;
template <class T> class BiotopeFeature2D;
template <class T> class OrganismFeature;
template <class T> class OrganismFeature2D;

class clBaseFeature {
 public:
  clBaseFeature();
  void update();
  void mutate();
};

template <class T>
class Feature : clBaseFeature {
 protected:
  T value;
 public:
  Feature(T initial_value);
  T get_value();
  void set_value(T new_value);
};

template <class T>
class Feature2D : clBaseFeature {
 protected:
  tLocation size; // matrix's dimensions
  T **matrix;
 public:
  Feature2D(tLocation size_);
  ~Feature2D();
  T get_value(tLocation location);
};

namespace biotope {

  class Sun_light : Feature2D<float> {
   public:
    float get_value(tLocation location);
    Sun_light(Biotope parentBiotope, tLocation size_);
  };

  class Temperature : Feature2D<Biotope, float> {
   public:
    Temperature(Biotope parent_, tLocation size_);
    void update();
  };

};

namespace plant_A {

  class Energy_reserve : Feature <Organism, float> {
    Energy_reserve(Organism parent_, float initial_value);
    void update();
  };

};

namespace plant_B {

  class Energy_reserve : Feature <Organism, float> {
    Energy_reserve(Organism parent_, float initial_value);
    void update();
  };

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

