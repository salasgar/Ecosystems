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

// ***************** clBaseFeature ******************

class clBaseFeature {
 public:
  clBaseFeature();
  void update();
  void mutate();
};

// ************ Feature ****** Feature2D **************

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

// ******* EcosystemFeature ****** EcosystemFeature2D *******

template <class T>
class EcosystemFeature : public Feature<T> {
 public:
  EcosystemFeature(Ecosystem parentEcosystem, T initial_value);
  T get_value(Ecosystem parentEcosystem);
  void set_value(T new_value);
  void update(Ecosystem parentEcosystem);
};

template <class T>
class EcosystemFeature2D : public Feature2D<T> {
 protected:
  tLocation size; // matrix's dimensions
  T **matrix;
 public:
  EcosystemFeature2D(Ecosystem parentEcosystem, tLocation size_);
  ~EcosystemFeature2D();
  T get_value(Ecosystem parentEcosystem, tLocation location);
  void update(Ecosystem parentEcosystem);
};

// ******** BiotopeFeature ****** BiotopeFeature2D *********

template <class T>
class BiotopeFeature : public Feature<T> {
 protected:
  T value;
 public:
  BiotopeFeature(Biotope parentBiotope, T initial_value);
  T get_value(Biotope parentBiotope);
  void set_value(T new_value);
  void update(Biotope parentBiotope);
};

template <class T>
class BiotopeFeature2D : public Feature2D<T> {
 protected:
  tLocation size; // matrix's dimensions
  T **matrix;
 public:
  BiotopeFeature2D(Biotope parentBiotope, tLocation size_);
  ~BiotopeFeature2D();
  T get_value(Biotope parentBiotope, tLocation location);
  void update(Biotope parentBiotope);
};

// ******** OrganismFeature ****** OrganismFeature2D *********

template <class T>
class OrganismFeature : public Feature<T> {
 protected:
  T value;
 public:
  OrganismFeature(Organism parentOrganism, T initial_value);
  T get_value(Organism parentOrganism);
  void set_value(T new_value);
  void update(Organism parentOrganism);
};

template <class T>
class OrganismFeature2D : public Feature2D<T> {
 protected:
  tLocation size; // matrix's dimensions
  T **matrix;
 public:
  OrganismFeature2D(Organism parentOrganism, tLocation size_);
  ~OrganismFeature2D();
  T get_value(Organism parentOrganism, tLocation location);
  void update(Organism parentOrganism);
};

// *************** custom features ****************

namespace biotope {

  class Sun_light : BiotopeFeature2D<float> {
   public:
    float get_value(Biotope parentBiotope, tLocation location);
    Sun_light(Biotope parentBiotope, tLocation size_);
  };

  class Temperature : BiotopeFeature2D<float> {
   public:
    Temperature(Biotope parentBiotope, tLocation size_);
    void update(Biotope parentBiotope);
  };

};

namespace plant_A {

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

