#import string
import extract_information_from_settings.py


def make_vector_of_dictionaries(dictionary_of_vectors):
    key0 = dictionary_of_vectors.keys()[0]
    return [
        dict(
            (key, dictionary_of_vectors[key][i])
            for key in dictionary_of_vectors)
        for i in range(len(dictionary_of_vectors[key0]))
    ]


def repeat_with(text, dictionary_of_vectors):
    vector_of_dict = make_vector_of_dictionaries(dictionary_of_vectors)
    result_text = ""
    for i in range(len(vector_of_dict)):
        one_iteration = text
        for key in vector_of_dict[i]:
            one_iteration = one_iteration.replace(key, vector_of_dict[i][key])
        result_text += one_iteration
    return result_text


def repeat_with(text, dictionary_of_dictionaries, keys_list):
    result_text = ""
    for main_key in keys_list:
        one_iteration = text
        for key in dictionary_of_dictionaries[main_key]:
            one_iteration = one_iteration.replace(
                key, dictionary_of_dictionaries[main_key][key])
        result_text += one_iteration
    return result_text


class CodeMaker:
    def __init__(self, settings):
        self.settings = settings
        self.information = Information(settings)
        self.make_classes_hpp()
        self.make_classes_cpp()

    def make_classes_hpp(self):
        synonym_of = self.information.synonym_of
        settings = self.information.settings
        names_dictionary = self.information.names_dictionary
        organisms_types_list = self.information.organisms_types_list
        organisms_attributes_list = self.information.organisms_attributes_list
        biotope_attributes_list = self.information.biotope_attributes_list
        ecosystem_attributes_list = self.information.ecosystem_attributes_list

        self.classes_hpp = """

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
"""

        for org_type in organisms_types_list:
            self.classes_hpp += '  {},\n'.format(org_type)
        self.classes_hpp = self.classes_hpp[:-1]

        self.classes_hpp += """
  NULL_ORGANISM_TYPE,
  ALL_TYPES
} OrganismType;

typedef enum OrganismAttribute // AUTOMATIC
{
"""
        for org_attr in organisms_attributes_list:
            self.classes_hpp += '  {},\n'.format(org_attr)
        self.classes_hpp = self.classes_hpp[:-2]

        self.classes_hpp += """
} OrganismAttribute;

"""

        self.classes_hpp += """
typedef enum BiotopeAttribute // AUTOMATIC
{
"""

        for biot_attr in biotope_attributes_list:
            self.classes_hpp += '  {},\n'.format(biot_attr)
        self.classes_hpp = self.classes_hpp[:-2]

        self.classes_hpp += """
} BiotopeAttribute;

const std::vector<BiotopeAttribute> BIOTOPE_ATTRIBUTES = {"""

        for biot_attr in biotope_attributes_list:
            self.classes_hpp += '{}, '.format(biot_attr)
        self.classes_hpp = self.classes_hpp[:-1] + "};\n"

        for org_type in organisms_types_list:
            self.classes_hpp += 'class {};\n'.format(
                names_dictionary[org_type]['class name'])

        self.classes_hpp += """


// ----------------------  O R G A N I S M   N O D E  ----------------------


class OrganismNode {
 public:
  // Connections:
  OrganismNode* prev;
  OrganismNode* next;
  // Attributes:
  OrganismType org_type;
  union {
"""

        for org_type in organisms_types_list:
            self.classes_hpp += '    {1}* {2}_ptr;\n'.format(
                names_dictionary[org_type]['class name'],
                names_dictionary[org_type]['variable name'])

        self.classes_hpp += """  };
  // Methods:
  OrganismNode();
  void initialize(
    intLocation location,
    Biotope* biot_ptr,
    Ecosystem* ecos_ptr
  );
  float get_numeric_attribute(OrganismAttribute org_attr);
  OrganismType get_organism_type_attribute(OrganismAttribute org_attr);
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

        if len(organisms_types_list) > 1:
            self.classes_hpp += "  // {} ".format(len(organisms_types_list))
            self.classes_hpp += "different types of organisms:\n"

        for org_type in organisms_types_list:
            self.classes_hpp += '  ObjectsPool<{1}> {2}_pool;\n'.format(
                names_dictionary[org_type]['class name'],
                names_dictionary[org_type]['variable name in plural'])

        self.classes_hpp += """  // and the nodes:
          ObjectsPool<OrganismNode> organism_nodes_pool;
          // methods:
          NodeMaker();
          OrganismNode* get_new(OrganismType org_type_);
          void set_available(OrganismNode* org_node);
        };

        """

# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******




_biotope = {
    'size': (500, 500),
    'attributes': {
        'sunlight': {},
        'temperature': {}
    }
}

_organisms_types_list = ['PLANT A', 'PLANT B', 'HERBIVORE', 'CARNIVORE']


_PLANT_A = {'type': 'PLANT A'}
_PLANT_B = {'type': 'PLANT B'}
_HERBIVORE = {'type': 'HERBIVORE'}
_CARNIVORE = {'type': 'CARNIVORE'}

_PLANT_A['initial number of organisms'] = 5000
_PLANT_B['initial number of organisms'] = 5000
_HERBIVORE['initial number of organisms'] = 5000
_CARNIVORE['initial number of organisms'] = 1600


_PLANT_A['names'] = {
    'enum name': 'PLANT_A',
    'class name': 'Plant_A',
    'variable name': 'plant_A',
    'variable name in plural': 'plants_A'
}

_PLANT_B['names'] = {
    'enum name': 'PLANT_B',
    'class name': 'Plant_B',
    'variable name': 'Plant_B',
    'variable name in plural': 'plants_B'
}

_PLANT_A['inlines'] = {
    '$SUNLIGHT':
        "(this->parent_biotope_ptr->sunlight->get_value(this->location))"
}

_PLANT_A['attributes'] = {
    'energy reserve': {
        'initial value': 10000,
        'type': 'float',
        'value in next cycle': {
            'help':
            """
                The increasement of the energy reserve depends
                both on the amount of sunlight
                and the photosynthesis capacity of the organism.

                'extract feature' returns certain amount of sunlight
                and also decreased the
                available amount of sunlight for other organisms that
                act after this one.

                'normalized location' returns the location of the current
                organisms but in these terms:
                    If the location of the organism is (i, j) and the size
                    of the ecosystem is (size_x, size_y), then:
                        'normalized location x' returns  i / size_x
                        and
                        'normalized location y' returns j / size_y
            """,
            'c++ code': """
                this->energy_reserve += -10 + 20 * $SUNLIGHT;
            """},
        'value after mutation': 'energy reserve at birth',
    },
    'minimum energy reserve for procreating': {
        'initial value': 400,
        'value after mutation': {
            'uniform_mutation_float_min': (7.5, 'energy reserve at birth')
        }
    },

    'energy reserve at birth': {
       'initial value': 200,
       'value after mutation': {
            'proportional_mutation_float': 0.015
       }
    }
}

_PLANT_A['decisions'] = {
    'decide procreate': {
        'c++ code': "return this->energy_reserve > this" +
        "->minimum_energy_reserve_for_procreating;"
    },
}

_PLANT_A['constraints'] = {
    'can stay alive': {
        'c++ code': "return (this->energy_reserve >= 100);"
    }
}

_PLANT_A['costs'] = {
    'subtract costs of procreating': {
        'c++ code': """
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
  // fixed cost:
  this->energy_reserve -= 50;"""
    }
}


_PLANT_B['inlines'] = _PLANT_A['inlines']

_PLANT_B['constants'] = {
    'DEATH_AGE': 1000,
    'MINIMUM_ENERGY_RESERVE_FOR_PROCREATING': 300,
}

_PLANT_B['attributes'] = {
    'energy reserve': {
        'initial value': {
            'uniform_rand_float': (100, 10000)
        },
        'type': 'float',
        'value in next cycle': {
            'c++ code': """
                this->energy_reserve += -25 +
                    0.2 * this->photosynthesis_capacity * $SUNLIGHT
            """},
        'value after mutation': {
            'c++ code': "this->energy_reserve = parent->energy_reserve / 3;"
        },
    },
    'age': {
        'type': 'int',
        'initial value': 0,
        'value in next cycle': {
            'c++ code': "this->age += 1;"
        },
        'value after mutation': 0
    }
}

_PLANT_B['decisions'] = _PLANT_A['decisions']

_PLANT_B['constraints'] = {
    'can stay alive': {
        'c++ code':
            "return (this->age < DEATH_AGE) and (this->energy_reserve > 100);"
    }
}

_PLANT_B['costs'] = {
    'subtract costs of procreating': {
        'c++ code': "this->energy_reserve -= 1.1 * offspring->energy_reserve;"
    }
}

_HERBIVORE['attributes'] = {

    'energy reserve': {
        'initial value': {
            'uniform_rand_float': (5000, 15000)
        },
        'allowed interval': [0, 'max_energy_reserve_capacity'],
        'value after mutation': 500
    },

    'max energy reserve capacity': {
        'initial value': {
            'uniform_rand_float': (10000, 60000)
        },
        'value after mutation': {
            'proportional_mutation_float': 0.05
        }
    },

    'strength': {
        'initial value': {
            'uniform_rand_float': (0.5, 20)
        },
        'value after mutation': {
            'proportional_mutation_float_min': (0.05, 0.01)
        }
    },

    'eatable plant type': {
        'type': 'OrganismType',
        'initial value': {
            'chose with probability': {
                'PLANT_A': 0.5,
                'PLANT_B': 0.5
            }
        },
        'value after mutation': {
            'c++ code': """
              this->eatable_plant_type = parent->eatable_plant_type;
  if(this->eatable_plant_type == PLANT_A) {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.001)) {
      this->eatable_plant_type = PLANT_B;
    }
  }
  else {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.0025))
    {
      this->eatable_plant_type = PLANT_A;
    };
  };
        """
        }
    },

    'action sequence': {
        'constant': ['hunt', 'move', 'hunt', 'update attributes', 'procreate']
    },

    'location to procreate': {
        'constant': 'adjacent'
        # The default value is 'adjacent', so this isn't necessary
    }
}

_HERBIVORE['constraints'] = {
    'can procreate': {
        'c++ code': "return (this->energy_reserve > 5000);"
    },

    'can stay alive': {
        'c++ code': "return (this->energy_reserve > 50);"
    }
}

_HERBIVORE['costs'] = {
    'subtract costs of being alive': {
        'c++ code': """
  this->energy_reserve -= 2 * this->strength;
  this->energy_reserve -= 100;
  this->energy_reserve -= 0.001 * this->max_energy_reserve_capacity;
        """
    },

    'subtract costs of procreating': {
        'c++ code': "this->energy_reserve -= 3000;"
    }
}

_CARNIVORE['inlines'] = {
    '$TEMPERATURE':
        "this->parent_biotope_ptr->temperature->get_value(this->location)"
}

_CARNIVORE['attributes'] = {

    'energy reserve': _HERBIVORE['attributes']['energy reserve'],

    'max energy reserve capacity': _HERBIVORE['attributes'][
        'max energy reserve capacity'],

    'strength': _HERBIVORE['attributes']['strength'],

    'action sequence': _HERBIVORE['attributes']['action sequence'],

    'ideal temperature': {
        'initial value': {
            'c++ code': "this->ideal_temperature = $TEMPERATURE;",
        },
        'value after mutation': {
            'uniform_mutation_float': 3.5
        }
    },

    'max temperature deviation': {
        'initial value': {
            'uniform_rand_float': (0.5, 40)
        },
        'value after mutation': {
            'proportional_mutation_float': 0.25
        }
    },

    'moving frequency': {
        'initial value': {
            'uniform_rand_float': (0.2, 1)
        },
        'value after mutation': {
            'proportional_mutation_float_min_max': (0.1, 0.0, 1.0)
        }
    },

    'moving time': {
        'initial value': 0,
        'value after mutation': 0
    }
}

_CARNIVORE['attributes']['energy reserve']['value after mutation'] = {
    'c++ code': "this->energy_reserve = 0.25 * parent->energy_reserve;"
}

_CARNIVORE['decisions'] = {

    'decide move': {
        'c++ code': """
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
        """
    },

    'decide procreate': {
        'c++ code': "return (this->energy_reserve > 5000);"
    }
}

_CARNIVORE['constraints'] = {

    'can procreate': {
        'c++ code': """
  return (
    std::abs(
      this->parent_biotope_ptr->temperature->get_value(this->location)
      - this->ideal_temperature
    ) <= this->max_temperature_deviation
  );
        """
    },

    'can stay alive': {
        'c++ code': "return (this->energy_reserve > 50);"
    }
}

_CARNIVORE['costs'] = {

    'subtract costs of moving': {
        'c++ code': """
  this->energy_reserve -= 2.5 * taxi_distance(this->location, new_location);
  this->energy_reserve -= 5.3 * this->max_temperature_deviation;
        """
    },

    'subtract costs of procreating': {
        'c++ code': """
  // proportional cost:
  this->energy_reserve -= 1.5 * offspring->energy_reserve;
  this->energy_reserve -= 5 * this->max_temperature_deviation;
  // fixed cost:
  this->energy_reserve -= 100;
  this->energy_reserve -= 0.001 * this->max_energy_reserve_capacity;
        """
    },

    'subtract cost of being alive': {
        'c++ code': """
  this->energy_reserve -= 2 * this->strength;
  this->energy_reserve -= 20;
  this->energy_reserve -= 5.8 * this->max_temperature_deviation;
  this->energy_reserve -= 0.0005 * this->max_energy_reserve_capacity;
        """
    }

}

first_example_of_ecosystem_settings = {
    'help':
    '''
        This is an example of ecosystem settings
        to automatically generate C++ code
    ''',
    'organisms types list': ['PLANT_A', 'PLANT_B', 'HERBIVORE', 'CARNIVORE'],
    'biotope': _biotope,
    'organisms': {
        'PLANT A': _PLANT_A,
        'PLANT B': _PLANT_B,
        'HERBIVORE': _HERBIVORE,
        'CARNIVORE': _CARNIVORE,
    },
}

# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******
# *******  *******  *******  *******  *******  *******  *******  *******



code_maker = CodeMaker(first_example_of_ecosystem_settings)

print code_maker.classes_hpp

text_file = open("automatic_classes.hpp", "w")
text_file.write(code_maker.classes_hpp)
text_file.close()






