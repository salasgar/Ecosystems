
// // // // // // // // // // // // // // // // // // // // //
//                                                          //
//    classes.hpp                                           //
//    Ecosystems                                            //
//                                                          //
//    Created on 28/05/2020 by:                             //
//                                                          //
//      Emilio Molina Martínez                              //
//      Juan Luis Salas García                              //
//                                                          //
//    Copyright © 2020 EMM & JLSG. All rights reserved.     //
//                                                          //
// // // // // // // // // // // // // // // // // // // // //

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

typedef enum OrganismType // AUTOMATIC
{
  NULL_ORGANISM_TYPE,
  ALL_TYPES,
  PLANT_A,
  PLANT_B,
  HERBIVORE,
  CARNIVORE
} OrganismType;

typedef enum OrganismAttribute // AUTOMATIC
{
  ENERGY_RESERVE,
  AGE,
  DEATH_AGE,
  GENERATION,
  PHOTOSYNTHESIS_CAPACITY,
  STRENGTH,
  MINIMUM_ENERGY_RESERVE_FOR_PROCREATING,
  ENERGY_RESERVE_AT_BIRTH,
  EATABLE_PLANT_TYPE, // this is not quantitative
  IDEAL_TEMPERATURE,
  MAX_TEMPERATURE_DEVIATION,
  MOVING_FREQUENCY
} OrganismAttribute;


typedef enum BiotopeAttribute // AUTOMATIC
{
  SUN_LIGHT,
  TEMPERATURE
} BiotopeAttribute;


class Plant_A; // AUTOMATIC
class Plant_B; // AUTOMATIC
class Herbivore; // AUTOMATIC
class Carnivore; // AUTOMATIC

class OrganismNode {
 public:
  // Connections:
  OrganismNode* prev;
  OrganismNode* next;
  // Attributes:
  OrganismType org_type;
  union {
    Plant_A* plant_A_ptr; // AUTOMATIC
    Plant_B* plant_B_ptr; // AUTOMATIC
    Herbivore* herbivore_ptr; // AUTOMATIC
    Carnivore* carnivore_ptr; // AUTOMATIC
  };
  // Methods:
  OrganismNode();
  void initialize(
    intLocation location,
    Biotope* biot_ptr,
    Ecosystem* ecos_ptr
  );
  float get_float_attribute(OrganismAttribute org_attr);
  void set_location(intLocation new_location);
  intLocation get_location();
  bool is_alive();
  void act();
  void unlink();
  void insert_before(OrganismNode* reference_organism);
  Ecosystem* get_parent_ecosystem_ptr();
};

template <class T>
class ObjectsPool {
 public:
  void create_more_objects();
  int buffer_size;
  std::vector<std::vector<T>> objects_pool;
  std::stack<T*> available_objects;
  // Methods:
  ObjectsPool();
  T* get_new();
  void set_available(T* object_ptr);
};

class NodeMaker {
 public:
  // 4 different types of organisms:
  ObjectsPool<Plant_A> plants_A_pool; // AUTOMATIC
  ObjectsPool<Plant_B> plants_B_pool; // AUTOMATIC
  ObjectsPool<Herbivore> herbivores_pool; // AUTOMATIC
  ObjectsPool<Carnivore> carnivores_pool; // AUTOMATIC
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
 public:
  // Connections:
  Ecosystem* parent_ecosystem_ptr;
  RandomNumbersGenerator* random_nums_gen_ptr;
  // Attributes:
  std::vector<OrganismNode*> organisms_vector;
  int size_x;
  int size_y;
  int area;
  std::vector<int> free_locs;
  int free_locs_counter;
  AdjacentLocationsPool adjacent_locations_pool;
  SunLight* sun_light;  // AUTOMATIC
  Temperature* temperature; // AUTOMATIC

 // methods:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  void initialize(RandomNumbersGenerator* random_nums_gen_ptr_);
  ErrorType evolve();
  OrganismNode* get_organism(intLocation location);
  void set_organism(intLocation location, OrganismNode* new_organism_ptr);
  void set_organism(OrganismNode* new_organism_ptr);
  void remove_organism(OrganismNode* organism_node);
  void move_organism(intLocation old_location, intLocation new_location);
  intLocation get_random_location();
  OrganismNode* get_random_organism();
  intLocation get_one_free_location();
  intLocation get_free_location_close_to(intLocation center, int radius);
  intLocation get_free_location_close_to(intLocation center, int radius, int number_of_attempts);
  intLocation get_free_adjacent_location(intLocation center);
  OrganismNode* get_adjacent_organism_of_type(intLocation center, OrganismType org_type);
  int get_num_organisms();
  intLocation normalize(intLocation location);
};

class SunLight { // AUTOMATIC or CUSTOM ?
 public:
  // connections:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  // methods:
  SunLight(Biotope* parent_biotope, Ecosystem* parent_ecosystem);
  float get_value(floatLocation location);
};

class Temperature { // AUTOMATIC or CUSTOM ?
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
  virtual void act();
  void set_location(intLocation new_location);
  void do_procreate();
  virtual void copy(Organism* parent);
  void mutate();
  void do_die();
  void unlink();
  // virtual bool decide_procreate();
};

class Plant_A : public Organism { // AUTOMATIC
  
  // class Plant_A:
public:
  // attributes:
  static const int photosynthesis_capacity = 100;
  float energy_reserve;
  float minimum_energy_reserve_for_procreating;
  float energy_reserve_at_birth;
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

class Plant_B : public Organism { // AUTOMATIC
  
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

class Herbivore : public Organism { // AUTOMATIC
public:
  float energy_reserve;
  float max_energy_reserve_capacity;
  float strength;
  OrganismType eatable_plant_type;
  //methods:
  Herbivore();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
  void do_internal_changes();
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

class Carnivore : public Organism { // AUTOMATIC
public:
  // attributes:
  float energy_reserve;
  float max_energy_reserve_capacity;
  float strength;
  float ideal_temperature;
  float max_temperature_deviation;
  float moving_frequency;
  float moving_time;
  // methods:
  Carnivore();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
  void do_internal_changes();
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

class SuperPredator : public Carnivore {
public:
  std::vector<u_char> V;
  SuperPredator();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void mutate();
};

// -----------------------------------------------------------------------
//                           P A T H O G E N
// -----------------------------------------------------------------------

class Pathogen{
 public:
  // Connections:
  OrganismNode* host_ptr;
  // Attributes:
  int antigen; // This is the pathogen's ID
  OrganismType target; // the type of organism that can infect
  float probability_of_contagion_each_cycle;
  float probability_of_killing_host_each_cycle;
  float probability_of_host_recovery_each_cycle;
  float probability_of_host_obtaining_immunity_after_infection;
  float probability_of_mutation_before_new_infection;
  //float radius_of_contagion_possibility;
  float percentage_of_energy_reserve_destroyed_by_desease_each_cycle;
  // Methods:
  Pathogen();
  void initialize(RandomNumbersGenerator* random_nums_gen_ptr);
  void set_host(OrganismNode* new_host);
  // actions:
  void act();
  void kill_host();
  void infect_new_host(OrganismNode* new_host);
  void spread(); // Look for new host closer than radius_of_contagion_possibility
  void steal_energy_reserve();
  void mutate();
};

// -----------------------------------------------------------------------
//                          S T A T I S T I C S
// -----------------------------------------------------------------------

class Statistics {
 public:
  // Connections:
  Biotope* parent_biotope_ptr;
  Ecosystem* parent_ecosystem_ptr;
  // Data:
  std::map<OrganismType, std::set<OrganismAttribute>> attributes_of_each_type;
  std::map<OrganismAttribute, std::set<OrganismType>> types_that_have_each_attribute;
  std::map<OrganismType, unsigned int> number_of_organisms_by_type;
  long int last_cycle_when_calculated_the_number_of_organisms_by_type;
  // Methods:
  Statistics();
  void initialize(Biotope* biot_ptr, Ecosystem* ecos_ptr);
  unsigned int get_number_of_organisms(OrganismType org_type);
  void calculate_number_of_organisms_by_type();
  float mean_of_attribute(OrganismAttribute org_attr, OrganismType org_type);
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
  NodeMaker node_maker;
  Statistics statistics;

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
  std::vector<float> get_attribute_matrix(OrganismAttribute org_attr, OrganismType org_type);
  void keep_number_of_organism_above(OrganismType org_type, int num_orgs);
};

/*
 COMANDOS GIT:
 
 // Send changes to repository:
 git add -u
 git commit -m "Rename few files"
 git push origin pruebas_cpp
 
 // See status:
 git status
 
 // Temporary hide or show last changes (uncommited changes):
 git stash
 git stash pop
 
 // Erase last changes in a file:
 git checkout filename.cpp
 
 // Update from repository:
 git pull origin pruebas_cpp
 
 */


class Matrix {
public:
  Matrix(Ecosystem &e, OrganismAttribute org_attr, OrganismType org_type);
  Matrix(Ecosystem &e, BiotopeAttribute bio_attr);
  float *data();
  size_t rows();
  size_t cols();
private:
  size_t m_rows, m_cols;
  vector<float> m_data;
};

#endif /* classes_hpp */
