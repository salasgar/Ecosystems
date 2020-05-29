//
//  classes.hpp
//  Ecosystems
//
//  Created by Juan Luis Salas García on 28/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#ifndef classes_hpp
#define classes_hpp

#include <stdio.h>
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
#include <typeinfo>
#include <chrono>
#include <iostream>
#include "math.h"
#define _USE_MATH_DEFINES
#include <numeric>

using std::pair;
using std::get;
using std::make_pair;
using std::default_random_engine;
using std::random_device;
using std::uniform_int_distribution;
using std::advance;
using std::vector;
using std::cout;
using std::endl;
using std::iota;
using std::begin;
using std::end;

#include "basic_tools.hpp"

typedef enum OrganismType
{
  PLANT_A,
  PLANT_B,
  HERBIVORE,
  CARNIVORE
} OrganismType;

class Plant_A;
class Plant_B;
class Herbivore;
class Carnivore;

class Organism_node {
 public:
  Organism_node* prev;
  Organism_node* next;
  OrganismType org_type;
  union {
    Plant_A* plant_A_ptr;
    Plant_B* plant_B_ptr;
    Herbivore* herbivore_ptr;
    Carnivore* carnivore_ptr;
  };
  void set_location(intLocation new_location);
  intLocation get_location();
  void unlink();
  void insert_before(Organism_node* reference_organism);
};

template <class T>
class Objects_pool {
 private:
  void create_more_objects();
  int buffer_size;
  std::vector<std::vector<T>> objects_pool;
  std::stack<T*> available_objects;
 public:
  Objects_pool();
  T* get_new();
  void set_available(T* object_ptr);
};

class Node_maker {
 public:
  // 4 different types of organisms:
  Objects_pool<Plant_A> plants_A_pool;
  Objects_pool<Plant_B> plants_B_pool;
  Objects_pool<Herbivore> herbivores_pool;
  Objects_pool<Carnivore> carnivores_pool;
  // and the nodes:
  Objects_pool<Organism_node> organism_nodes_pool;
  // methods:
  Node_maker()
    : plants_A_pool(),
      plants_B_pool(),
      herbivores_pool(),
      carnivores_pool(),
      organism_nodes_pool() {};
  Organism_node* get_new(OrganismType org_type_);
  void set_available(Organism_node* org_node);
};


// -----------------------------------------------------------------------
//                           B I O T O P E
// -----------------------------------------------------------------------

class Sun_light;
class Temperature;

class Biotope {
 public:
  int size_x;
  int size_y;
  int area;
  std::vector<int> free_locs;
  int free_locs_counter;
  std::vector<intLocation> adjacent_locations;
  std::map<intLocation, Organism_node*> organisms_map;
  Sun_light *sun_light;
  Temperature *temperature;
  Ecosystem* parent_ecosystem_ptr;
 
 // methods:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  ErrorType evolve();
  Organism_node* get_organism(intLocation location);
  ErrorType add_organism(Organism_node* new_organism_ptr, intLocation location);
  ErrorType move_organism(intLocation old_location, intLocation new_location);
  intLocation get_random_location();
  intLocation get_one_free_location();
  std::vector<intLocation> get_free_locations(int number_of_locations);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius);
  ErrorType get_free_location_close_to(intLocation &free_location, intLocation center, int radius, int number_of_attempts);
  ErrorType get_free_adjacent_location(intLocation &free_location, intLocation center);
  Organism_node* get_adjacent_organism_of_type(intLocation center, OrganismType org_type);
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


// -----------------------------------------------------------------------
//                           O R G A N I S M
// -----------------------------------------------------------------------

class Organism {
public:
  // attributes:
  bool is_alive;
  intLocation location;
  // connections:
  Organism_node* node;
  Biotope* parent_biotope_ptr;
  Ecosystem* parent_ecosystem_ptr;
  // methods:
  Organism() {};
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void reset(intLocation location, Ecosystem* ecos_ptr);
  void reset(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  virtual void copy(Organism* parent);
  virtual void act();
  void set_location(intLocation new_location);
  void do_procreate();
  void mutate();
  void do_die();
  void unlink();
  // virtual bool decide_procreate();
};

class Plant_A : public Organism {
  
  // class Plant_A:
public:
  // attributes:
  static const int photosynthesis_capacity = 100;
  float energy_reserve;
  constexpr static const float initial_minimum_energy_reserve_for_procreating = 300;
  float minimum_energy_reserve_for_procreating;
  float energy_reserve_at_birth;
  constexpr static const float initial_energy_reserve_at_birth = 100;
  // methods:
  Plant_A() {};
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  // void reset(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);   // No es necesaria de momento
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
  
  // class Plant_B:
public:
  // attributes:
  float photosynthesis_capacity() { return sqrt(this->age + this->energy_reserve); };
  static const int death_age = 1000;
  constexpr static const float minimum_energy_reserve_for_procreating = 300;
  float energy_reserve;
  int age;
  // methods:
  Plant_B() {};
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
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
  OrganismType eatable_plant_type;
public:
  Herbivore() {};
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
  void do_move();
  void do_hunt();
  void do_eat(Organism_node* food);
  void do_procreate();
  void reset(intLocation location,
             Ecosystem* parent_ecosystem_ptr);
  void copy(Herbivore* parent);
  void mutate();
  // constraints:
  bool can_procreate();
  // costs:
  void subtract_costs_of_procreating(Herbivore *offspring);
  void substract_costs_of_being_alive();
};

class Carnivore : public Organism {
public:
  // attributes:
  float energy_reserve;
  float strength;
  float ideal_temperature;
  float max_temperature_deviation;
  float moving_frequency;
  float moving_time;
  // methods:
  Carnivore() {};
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
  void do_move();
  void do_hunt();
  void do_try_to_eat(Herbivore *herbivore);
  void do_eat(Herbivore *herbivore);
  void do_procreate();
  void copy(Carnivore* parent);
  void mutate();
  // decisions:
  bool decide_move();
  bool decide_procreate();
  // constraints:
  bool can_procreate();
  // costs:
  void substract_costs_of_moving(intLocation new_location);
  void subtract_costs_of_procreating(Carnivore *offspring);
  void substract_costs_of_being_alive();
};


// -----------------------------------------------------------------------
//                           E C O S Y S T E M
// -----------------------------------------------------------------------


class Ecosystem {
public:
  Biotope biotope;
  long int cycle;
  RandomNumbersGenerator random_nums_gen;
  Organism_node* first_organism_node;
  Organism_node* last_organism_node;
  Node_maker node_maker;

  std::vector<Organism_node*> ghost_organisms_ptrs;
  
  // methods:
  Ecosystem();
  void insert_new_organism_before(Organism_node* new_organism, Organism_node* reference_organism);
  void append_organism(Organism_node* new_node);
  void append_organisms(Organism* organisms);
  void evolve();
  void kill_and_remove_organism(intLocation location);
  void kill_and_remove_organism(Organism_node* organism_node);
  void add_new_organisms(OrganismType organism_type, int number_of_new_organisms);
  Organism_node* create_new_organism(OrganismType organism_type);
  int get_num_organisms();
  void clear_ghost_organisms();
};

/*
 COMANDOS GIT:
 
 git add -u
 git commit -m "Rename few files"
 git push origin pruebas_cpp
 
 */

#endif /* classes_hpp */
