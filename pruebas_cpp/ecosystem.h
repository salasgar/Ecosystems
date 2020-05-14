#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>

typedef std::pair<int, int> tLocation;
typedef std::pair<float, float> fLocation;
typedef enum {No_error, Error_Organism_not_found, Error_no_free_location_found} ErrorType;

class Sun_light;
class Temperature;
class Ecosystem;
class Biotope;
class Organism;
class OrganismsPool;
class RandomNumbersGenerator;


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
  Sun_light *sun_light;
  Temperature *temperature;
 public:
  Biotope(Ecosystem* parent_ecosystem_ptr);
  ErrorType evolve();
  Organism* get_organism(tLocation location);
  ErrorType add_organism(Organism* new_organism_ptr, tLocation location);
  ErrorType move_organism(tLocation old_location, tLocation new_location);
};

class Ecosystem {
  void _clear_ghost_organisms();
 public:
  Organism* first_organism_node;
  Organism* last_organism_node;
  RandomNumbersGenerator random_nums_gen;
  OrganismsPool organisms_pool;
  long int cycle;
  std::vector<Organism*> ghost_organisms_ptrs;
  Biotope biotope;
 public:
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
  Biotope* parent_biotope_ptr;
  std::pair<int, int> location;
 public:
  void reset(std::pair<int, int> location,
             Ecosystem* parent_ecosystem_ptr);
  void act();
  void do_die();
  void unlink();
  void change_location(tLocation old_location, tLocation new_location);
};

class Sun_light {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  float get_value(fLocation location);
  Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
};

class Temperature {
 public:
  std::vector<float> data;
  Biotope *parent_biotope_ptr;
  Ecosystem *parent_ecosystem_ptr;
 public:
  Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem);
  float get_value(tLocation location);
  void update();
};

class Plant_A : public Organism {

  class Energy_reserve {
   public:
    float data;
    Organism *parent_organism_ptr;
    Biotope *parent_biotope_ptr;
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update();
    float get_value();
  };

 // class Plant_A:
public:
 static const int photosynthesis_capacity = 100;
 Energy_reserve energy_reserve;
public:
 void do_photosynthesis();
 void procreate();
 // decisions:
 bool decide_procreate();
}; // *************** class Plant_A ***************

class Plant_B : public Organism {

  class Energy_reserve {
   public:
    float data;
    Organism *parent_organism_ptr;
    Biotope *parent_biotope_ptr;
    Energy_reserve(Biotope parentBiotope, Organism parentOrganism, float initial_value);
    void update();
  };

  // class Plant_B:
 public:
  static const int photosynthesis_capacity = 120;
  static const int death_age = 1000;
  Energy_reserve energy_reserve;
  int age;
 public:
  Plant_B(Biotope parentBiotope);
  void do_photosynthesis();
  void do_age();
  void do_procreate();
  void act();
};  // *************** class Plant_B ***************

class Herbivore : public Organism {
 public:
  float energy_reserve;
 public:
  Herbivore(Biotope parentBiotope);
  void do_move();
  void do_hunt();
  void do_eat(Plant_A plant_a);
  void do_eat(Plant_B plant_b);
};

class Carnivore : public Organism {
  public:
   float energy_reserve;
  public:
   Carnivore(Biotope parentBiotope);
   void do_move();
   void do_hunt();
   void do_eat(Herbivore hervibore);
};


#endif  // ECOSYSTEM_H_INCLUDED
