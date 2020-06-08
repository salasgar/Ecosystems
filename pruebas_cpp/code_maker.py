
# Information extracted from settings:
organisms_types = ['PLANT A', 'PLANT B', 'HERBIVORE', 'CARNIVORE']
organisms_types_class_names = ['Plant_A', 'Plant_B', 'Herbivore', 'Carnivore']
organisms_types_variable_names = [
    'plant_A', 'plant_B', 'herbivore', 'carnivore']
organisms_types_variable_plural_names = [
    'plants_A', 'plants_B', 'herbivores', 'carnivores']
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


classes_hpp += repeat_with('  #,\n', {'#': organisms_types})[:-2]


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


classes_hpp += repeat_with('  #1* #2;\n', {'#1': biotope_features_class_names, '#2': biotope_features_variable_names})


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

"""


classes_hpp += repeat_with("""
class #1 : public Organism { // AUTOMATIC
public:
  // attributes:
#2
  // methods:
  #3();
  void initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr);
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
"""


# ***********************************************************************

# ***********************************************************************

# ************************************************************************

classes_hpp = classes_hpp.replace(' // AUTOMATIC', '')


print classes_hpp









