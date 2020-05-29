#ifndef ORGANISM_H_INCLUDED
#define ORGANISM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
//#include <random>
#include <stack>
#include <vector>
#include "basic_tools.hpp"
#include "pool_of_organisms.hpp"
#include "biotope.hpp"

class Sun_light;
class Temperature;

class Organism : public Base_organism {
 public:
  Organism* prev;
  Organism* next;
  bool is_alive;
  intLocation location;
  Biotope* parent_biotope_ptr;
  Ecosystem* parent_ecosystem_ptr;
 // methods:
  Organism() : Base_organism() {};
  void reset(intLocation location,
             Base_ecosystem* parent_ecosystem_ptr);
  virtual void copy(Organism* model_organism);
  virtual void act();
  void change_location_to(intLocation new_location);
  void do_procreate();
  void mutate();
  void do_die();
  void unlink();
  // virtual bool decide_procreate();
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
    void set_value(float new_value);
    float get_value();
  };

 // class Plant_A:
 public:
  static const int photosynthesis_capacity = 100;
  Energy_reserve energy_reserve;
  constexpr static const float initial_minimum_energy_reserve_for_procreating = 300;
  float minimum_energy_reserve_for_procreating;
  float energy_reserve_at_birth;
  constexpr static const float initial_energy_reserve_at_birth = 100;
  // methods:
  Plant_A();
  void act();
  void do_procreate();
  void copy(Plant_A *parent);
  void mutate();
  // decisions:
  bool decide_procreate();
  // costs:
  void subtract_costs_of_procreating(Plant_A *offspring);
}; // *************** class Plant_A ***************

class Plant_B : public Organism {

  class Energy_reserve {
   public:
    float data;
    Organism *parent_organism_ptr;
    Biotope *parent_biotope_ptr;
    Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value);
    void update();
    void set_value(float new_value);
    float get_value();
};

  // class Plant_B:
 public:
  static const int photosynthesis_capacity = 120;
  static const int death_age = 1000;
  constexpr static const float minimum_energy_reserve_for_procreating = 300;
  Energy_reserve energy_reserve;
  int age;
 public:
  Plant_B(Biotope *parentBiotope);
  void act();
  void do_procreate();
  void do_age();
  // decisions:
  bool decide_procreate();
  // costs:
  void subtract_costs_of_procreating(Plant_B *offspring);
};  // *************** class Plant_B ***************

class Herbivore : public Organism {
 public:
  float energy_reserve;
  float strength;
  std::type_info favorite_food;
 public:
  Herbivore(Biotope *parentBiotope);
  void do_move();
  void do_hunt();
  void do_eat(Plant_A *plant_a);
  void do_eat(Plant_B *plant_b);
  void do_procreate();
  void mutate();
  // constraints:
  bool can_procreate();
  // costs:
  void subtract_costs_of_procreating(Herbivore *offspring);
  void substract_costs_of_being_alive();
};

class Carnivore : public Organism {
 public:
  float energy_reserve;
  float strength;
  float moving_frequency;
  float moving_time;
  // methods:
  Carnivore(Biotope *parentBiotope);
  void act();
  void do_move();
  void do_hunt();
  void do_try_to_eat(Herbivore *herbivore);
  void do_eat(Herbivore *herbivore);
  void do_procreate();
  void mutate();
  // decisions:
  bool decide_move();
  bool decide_procreate();
  // costs:
  void substract_costs_of_moving(intLocation new_location);
  void subtract_costs_of_procreating(Carnivore *offspring);
  void substract_costs_of_being_alive();
};


#endif  // ORGANISM_H_INCLUDED
