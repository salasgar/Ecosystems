
//
//  classes.hpp
//  Ecosystems
//
//  Created by Juan Luis Salas García on 28/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#ifndef classes_hpp
#define classes_hpp

#include "basic_tools.hpp"

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


class Organism;
class Biotope;
class Ecosystem;

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

class OrganismNode {
 public:
  OrganismNode* prev;
  OrganismNode* next;
  OrganismType org_type;
  union {
    Plant_A* plant_A_ptr;
    Plant_B* plant_B_ptr;
    Herbivore* herbivore_ptr;
    Carnivore* carnivore_ptr;
  };
  OrganismNode();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void set_location(intLocation new_location);
  intLocation get_location();
  bool is_alive();
  void act_if_alive();
  void unlink();
  void insert_before(OrganismNode* reference_organism);
};

template <class T>
class ObjectsPool {
 private:
  void create_more_objects();
  int buffer_size;
  std::vector<std::vector<T>> objects_pool;
  std::stack<T*> available_objects;
 public:
  ObjectsPool();
  T* get_new();
  void set_available(T* object_ptr);
};

class NodeMaker {
 public:
  // 4 different types of organisms:
  ObjectsPool<Plant_A> plants_A_pool;
  ObjectsPool<Plant_B> plants_B_pool;
  ObjectsPool<Herbivore> herbivores_pool;
  ObjectsPool<Carnivore> carnivores_pool;
  // and the nodes:
  ObjectsPool<OrganismNode> organism_nodes_pool;
  // methods:
  NodeMaker();
  OrganismNode* get_new(OrganismType org_type_);
  void set_available(OrganismNode* org_node);
};


// -----------------------------------------------------------------------
//                           B I O T O P E
// -----------------------------------------------------------------------

class SunLight;
class Temperature;

class Biotope {
 private:
  std::vector<OrganismNode*> organisms_map;
 public:
  int size_x;
  int size_y;
  int area;
  std::vector<int> free_locs;
  int free_locs_counter;
  std::vector<intLocation> adjacent_locations;
  SunLight* sun_light;
  Temperature* temperature;
  Ecosystem* parent_ecosystem_ptr;
 
 // methods:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  void initialize();
  ErrorType evolve();
  OrganismNode* get_organism(intLocation location);
  void set_organism(intLocation location, OrganismNode* new_organism_ptr);
  void set_organism(OrganismNode* new_organism_ptr);
  void remove_organism(OrganismNode* organism_node);
  void move_organism(intLocation old_location, intLocation new_location);
  intLocation get_random_location();
  intLocation get_one_free_location();
  intLocation get_free_location_close_to(intLocation center, int radius);
  intLocation get_free_location_close_to(intLocation center, int radius, int number_of_attempts);
  intLocation get_free_adjacent_location(intLocation center);
  OrganismNode* get_adjacent_organism_of_type(intLocation center, OrganismType org_type);
  int get_num_organisms();
  intLocation normalize(intLocation location);
};

class SunLight {
 public:
  // connections:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  // methods:
  SunLight(Biotope* parent_biotope, Ecosystem* parent_ecosystem);
  float get_value(floatLocation location);
};

class Temperature {
 public:
  // attributes:
  std::vector<float> data;
  // connections:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  // methods:
  Temperature(Biotope* parent_biotope, Ecosystem* parent_ecosystem);
  void initialize();
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
  OrganismNode* node;
  Biotope* parent_biotope_ptr;
  Ecosystem* parent_ecosystem_ptr;
  // methods:
  Organism();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
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
  Plant_A();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
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
  float photosynthesis_capacity();
  static const int death_age = 1000;
  constexpr static const float minimum_energy_reserve_for_procreating = 300;
  float energy_reserve;
  int age;
  // methods:
  Plant_B();
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
  //methods:
  Herbivore();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
  void do_move();
  void do_hunt();
  void do_eat(OrganismNode* food);
  void do_procreate();
  void copy(Herbivore* parent);
  void mutate();
  // constraints:
  bool can_procreate();
  // costs:
  void subtract_costs_of_procreating(Herbivore *offspring);
  void subtract_costs_of_being_alive();
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
  Carnivore();
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
  void subtract_costs_of_moving(intLocation new_location);
  void subtract_costs_of_procreating(Carnivore *offspring);
  void subtract_costs_of_being_alive();
};


// -----------------------------------------------------------------------
//                           E C O S Y S T E M
// -----------------------------------------------------------------------


class Ecosystem {
public:
  Biotope biotope;
  long int cycle;
  int number_of_organisms;
  RandomNumbersGenerator random_nums_gen;
  OrganismNode* first_organism_node;
  OrganismNode* last_organism_node;
  NodeMaker node_maker;

  std::vector<OrganismNode*> ghost_organisms_ptrs;
  
  // methods:
  Ecosystem();
  void initialize();
  void create_new_organisms(OrganismType organism_type, int number_of_new_organisms);
  void create_one_new_organism(OrganismType organism_type);
  void append_first_organism(OrganismNode* first_organism);
  void append_organism(OrganismNode* new_organism);
  void insert_new_organism_before(OrganismNode* new_organism, OrganismNode* reference_organism);
  int get_num_organisms();
  void evolve();
  void move_dead_organism_to_ghost_list(Organism* org);
  void clear_ghost_organisms();
};

/*
 COMANDOS GIT:
 
 git add -u
 git commit -m "Rename few files"
 git push origin pruebas_cpp
 
 */


#endif /* classes_hpp */
