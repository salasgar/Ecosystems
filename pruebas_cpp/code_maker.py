import string


def type_name(token):
    return string.upper(variable_name(token))


def variable_name(token):
    if string.islower(token):
        return token.replace(' ', '_')
    if string.isupper(token):
        return string.lower(token).replace(' ', '_')
    result_token = string.lower(token[0])
    for letter in token[1:]:
        if string.isupper(letter):
            result_token += '_' + string.lower(letter)
        result_token += letter
    return result_token

def class_name(token):
    if string.isupper(token) or string.islower(token):
        result_token = ""
        next_upper = true
        for letter in token:
            if letter == '_':
                next_upper = true
            else:
                if next_upper:
                    result_token += string.upper(letter)
                    next_upper = false
                else:
                    result_token += string.lower(letter)
        return result_token
    else:
        return token





# Information extracted from settings:
organisms_types_matrix = [
    ['PLANT_A', 'Plant_A', 'plant_A', 'plants_A'],
    ['PLANT_B', 'Plant_B', 'plant_B', 'plants_B'],
    ['HERBIVORE', 'Herbivore', 'herbivore', 'herbivores'],
    ['CARNIVORE', 'Carnivore', 'carnivore', 'carnivores']
]

organisms_types = {}

for vector in organisms_types_matrix:
    organisms_types[vector[0]] = {
        'type name': vector[0],
        'class name': vector[1],
        'variable name': vector[2],
        'plural': vector[3]
    }


def get_organisms_types_vector(label):
    return [organisms_types[type_name][label] for type_name in organisms_types]


organisms_type_names = get_organisms_types_vector('type name')
organisms_types_class_names = get_organisms_types_vector('class name')
organisms_types_variable_names = get_organisms_types_vector('variable name')
organisms_types_variable_plural_names = get_organisms_types_vector('plural')

organism_types_attributes_declaration = [

    # Plant_A:
    """  static const int photosynthesis_capacity = 100;
  float energy_reserve;
  float minimum_energy_reserve_for_procreating;
  float energy_reserve_at_birth;
""",

    # Plant_B:
    """  float photosynthesis_capacity();
  static const int death_age = 1000;
  constexpr static const float minimum_energy_reserve_for_procreating = 300;
  float energy_reserve;
  int age;
""",

    # Herbivore:
    """  float energy_reserve;
  float max_energy_reserve_capacity;
  float strength;
  OrganismType eatable_plant_type;
""",

    # Carnivore:
    """  float energy_reserve;
  float max_energy_reserve_capacity;
  float strength;
  float ideal_temperature;
  float max_temperature_deviation;
  float moving_frequency;
  float moving_time;
"""
]
organisms_attributes = ['ENERGY RESERVE', 'AGE', 'DEATH AGE', 'GENERATION',
    'PHOTOSYNTHESIS CAPACITY',
    'STRENGTH',
    'MINIMUM ENERGY RESERVE FOR PROCREATING', 'ENERGY RESERVE AT BIRTH',
    'EATABLE PLANT TYPE', 'IDEAL TEMPERATURE', 'MAX TEMPERATURE DEVIATION',
    'MOVING FREQUENCY']

organisms_types_actions_declaration = [

    # Plant_A:
    """  void do_procreate();
  void copy(Plant_A *parent);
  void mutate();
""",

    # Plant_B:
    """  void do_procreate();
  void do_age();
""",

    # Herbivore:
    """  void do_internal_changes();
  void do_move();
  void do_hunt();
  void do_eat(OrganismNode* food);
  void do_procreate();
  void copy(Herbivore* parent);
  void mutate();
""",

    # Carnivore:
    """  void do_internal_changes();
  void do_move();
  void do_hunt();
  void do_try_to_eat(Herbivore *herbivore);
  void do_eat(Herbivore *herbivore);
  void do_procreate();
  void copy(Carnivore* parent);
  void mutate();
"""
]


organisms_types_decisions_declaration = [

    # Plant_A:
    """  bool decide_procreate();
""",

    # Plant_B:
    """  bool decide_procreate();
""",

    # Herbivore:
    """""",

    # Carnivore:
    """  bool decide_move();
  bool decide_procreate();
"""
]

organisms_types_constraints_declaration = [

    # Plant_A:
    """""",

    # Plant_B:
    """""",

    # Herbivore:
    """  bool can_procreate();
""",

    # Carnivore:
    """  bool can_procreate();
"""
]

organisms_types_costs_declaration = [

    # Plant_A:
    """  void subtract_costs_of_procreating(Plant_A *offspring);
""",

    # Plant_B:
    """  void subtract_costs_of_procreating(Plant_B *offspring);
""",

    # Herbivore:
    """  void subtract_costs_of_procreating(Herbivore *offspring);
  void subtract_costs_of_being_alive();
""",

    # Carnivore:
    """  void subtract_costs_of_moving(intLocation new_location);
  void subtract_costs_of_procreating(Carnivore *offspring);
  void subtract_costs_of_being_alive();
"""
]

biotope_features_class_names = ['SunLight', 'Temperature']
biotope_features_variable_names = ['sun_light', 'temperature']
biotope_features_data = ['', '  std::vector<float> data;']

# making code:


def transpose_dict(dictionary):
    key0 = dictionary.keys()[0]
    return [
        dict((key, dictionary[key][i]) for key in dictionary)
        for i in range(len(dictionary[key0]))
    ]


def repeat_with(text, dictionary):
    tr_dict = transpose_dict(dictionary)
    result_text = ""
    for i in range(len(tr_dict)):
        one_iteration = text
        for key in tr_dict[i]:
            one_iteration = one_iteration.replace(key, tr_dict[i][key])
        result_text += one_iteration
    return result_text


classes_hpp = """

// // // // // // // // // // // // // // // // // // // // //
//                                                          //
//    classes.hpp                                           //
//    Ecosystems                                            //
//                                                          //
//    Created on 28/05/2020 by:                             //
//                                                          //
//      Emilio Molina Martinez                              //
//      Juan Luis Salas Garcia                              //
//                                                          //
//    Copyright @ 2020 EMM & JLSG. All rights reserved.     //
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
"""


classes_hpp += repeat_with('  #,\n', {'#': organisms_type_names})[:-2]


classes_hpp += """
} OrganismType;

typedef enum OrganismAttribute // AUTOMATIC
{
"""


classes_hpp += repeat_with('  #,\n', {'#': organisms_attributes})[:-2]


classes_hpp += """
} OrganismAttribute;

"""


classes_hpp += repeat_with('class #;\n', {'#': organisms_types_class_names})


classes_hpp += """
class OrganismNode {
 public:
  // Connections:
  OrganismNode* prev;
  OrganismNode* next;
  // Attributes:
  OrganismType org_type;
  union {
"""


dictionary = {
    '#1': organisms_types_class_names,
    '#2': organisms_types_variable_names
}

classes_hpp += repeat_with('    #1* #2_ptr;\n', dictionary)


classes_hpp += """  };
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
"""


if len(organisms_types) > 1:
    classes_hpp += """  // {} different types of organisms:
""".format(len(organisms_types))


dictionary = {
    '#1': organisms_types_class_names,
    '#2': organisms_types_variable_plural_names
}


classes_hpp += repeat_with('  ObjectsPool<#1> #2_pool;\n', dictionary)


classes_hpp += """
  // and the nodes:
  ObjectsPool<OrganismNode> organism_nodes_pool;
  // methods:
  NodeMaker();
  OrganismNode* get_new(OrganismType org_type_);
  void set_available(OrganismNode* org_node);
};


// --------------------------------------------------------------------
//                           B I O T O P E
// --------------------------------------------------------------------

"""


classes_hpp += repeat_with('class #;\n', {'#': biotope_features_class_names})


classes_hpp += """
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
"""


classes_hpp += repeat_with('  #1* #2;\n', {
    '#1': biotope_features_class_names,
    '#2': biotope_features_variable_names}
)


classes_hpp += """
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
  intLocation get_free_location_close_to(intLocation center, int radius,
    int number_of_attempts);
  intLocation get_free_adjacent_location(intLocation center);
  OrganismNode* get_adjacent_organism_of_type(intLocation center,
    OrganismType org_type);
  int get_num_organisms();
  intLocation normalize(intLocation location);
};

"""


classes_hpp += repeat_with("""
class #1 {
 public:
  // attributes:
#2
  // connections:
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
  // methods:
  #(Biotope* parent_biotope, Ecosystem* parent_ecosystem);
  void initialize();
  float get_value(intLocation location);
  void update();
};

""", {'#1': biotope_features_class_names, '#2': biotope_features_data})


classes_hpp += """
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
  void initialize(intLocation location,
    Biotope* biot_ptr, Ecosystem* ecos_ptr);
  virtual void act();
  void set_location(intLocation new_location);
  void do_procreate();
  virtual void copy(Organism* parent);
  void mutate();
  void do_die();
  void unlink();
  // virtual bool decide_procreate();
};

"""


classes_hpp += repeat_with("""
class #1 : public Organism { // AUTOMATIC
public:
  // attributes:
#2
  // methods:
  #3();
  void initialize(intLocation location,
    Biotope* biot_ptr, Ecosystem* ecos_ptr);
  void act();
#4
  // decisions:
#5
  // constraints:
#6
  // costs:
#7};
""", {
    '#1': organisms_types_class_names,
    '#2': organism_types_attributes_declaration,
    '#3': organisms_types_class_names,
    '#4': organisms_types_actions_declaration,
    '#5': organisms_types_decisions_declaration,
    '#6': organisms_types_constraints_declaration,
    '#7': organisms_types_costs_declaration
})


classes_hpp += """

// --------------------------------------------------------------------
//                           P A T H O G E N
// --------------------------------------------------------------------

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

// --------------------------------------------------------------------
//                          S T A T I S T I C S
// --------------------------------------------------------------------

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

// --------------------------------------------------------------------
//                           E C O S Y S T E M
// --------------------------------------------------------------------


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
"""


# *********************************************************************

# *********************************************************************

# *********************************************************************

classes_hpp = classes_hpp.replace(' // AUTOMATIC', '')


# print classes_hpp


classes_cpp = """

// // // // // // // // // // // // // // // // // // // // //
//                                                          //
//    classes.cpp                                           //
//    Ecosystems                                            //
//                                                          //
//    Created on 28/05/2020 by:                             //
//                                                          //
//      Emilio Molina Martinez                              //
//      Juan Luis Salas Garcia                              //
//                                                          //
//    Copyright @ 2020 EMM & JLSG. All rights reserved.     //
//                                                          //
// // // // // // // // // // // // // // // // // // // // //


#ifndef classes_cpp
#define classes_cpp

#include "basic_tools.hpp"
#include "classes.hpp"

// ******************************************************************
//                        N O D E   M A K E R
// ******************************************************************

OrganismNode::OrganismNode() {};

void OrganismNode::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  switch (this->org_type) { // AUTOMATIC """


classes_cpp += repeat_with("""
    case #1:
      this->#2_ptr->initialize(location, biot_ptr, ecos_ptr);
      break;""", {'#1': organisms_type_names, '#2': organisms_types_variable_names})


classes_cpp += """
    default:
      error("Unknown organism type");
      break;
  };
};
"""


classes_cpp += """
float OrganismNode::get_float_attribute(OrganismAttribute org_attr) {

  switch (org_attr) { // AUTOMATIC """

"""

for float_attribute in float_attributes:
    classes_cpp += """

"""
    case """ 

"""
    + float_attribute + """

"""
    :
      switch (this->org_type) {"""

"""
    classes_cpp += repeat_with("""

"""
        case #1:
          return this->#2_ptr->"""

"""
        + float_attribute_variable_names[float_attribute] + """
"""
        ;
          break;"""

"""
          , {

          }
        case PLANT_B:
          return this->plant_B_ptr->energy_reserve;
          break;
        case HERBIVORE:
          return this->herbivore_ptr->energy_reserve;
          break;
        case CARNIVORE:
          return this->carnivore_ptr->energy_reserve;
          break;
        default:
          return 0;
          break;
      };
    break;
      
    case AGE:
      switch (this->org_type) {
        case PLANT_B:
          return this->plant_B_ptr->age;
          break;
        default:
          return 0;
          break;
      };
    break;
      
    case PHOTOSYNTHESIS_CAPACITY:
      switch (this->org_type) {
        case PLANT_A:
          return this->plant_A_ptr->photosynthesis_capacity;
          break;
        case PLANT_B:
          return this->plant_B_ptr->photosynthesis_capacity();
          break;
        default:
          return 0;
          break;
      };
    break;

    case STRENGTH:
      switch (this->org_type) {
        case HERBIVORE:
          return this->herbivore_ptr->strength;
          break;
        case CARNIVORE:
          return this->carnivore_ptr->strength;
          break;
        default:
          return 0;
          break;
       };

    break;
      
    case MINIMUM_ENERGY_RESERVE_FOR_PROCREATING:
      switch (this->org_type) {
        case PLANT_A:
          return this->plant_A_ptr->minimum_energy_reserve_for_procreating;
          break;
        case PLANT_B:
          return this->plant_B_ptr->minimum_energy_reserve_for_procreating;
          break;
        default:
          return 0;
          break;
      };
    break;

    case ENERGY_RESERVE_AT_BIRTH:
      switch (this->org_type) {
        case PLANT_A:
          return this->plant_A_ptr->energy_reserve_at_birth;
          break;
        default:
          return 0;
          break;
      };
    break;
      
    case IDEAL_TEMPERATURE:
      switch (this->org_type) {
        case CARNIVORE:
          return this->carnivore_ptr->ideal_temperature;
          break;
        default:
          return 0;
          break;
      };
    break;
      
    case MAX_TEMPERATURE_DEVIATION:
      switch (this->org_type) {
        case CARNIVORE:
          return this->carnivore_ptr->max_temperature_deviation;
          break;
        default:
          return 0;
          break;
      };
    break;

    default:
      return 0;
      break;
  };
};

void OrganismNode::set_location(intLocation new_location) {
  switch (this->org_type) { // AUTOMATIC
    case PLANT_A:
      this->plant_A_ptr->location = new_location;
      break;
    case PLANT_B:
      this->plant_B_ptr->location = new_location;
      break;
    case HERBIVORE:
      this->herbivore_ptr->location = new_location;
      break;
    case CARNIVORE:
      this->carnivore_ptr->location = new_location;
      break;
    default:
      error("Unknown organism type");
      break;
  };
};

intLocation OrganismNode::get_location() {
  switch (this->org_type) { // AUTOMATIC
    case PLANT_A:
      return this->plant_A_ptr->location;
      break;
    case PLANT_B:
      return this->plant_B_ptr->location;
      break;
    case HERBIVORE:
      return this->herbivore_ptr->location;
      break;
    case CARNIVORE:
      return this->carnivore_ptr->location;
      break;
    default:
      error("Unknown organism type");
      return NULL_LOCATION;
      break;
  };
};

bool OrganismNode::is_alive() {
  switch (this->org_type) { // AUTOMATIC
    case PLANT_A:
      return this->plant_A_ptr->is_alive;
      break;
    case PLANT_B:
      return this->plant_B_ptr->is_alive;
      break;
    case HERBIVORE:
      return this->herbivore_ptr->is_alive;
      break;
    case CARNIVORE:
      return this->carnivore_ptr->is_alive;
      break;
    default:
      error("Unknown organism type");
      return false;
      break;
  };
};

void OrganismNode::act() {
  switch (this->org_type) { // AUTOMATIC
    case PLANT_A:
      this->plant_A_ptr->act();
      break;
    case PLANT_B:
      this->plant_B_ptr->act();
      break;
    case HERBIVORE:
      this->herbivore_ptr->act();
      break;
    case CARNIVORE:
      this->carnivore_ptr->act();
      break;
    default:
      error("Unknown organism type");
      break;
  };
};

void OrganismNode::unlink() {
  if (this->next != nullptr)
    this->next->prev = this->prev;
  if (this->prev != nullptr)
    this->prev->next = this->next;
  // Do NOT do this->next = nullptr;
  // because Ecosystem::evolve() needs that pointer
};

void OrganismNode::insert_before(OrganismNode* reference_organism) {
  this->prev = reference_organism->prev;
  this->next = reference_organism;
  reference_organism->prev = this;
  if(this->prev != nullptr) this->prev->next = this;
};

Ecosystem* OrganismNode::get_parent_ecosystem_ptr() {
  switch (this->org_type) { // AUTOMATIC
    case PLANT_A:
      return this->plant_A_ptr->parent_ecosystem_ptr;
      break;
    case PLANT_B:
      return this->plant_B_ptr->parent_ecosystem_ptr;
      break;
    case HERBIVORE:
      return this->herbivore_ptr->parent_ecosystem_ptr;
      break;
    case CARNIVORE:
      return this->carnivore_ptr->parent_ecosystem_ptr;
      break;
    default:
      error("Unknown organism type");
      return nullptr;
      break;
  };
};


// class ObjectsPool:

template <class T>
void ObjectsPool<T>::create_more_objects() {
  this->objects_pool.push_back(std::vector<T>(this->buffer_size));
  for (auto &o : this->objects_pool.back()) {
    this->available_objects.push(&o);
  };
};

template <class T>
ObjectsPool<T>::ObjectsPool() {
  this->buffer_size = 100000;
  this->create_more_objects();
};

template <class T>
T* ObjectsPool<T>::get_new() {
  if (this->available_objects.empty()) {
    this->create_more_objects();
  };
  T* object_ptr = this->available_objects.top();
  this->available_objects.pop();
  return object_ptr;
};

template <class T>
void ObjectsPool<T>::set_available(T *object_ptr) {
  this->available_objects.push(object_ptr);
};


// class NodeMaker:

NodeMaker::NodeMaker()
  : plants_A_pool(),
    plants_B_pool(),
    herbivores_pool(),
    carnivores_pool(),
    organism_nodes_pool() {}; // AUTOMATIC

OrganismNode* NodeMaker::get_new(OrganismType org_type_) {
  OrganismNode* new_node = organism_nodes_pool.get_new();
  new_node->org_type = org_type_;
  switch (org_type_) { // AUTOMATIC
    case PLANT_A:
      new_node->plant_A_ptr = this->plants_A_pool.get_new();
      new_node->plant_A_ptr->node = new_node;
      break;
    case PLANT_B:
       new_node->plant_B_ptr = this->plants_B_pool.get_new();
       new_node->plant_B_ptr->node = new_node;
       break;
    case HERBIVORE:
       new_node->herbivore_ptr = this->herbivores_pool.get_new();
       new_node->herbivore_ptr->node = new_node;
       break;
    case CARNIVORE:
       new_node->carnivore_ptr = this->carnivores_pool.get_new();
       new_node->carnivore_ptr->node = new_node;
       break;
    default:
       error("Unknown organism type");
       break;
  };
  return new_node;
};

void NodeMaker::set_available(OrganismNode* org_node) {
  switch (org_node->org_type) { // AUTOMATIC
    case PLANT_A:
      this->plants_A_pool.set_available(org_node->plant_A_ptr);
      break;
    case PLANT_B:
      this->plants_B_pool.set_available(org_node->plant_B_ptr);
      break;
    case HERBIVORE:
      this->herbivores_pool.set_available(org_node->herbivore_ptr);
      break;
    case CARNIVORE:
      this->carnivores_pool.set_available(org_node->carnivore_ptr);
      break;
    default:
      error("Unknown organism type");
      break;
  };
  this->organism_nodes_pool.set_available(org_node);
};



// ******************************************************************
//                           B I O T O P E
// ******************************************************************


SunLight::SunLight(Biotope* parent_biotope, Ecosystem* parent_ecosystem)
    : parent_biotope_ptr(parent_biotope), parent_ecosystem_ptr(parent_ecosystem) // AUTOMATIC
{};

float float_module_int(float f, int i) {
  float answer = f - i * (lround(f) / i);
  if(answer < 0) answer += i;
  return answer;
};

float SunLight::get_value(floatLocation location) {  // CUSTOM
  return (1 + abs(sin(2 * M_PI * parent_ecosystem_ptr->cycle / 365.0))) * (1 + abs(sin(M_PI * float_module_int(location.second, this->parent_biotope_ptr->size_y)  / float(parent_biotope_ptr->size_y))));
};

Temperature::Temperature(Biotope* parent_biotope, Ecosystem* parent_ecosystem)
    : parent_biotope_ptr(parent_biotope), parent_ecosystem_ptr(parent_ecosystem),
      data({})  // AUTOMATIC
{};

void Temperature::initialize() {  // CUSTOM
  this->data = {-10, 10, 30, 30, 10, -10};
};

float Temperature::get_value(intLocation location) {  // CUSTOM
  int loc_y = location.second % this->parent_biotope_ptr->size_y;
  if (loc_y < 0) loc_y += this->parent_biotope_ptr->size_y;
  float y_float = float((data.size() - 1) * loc_y)/this->parent_biotope_ptr->size_y;
  int y_int = int(std::trunc(y_float));
  y_float -= y_int;
  return data[y_int]*(1-y_float) + data[y_int + 1] * y_float;
};

void Temperature::update() { // CUSTOM
  for(int y=0; y<data.size(); y++) {
    data[y] *= 0.95; // cada ciclo se pierde un 5% de la temperatura
    floatLocation loc(
                      0.0,
                      float(y * parent_biotope_ptr->size_y) / (data.size()-1)
                      );
    data[y] += parent_biotope_ptr->sun_light->get_value(loc);
  }
};

Biotope::Biotope(Ecosystem* parent_ecosystem) {
  this->parent_ecosystem_ptr = parent_ecosystem;
};

void Biotope::initialize(RandomNumbersGenerator* random_nums_gen_ptr_) {
  // This function has to be called AFTER parent_ecosystem_ptr->random_nums_gen has been initialized
  this->random_nums_gen_ptr = random_nums_gen_ptr_;
  this->size_x = 500;   // AUTOMATIC
  this->size_y = 500;   // AUTOMATIC
  this->area = this->size_x * this->size_y;
  organisms_vector.resize(this->area);
  this->free_locs = std::vector<int> (this->size_x * this->size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          this->random_nums_gen_ptr->eng);
  this->free_locs_counter = 0;
  this->adjacent_locations_pool.initialize(&(this->random_nums_gen_ptr->eng));
  this->temperature = new Temperature(this, this->parent_ecosystem_ptr); // AUTOMATIC
  this->temperature->initialize(); // AUTOMATIC
  this->sun_light = new SunLight(this, this->parent_ecosystem_ptr); // AUTOMATIC
};

ErrorType Biotope::evolve() {
  // Update those biotope features that need to be updated:
  this->temperature->update();  // AUTOMATIC
  return No_error;
};

OrganismNode* Biotope::get_organism(intLocation location) {
  return this->organisms_vector[location.x() * this->size_y +
    location.y()];
};

void Biotope::set_organism(intLocation location, OrganismNode* new_organism_ptr) {
  this->organisms_vector[location.x() * this->size_y +
                      location.y()] = new_organism_ptr;
};

void Biotope::set_organism(OrganismNode* new_organism_ptr) {
  this->set_organism(new_organism_ptr->get_location(),
                     new_organism_ptr);
};

void Biotope::remove_organism(OrganismNode *organism_node) {

  this->set_organism(organism_node->get_location(), nullptr);
};

void Biotope::move_organism(intLocation old_location, intLocation new_location) {
  intLocation old_loc = this->normalize(old_location);
  intLocation new_loc = this->normalize(new_location);
  OrganismNode* org_node = this->get_organism(old_loc);
  this->set_organism(new_loc, org_node);
  this->set_organism(old_loc,  nullptr);
  org_node->set_location(new_loc);
};

int Biotope::get_num_organisms() {
  return this->parent_ecosystem_ptr->get_num_organisms();
};

// get random location in the biotope, NOT NECESSRAY AN EMPTY LOCATION:
intLocation Biotope::get_random_location() {
  this->free_locs_counter++;
  this->free_locs_counter %= this->area;
  if(this->free_locs_counter == 0)
    shuffle(this->free_locs.begin(), this->free_locs.end(),
            this->random_nums_gen_ptr->eng);
  int packed_location = this->free_locs[this->free_locs_counter];
  return intLocation(
                           packed_location / this->size_y,
                           packed_location % this->size_y
                           );
};

intLocation Biotope::get_one_free_location() {
  if(this->get_num_organisms() < this->area) {
    intLocation loc = this->get_random_location();
    while(this->get_organism(loc) != nullptr)
      loc = this->get_random_location();
    return loc;
  }
  else {
    error("No free locations found"); // return Error;
    return NULL_LOCATION;
  };
};

OrganismNode* Biotope::get_random_organism() {
  OrganismNode* node = nullptr;
  while(node == nullptr) node = this->get_organism(get_random_location());
  return node;
};

intLocation Biotope::get_free_location_close_to(intLocation center, int radius) {
  // Use this method only with small radiuses. Otherwise, it's very time-consuming.
  std::vector<intLocation> free_locations_found = {};
  for(int x = center.x() - radius;
      x <= center.x() + radius;
      x++) {
    for(int y = center.y() - radius;
        y <= center.y() + radius;
        y++) {
      intLocation new_loc = this->normalize(intLocation(x, y));
      if(this->get_organism(new_loc) == nullptr)
        free_locations_found.push_back(new_loc);
    };
  };
  if(free_locations_found.size() == 0) {
    return NULL_LOCATION;
  } else {
    return this->normalize(free_locations_found[
      this->random_nums_gen_ptr->get_uniform_rand_int(0, (int) free_locations_found.size())
    ]);
  };
};

intLocation Biotope::get_free_location_close_to(intLocation center, int radius, int number_of_attempts) {
  // This method is assumed to be used by some organisms in order to move themselves to another location. For organisms that jump very far away each time, it's very time-consuming to collect every single empty location within such a large radius, just to randomly chose one of them. That's why they should try a number of times and resign from moving if they don't find a place to do it in those attempts:
  for(int i=0; i<number_of_attempts; i++) {
    intLocation new_location = this->normalize(center + this->random_nums_gen_ptr->get_rand_intLocation(radius));
    if(this->get_organism(new_location) == nullptr) {
      return new_location;
    };
  };
  return NULL_LOCATION;
};

intLocation Biotope::get_free_adjacent_location(intLocation center) {
  std::vector<intLocation> adjacent_locations = this->adjacent_locations_pool.get_next();
  for(intLocation location : adjacent_locations) {
    intLocation new_loc = this->normalize(center + location);
    if(this->get_organism(new_loc) == nullptr) {
      return new_loc;
    };
  };
  return NULL_LOCATION;
};

OrganismNode* Biotope::get_adjacent_organism_of_type(intLocation center, OrganismType org_type) {
  std::vector<intLocation> adjacent_locations = this->adjacent_locations_pool.get_next();
  for(intLocation location : adjacent_locations) {
    intLocation new_loc = this->normalize(center + location);
    OrganismNode* org_node = this->get_organism(new_loc);
    if(org_node != nullptr) {
      if(org_node->org_type == org_type) {
        return org_node;
      };
    };
  };
  return nullptr;
};

intLocation Biotope::normalize(intLocation location) {
  return intLocation(
    (location.x() % this->size_x + this->size_x) % this->size_x,
    (location.y() % this->size_y + this->size_y) % this->size_y);
};


// ******************************************************************
//                           O R G A N I S M
// ******************************************************************

Organism::Organism() {};

void Organism::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  
  // This function is called when an organism is created from scratch,
  // not by procreation of another organism.
  
  this->location = location;
  this->parent_ecosystem_ptr = ecos_ptr;
  this->parent_biotope_ptr = biot_ptr;
  this->is_alive = true;
};

void Organism::act() {};

void Organism::set_location(intLocation new_location) {
  this->location = new_location;
};

void Organism::do_procreate() {};

void Organism::copy(Organism* parent) {
  this->parent_ecosystem_ptr = parent->parent_ecosystem_ptr;
  this->parent_biotope_ptr = parent->parent_biotope_ptr;
};

void Organism::mutate() {
  this->is_alive = true;
  // nothing to do here yet
};

void Organism::do_die() {
  this->is_alive = false;
  this->parent_ecosystem_ptr->move_dead_organism_to_ghost_list(this);
};

void Organism::unlink() {
  if(this->node != nullptr) this->node->unlink();
};



// ******************************************************************
//                         P L A N T   A
// ******************************************************************
// plant_A: plants that can live with little sunlight

Plant_A::Plant_A() {};

void Plant_A::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) { // CUSTOM
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->minimum_energy_reserve_for_procreating = 300;
  this->energy_reserve_at_birth = 100;
  this->energy_reserve = 100;
};

void Plant_A::act() {  // CUSTOM
  // do photosynthesis:
  this->energy_reserve += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(floatLocation(this->location)));
  // procreate:
  if(this->decide_procreate()) this->do_procreate();
  // constraint:
  if(this->energy_reserve < 100) do_die();
};

void Plant_A::do_procreate() {  // AUTOMATIC
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    OrganismNode* offspring = this->parent_ecosystem_ptr->node_maker.get_new(PLANT_A);
    offspring->plant_A_ptr->copy(this);
    offspring->plant_A_ptr->set_location(free_location);
    offspring->plant_A_ptr->mutate();
    offspring->plant_A_ptr->is_alive = true;
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->plant_A_ptr);
  };
};

void Plant_A::copy(Plant_A *parent) {  // AUTOMATIC
  Organism::copy(parent);
  this->minimum_energy_reserve_for_procreating = parent->minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = parent->energy_reserve_at_birth;
};

void Plant_A::mutate() {  // CUSTOM
  this->energy_reserve = this->energy_reserve_at_birth;
  this->energy_reserve_at_birth = this->parent_ecosystem_ptr->random_nums_gen.proportional_mutation_float(this->energy_reserve_at_birth, 0.015);
  this->minimum_energy_reserve_for_procreating = this->parent_ecosystem_ptr->random_nums_gen.uniform_mutation_float_min(this->minimum_energy_reserve_for_procreating, 7.5, this->energy_reserve_at_birth);
};

bool Plant_A::decide_procreate() {  // CUSTOM
  return this->energy_reserve > this->minimum_energy_reserve_for_procreating;
};

void Plant_A::subtract_costs_of_procreating(Plant_A *offspring) { // CUSTOM
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
  // fixed cost:
  this->energy_reserve -= 50;
};


// ******************************************************************
//                         P L A N T   B
// ******************************************************************
// plant_B: plants that need much sunlight

float Plant_B::photosynthesis_capacity() {  // CUSTOM
  return 2 * sqrt(this->age + this->energy_reserve);
};

Plant_B::Plant_B() {};

void Plant_B::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {   // CUSTOM
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = ecos_ptr->random_nums_gen.get_uniform_rand_float(100, 1000);
};

void Plant_B::act() {  // CUSTOM
  // do photosynthesis:
  this->energy_reserve += -25 + 34 * (this->parent_biotope_ptr->sun_light->get_value(floatLocation(this->location)));
  // procreate:
  if(this->decide_procreate()) this->do_procreate();
  // constraint:
  if(this->energy_reserve < 100) do_die();
  // age:
  if(this->is_alive) this->do_age();
};

void Plant_B::do_procreate() {  // AUTOMATIC
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    OrganismNode* offspring = this->parent_ecosystem_ptr->node_maker.get_new(PLANT_B);
    offspring->plant_B_ptr->copy(this);
    offspring->plant_B_ptr->set_location(free_location);
    offspring->plant_B_ptr->age = 0;
    offspring->plant_B_ptr->is_alive = true;
    // offspring->plant_B_ptr->mutate();    // this isn't necessary
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->plant_B_ptr);
  };
};

void Plant_B::do_age() {  // CUSTOM
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  };
};

bool Plant_B::decide_procreate() {  // CUSTOM
  return (this->energy_reserve > this->minimum_energy_reserve_for_procreating);
};

void Plant_B::subtract_costs_of_procreating(Plant_B *offspring) {  // CUSTOM
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
};


// ******************************************************************
//                       H E R B I V O R E
// ******************************************************************

Herbivore::Herbivore() {};

void Herbivore::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) { // CUSTOM
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(5000, 15000);
  this->max_energy_reserve_capacity = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(10000, 60000);;
  this->strength = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 20);
  this->eatable_plant_type = this->parent_ecosystem_ptr->random_nums_gen.true_with_probability(0.5) ? PLANT_A : PLANT_B;
};

void Herbivore::act() { // CUSTOM
  this->do_hunt();
  this->do_move();
  this->do_hunt();
  this->do_internal_changes();
  if(this->can_procreate()) {
    this->do_procreate();
  };
  this->subtract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Herbivore::do_internal_changes() { // CUSTOM
  if(this->energy_reserve > this->max_energy_reserve_capacity) {
    this->energy_reserve = this->max_energy_reserve_capacity;
  };
};

void Herbivore::do_move() { // CUSTOM
  intLocation new_location = this->parent_biotope_ptr
    ->get_free_location_close_to(this->location, 4.5, 2);
  if(new_location != NULL_LOCATION) {
    this->parent_biotope_ptr->move_organism(this->location, new_location);
  };
};

void Herbivore::do_hunt() { // CUSTOM or AUTOMATIC ?
  OrganismNode* food = this->parent_biotope_ptr
  ->get_adjacent_organism_of_type(this->location, this->eatable_plant_type);
  if(food != nullptr) {
    this->do_eat(food);
  };
};

void Herbivore::do_eat(OrganismNode* food) { // AUTOMATIC
  switch (food->org_type) {
    case PLANT_A:
      this->energy_reserve += food->plant_A_ptr->energy_reserve;
      food->plant_A_ptr->do_die();
      break;
    case PLANT_B:
      this->energy_reserve += food->plant_B_ptr->energy_reserve;
      food->plant_B_ptr->do_die();
      break;
    default:
      error("Incorrect organism type");
      break;
  };
};

void Herbivore::do_procreate() {  // AUTOMATIC
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    OrganismNode* offspring = this->parent_ecosystem_ptr->node_maker.get_new(HERBIVORE);
    offspring->herbivore_ptr->copy(this);
    offspring->herbivore_ptr->set_location(free_location);
    offspring->herbivore_ptr->mutate();
    offspring->herbivore_ptr->is_alive = true;
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->herbivore_ptr);
  };
};

void Herbivore::copy(Herbivore* parent) { // AUTOMATIC
  Organism::copy(parent);
  this->strength = parent->strength;
  this->eatable_plant_type = parent->eatable_plant_type;
  this->max_energy_reserve_capacity = parent->max_energy_reserve_capacity;
};

void Herbivore::mutate() { // CUSTOM
  this->energy_reserve = 500;
  
  this->strength =
  parent_ecosystem_ptr->random_nums_gen
  .proportional_mutation_float_min(this->strength, 0.05, 0.01);
  
  if(this->eatable_plant_type == PLANT_A) {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.1)) {
      this->eatable_plant_type = PLANT_B;
    }
  }
  else {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.25))
    {
      this->eatable_plant_type = PLANT_A;
    };
  };
  
  this->max_energy_reserve_capacity =
  parent_ecosystem_ptr->random_nums_gen
  .proportional_mutation_float(this->max_energy_reserve_capacity, 0.05);
};

bool Herbivore::can_procreate() { // CUSTOM
  return (this->energy_reserve > 5000);
};

void Herbivore::subtract_costs_of_being_alive() { // CUSTOM
  this->energy_reserve -= 2 * this->strength;
  this->energy_reserve -= 100;
  this->energy_reserve -= 0.001 * this->max_energy_reserve_capacity;
}

void Herbivore::subtract_costs_of_procreating(Herbivore *offspring) {
  // CUSTOM
  // fixed cost:
  this->energy_reserve -= 3000;
};


// ******************************************************************
//                       C A R N I V O R E
// ******************************************************************

Carnivore::Carnivore() {};

void Carnivore::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) { // CUSTOM
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(1500, 15000);
  this->max_energy_reserve_capacity = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(10000, 50000);;
  this->strength = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 20);
  this->ideal_temperature = biot_ptr->temperature->get_value(location);
  this->max_temperature_deviation = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 40);
  this->moving_frequency = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.2, 1);
  this->moving_time = 0.0;
};


void Carnivore::act() { // CUSTOM
  this->do_hunt();
  if(this->decide_move()) {
    this->do_move();
  };
  this->do_hunt(); // yes, again
  this->do_internal_changes();
  if(this->decide_procreate() and this->can_procreate()) {
    this->do_procreate();
  };
  this->subtract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Carnivore::do_internal_changes() { // CUSTOM
  if(this->energy_reserve > this->max_energy_reserve_capacity) {
    this->energy_reserve = this->max_energy_reserve_capacity;
  };
};

void Carnivore::do_move() { // CUSTOM
  intLocation new_location = this->parent_biotope_ptr
  ->get_free_location_close_to(this->location, 6.5, 4);
  if(new_location != NULL_LOCATION) {
    this->subtract_costs_of_moving(new_location);
    this->parent_biotope_ptr->move_organism(this->location, new_location);
  };
};

void Carnivore::do_hunt() {  // CUSTOM or AUTOMATIC ?
  OrganismNode* food = this->parent_biotope_ptr
  ->get_adjacent_organism_of_type(this->location, HERBIVORE);
  if(food != nullptr) {
    this->do_try_to_eat(food->herbivore_ptr);
  };
};

void Carnivore::do_try_to_eat(Herbivore *herbivore) { // CUSTOM
  if(this->parent_ecosystem_ptr->random_nums_gen
     .true_with_probability(this->strength / (this->strength + herbivore->strength))) {
    this->do_eat(herbivore);
  };
};

void Carnivore::do_eat(Herbivore *herbivore) { // AUTOMATIC
  this->energy_reserve += herbivore->energy_reserve;
  herbivore->do_die();
};

void Carnivore::do_procreate() { // AUTOMATIC
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    OrganismNode* offspring = this->parent_ecosystem_ptr->node_maker.get_new(CARNIVORE);
    offspring->carnivore_ptr->copy(this);
    offspring->carnivore_ptr->set_location(free_location);
    offspring->carnivore_ptr->mutate();
    offspring->carnivore_ptr->is_alive = true;
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->carnivore_ptr);
  };
};

void Carnivore::copy(Carnivore* parent) { // AUTOMATIC
  Organism::copy(parent);
  this->strength = parent->strength;
  this->ideal_temperature = parent->ideal_temperature;
  this->max_temperature_deviation = parent->max_temperature_deviation;
  this->moving_frequency = parent->moving_frequency;
  this->moving_time = 0.0;
  this->max_energy_reserve_capacity = parent->max_energy_reserve_capacity;
};

void Carnivore::mutate() { // CUSTOM
  this->energy_reserve *= 0.25;
  
  this->strength =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation_float_min(this->strength, 0.05, 0.01);
    
  this->ideal_temperature = parent_ecosystem_ptr->random_nums_gen
  .uniform_mutation_float(this->ideal_temperature, 3.5);
  
  this->max_temperature_deviation =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation_float(this->max_temperature_deviation, 0.25);
  
  this->moving_frequency = parent_ecosystem_ptr->random_nums_gen.proportional_mutation_float_min_max(this->moving_frequency, 0.1, 0.0, 1.0);
  
  this->moving_time = 0.0;
  
  this->max_energy_reserve_capacity =
  parent_ecosystem_ptr->random_nums_gen
  .proportional_mutation_float(this->max_energy_reserve_capacity, 0.05);
};

bool Carnivore::decide_move() {  // CUSTOM
  this->moving_time += this->moving_frequency;
  if(this->moving_time > 1)
  {
    this->moving_time -= 1;
    if(this->energy_reserve > 1000)
    {
      return true;
    }
    else {
      return false;
    }
  }
  else {
    return false;
  };
};

bool Carnivore::decide_procreate() {  // CUSTOM
  return (this->energy_reserve > 5000);
};

bool Carnivore::can_procreate() {  // CUSTOM
  return (
    std::abs(
      this->parent_biotope_ptr->temperature->get_value(this->location)
      - this->ideal_temperature
    ) <= this->max_temperature_deviation
  );
};

void Carnivore::subtract_costs_of_moving(intLocation new_location) { // CUSTOM
  this->energy_reserve -= 2.5 * taxi_distance(this->location, new_location);
  this->energy_reserve -= 0.3 * this->max_temperature_deviation;
};

void Carnivore::subtract_costs_of_procreating(Carnivore *offspring) { // CUSTOM
  // proportional cost:
  this->energy_reserve -= 1.5 * offspring->energy_reserve;
  this->energy_reserve -= this->max_temperature_deviation;
  // fixed cost:
  this->energy_reserve -= 100;
  this->energy_reserve -= 0.001 * this->max_energy_reserve_capacity;
};

void Carnivore::subtract_costs_of_being_alive() { // CUSTOM
  this->energy_reserve -= 2 * this->strength;
  this->energy_reserve -= 20;
  this->energy_reserve -= 0.8 * this->max_temperature_deviation;
  this->energy_reserve -= 0.0005 * this->max_energy_reserve_capacity;
};


// ******************************************************************
//                           P A T H O G E N
// ******************************************************************

Pathogen::Pathogen() {};
void Pathogen::initialize(RandomNumbersGenerator* random_nums_gen_ptr) {
  this->antigen = random_nums_gen_ptr->get_uniform_rand_int(100, 200);
  switch (random_nums_gen_ptr->get_uniform_rand_int(0, 3)) {
    case 0:
      this->target = PLANT_A;
      break;
    case 1:
      this->target = PLANT_B;
      break;
    case 2:
      this->target = HERBIVORE;
      break;
    case 3:
      this->target = CARNIVORE;
      break;
  };
  this->probability_of_contagion_each_cycle = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
  this->probability_of_killing_host_each_cycle = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
  this->probability_of_host_recovery_each_cycle = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
  this->probability_of_host_obtaining_immunity_after_infection = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
  this->probability_of_mutation_before_new_infection = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
  this->percentage_of_energy_reserve_destroyed_by_desease_each_cycle = random_nums_gen_ptr->get_uniform_rand_float(0, 1);
};

void Pathogen::set_host(OrganismNode* new_host) {};
// actions:
void Pathogen::act() {};
void Pathogen::kill_host() {};
void Pathogen::infect_new_host(OrganismNode* new_host) {};
void Pathogen::spread() {}; // Look for new host closer than radius_of_contagion_possibility
void Pathogen::steal_energy_reserve() {};
void Pathogen::mutate() {};


// ******************************************************************
//                          S T A T I S T I C S
// ******************************************************************

Statistics::Statistics() {};

void Statistics::initialize(Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  this->parent_biotope_ptr = biot_ptr;
  this->parent_ecosystem_ptr = ecos_ptr;
  this->last_cycle_when_calculated_the_number_of_organisms_by_type = -1;
  this->number_of_organisms_by_type[PLANT_A] = 0; // AUTOMATIC
  this->number_of_organisms_by_type[PLANT_B] = 0;
  this->number_of_organisms_by_type[HERBIVORE] = 0;
  this->number_of_organisms_by_type[CARNIVORE] = 0;

  this->attributes_of_each_type[PLANT_A] = { // AUTOMATIC
    PHOTOSYNTHESIS_CAPACITY,
    ENERGY_RESERVE,
    MINIMUM_ENERGY_RESERVE_FOR_PROCREATING,
    ENERGY_RESERVE_AT_BIRTH
  };
  
  this->attributes_of_each_type[PLANT_B] = {
    PHOTOSYNTHESIS_CAPACITY,
    AGE,
    DEATH_AGE,
    ENERGY_RESERVE,
    MINIMUM_ENERGY_RESERVE_FOR_PROCREATING
  };
  
  this->attributes_of_each_type[HERBIVORE] = {
    ENERGY_RESERVE,
    STRENGTH,
    EATABLE_PLANT_TYPE
  };
  
  this->attributes_of_each_type[CARNIVORE] = {
    ENERGY_RESERVE,
    STRENGTH,
    IDEAL_TEMPERATURE,
    MAX_TEMPERATURE_DEVIATION,
    MOVING_FREQUENCY
  };
  
  this->types_that_have_each_attribute[PHOTOSYNTHESIS_CAPACITY] = {
    PLANT_A,
    PLANT_B
  };

  this->types_that_have_each_attribute[MINIMUM_ENERGY_RESERVE_FOR_PROCREATING] = {
    PLANT_A,
    PLANT_B
  };

  this->types_that_have_each_attribute[ENERGY_RESERVE] = {
    PLANT_A,
    PLANT_B,
    HERBIVORE,
    CARNIVORE
  };
  
  this->types_that_have_each_attribute[STRENGTH] = {
    HERBIVORE,
    CARNIVORE
  };
};

unsigned int Statistics::get_number_of_organisms(OrganismType org_type) {
  this->calculate_number_of_organisms_by_type();
  return this->number_of_organisms_by_type[org_type];
};

void Statistics::calculate_number_of_organisms_by_type() {
  if(this->last_cycle_when_calculated_the_number_of_organisms_by_type < this->parent_ecosystem_ptr->cycle) {
    // setting all the counts to zero:
    for(auto const& item : this->number_of_organisms_by_type) {
      this->number_of_organisms_by_type[item.first] = 0;
    };
    // counting:
    OrganismNode* org_node = this->parent_ecosystem_ptr->first_organism_node;
    while(org_node != nullptr) {
      this->number_of_organisms_by_type[org_node->org_type]++;
      org_node = org_node->next;
    };
    this->last_cycle_when_calculated_the_number_of_organisms_by_type = this->parent_ecosystem_ptr->cycle;
  };
};

float Statistics::mean_of_attribute(OrganismAttribute org_attr, OrganismType org_type) { return 0; };


// ******************************************************************
//                           E C O S Y S T E M
// ******************************************************************


Ecosystem::Ecosystem() : random_nums_gen(), biotope(this) {
  this->statistics.initialize(&(this->biotope), this);
  this->random_nums_gen.set_seed(0);
  this->cycle = 0;
  this->first_organism_node = nullptr;
  this->ghost_organisms_ptrs = {};
  this->number_of_organisms = 0;
  this->biotope.initialize(&(this->random_nums_gen));
};

void Ecosystem::initialize() {
  this->random_nums_gen.set_seed(0);
  this->cycle = 0;
  this->first_organism_node = nullptr;
  this->ghost_organisms_ptrs = {};
  this->biotope.initialize(&(this->random_nums_gen));
};

void Ecosystem::create_new_organisms(OrganismType organism_type, int number_of_new_organisms) {
  for(int i = 0; i < number_of_new_organisms; i++) {
    this->create_one_new_organism(organism_type);
  };
};

void Ecosystem::create_one_new_organism(OrganismType organism_type) {
  OrganismNode* new_organism = this->node_maker.get_new(organism_type);
  intLocation location = this->biotope.get_one_free_location();
  new_organism->initialize(location, &(this->biotope), this);
  this->biotope.set_organism(location, new_organism);
  this->append_organism(new_organism);
};

void Ecosystem::append_first_organism(OrganismNode *first_organism) {
  this->first_organism_node = first_organism;
  first_organism->prev = nullptr;
  first_organism->next = nullptr;
  this->biotope.set_organism(first_organism);
  this->number_of_organisms++;
};

void Ecosystem::append_organism(OrganismNode* new_organism) {
  if(this->first_organism_node == nullptr) {
    this->append_first_organism(new_organism);
  }
  else {
    this->insert_new_organism_before(new_organism, this->first_organism_node);
    this->first_organism_node = new_organism;
  };
};

void Ecosystem::insert_new_organism_before(OrganismNode* new_organism, OrganismNode* reference_organism) {
  // We assume that:
  //    this->first_organism_node != nullptr
  //    reference_organism != nullptr
  this->number_of_organisms++;
  this->biotope.set_organism(new_organism);
  if(reference_organism == this->first_organism_node) {
    this->first_organism_node = new_organism;
  };
  new_organism->insert_before(reference_organism);
};

int Ecosystem::get_num_organisms() {
  return this->number_of_organisms;
};

void Ecosystem::evolve() {
  this->clear_ghost_organisms();
  OrganismNode* organism_node = this->first_organism_node;
  while (organism_node != nullptr) {
    
    assert(organism_node->is_alive());
    
    organism_node->act();
    organism_node = organism_node->next;
  };
  this->biotope.evolve();
  this->cycle += 1;
};

void Ecosystem::move_dead_organism_to_ghost_list(Organism* org) {
  this->biotope.remove_organism(org->node);
  this->number_of_organisms--;
  if(org->node == this->first_organism_node) this->first_organism_node = org->node->next;
  org->node->unlink();
  this->ghost_organisms_ptrs.push_back(org->node);
};

void Ecosystem::clear_ghost_organisms() {
  for (auto &ghost_organism_ptr : this->ghost_organisms_ptrs) {
    this->node_maker.set_available(ghost_organism_ptr);
  };
  this->ghost_organisms_ptrs.clear();
};

std::vector<float> Ecosystem::get_attribute_matrix(OrganismAttribute org_attr, OrganismType org_type) {
  std::vector<float> matrix;
  matrix.resize(this->biotope.area);
  for(int x = 0; x<this->biotope.size_x; x++)
    for(int y = 0; y<this->biotope.size_y; y++) {
      OrganismNode* org_node = this->biotope.get_organism(intLocation(x, y));
      if(org_node != nullptr) {
        if(org_node->org_type == org_type) { matrix.push_back(org_node->get_float_attribute(org_attr));
        } else { matrix.push_back(0); }
      } else { matrix.push_back(0); };
    };
  return matrix;
};

void Ecosystem::keep_number_of_organism_above(OrganismType org_type, int num_orgs) {
  int n = num_orgs - this->statistics.get_number_of_organisms(org_type);
  if(n>0) this->create_new_organisms(org_type, n);
};

Matrix::Matrix(Ecosystem &e, OrganismAttribute org_attr, OrganismType org_type) :
    m_rows(e.biotope.size_x),
    m_cols(e.biotope.size_y),
    m_data(m_rows * m_cols) {
  for(int x = 0; x < e.biotope.size_x; x++) {
    for(int y = 0; y < e.biotope.size_y; y++) {
      int i = x * e.biotope.size_y + y;
      OrganismNode* org_node = e.biotope.get_organism(intLocation(x, y));
      if(org_node != nullptr) {
        if(org_node->org_type == org_type) {
          m_data[i] = org_node->get_float_attribute(org_attr);
        } else {
          m_data[i] = -1.0f;
        }
      } else {
        m_data[i] = -1.0f;
      };
    };
  };
};

float* Matrix::data() {
  return &m_data[0];
};

size_t Matrix::rows() {
  return m_rows;
};

size_t Matrix::cols() {
  return m_cols;
};


#endif /* classes_cpp */


"""

print classes_hpp
print classes_cpp








