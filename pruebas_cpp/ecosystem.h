#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>


class Organism;
class Ecosystem;

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
  void _delete_dead_organisms();
 public:
  Organism* first_organism;
  RandomNumbersGenerator random_nums_gen;
  OrganismsPool organisms_pool;
  int time;
  std::vector<Organism*> dead_organisms_ptrs;
  Biotope biotope;
  Ecosystem();
  void evolve();
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