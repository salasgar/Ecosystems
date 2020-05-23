#ifndef ORGANISM_H_INCLUDED
#define ORGANISM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
//#include <random>
#include <stack>
#include <vector>
#include "basic_tools.hpp"

class Sun_light;
class Temperature;
class Ecosystem;
class Biotope;
class Organism;
class OrganismsPool;
class RandomNumbersGenerator;

class Organism {
 public:
  Organism* prev;
  Organism* next;
  bool is_alive;
  Ecosystem* parent_ecosystem_ptr;
  Biotope* parent_biotope_ptr;
  intLocation location;
 // methods:
  void reset(intLocation location,
             Ecosystem* parent_ecosystem_ptr);
  virtual void act();
  void do_die();
  void unlink();
  void change_location_to(intLocation new_location);
  void do_procreate();
  virtual bool decide_procreate();
  void mutate();
};

class Plant_A : public Organism {

  class Energy_reserve {
   public:
    float data;
    Organism *parent_organism_ptr;
    Biotope *parent_biotope_ptr;
    //methods:
    Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value);
    void update();
    float get_value(); // Is this method necessary?
  };

 // class Plant_A:
 public:
  static const int photosynthesis_capacity = 100;
  constexpr static const float initial_minimum_energy_reserve_for_procreating = 200;
  Energy_reserve energy_reserve;
  float minimum_energy_reserve_for_procreating;
 public:
  Plant_A();
  void do_photosynthesis();
  // decisions:
  bool decide_procreate();
}; // *************** class Plant_A ***************

class Plant_B : public Organism {

  class Energy_reserve {
   public:
    float data;
    Organism *parent_organism_ptr;
    Biotope *parent_biotope_ptr;
    Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value);
    void update();
  };

  // class Plant_B:
 public:
  static const int photosynthesis_capacity = 120;
  static const int death_age = 1000;
  Energy_reserve energy_reserve;
  int age;
 public:
  Plant_B(Biotope *parentBiotope);
  void do_photosynthesis();
  void do_age();
  void do_procreate();
  void act();
};  // *************** class Plant_B ***************

class Herbivore : public Organism {
 public:
  float energy_reserve;
 public:
  Herbivore(Biotope *parentBiotope);
  void do_move();
  void do_hunt();
  void do_eat(Plant_A plant_a);
  void do_eat(Plant_B plant_b);
};

class Carnivore : public Organism {
  public:
   float energy_reserve;
  public:
   Carnivore(Biotope *parentBiotope);
   void do_move();
   void do_hunt();
   void do_eat(Herbivore hervibore);
};


#endif  // ORGANISM_H_INCLUDED
