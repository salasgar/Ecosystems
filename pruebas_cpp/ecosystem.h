#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <tuple>
#include <set>
#include <vector>

class Organism;
class Ecosystem;

class Biotope {
 public:
  Ecosystem* parent_ecosystem_ptr;
  int size_x;
  int size_y;
  std::map<std::tuple<int, int>, Organism*> organisms_map;
  std::set<std::tuple<int, int>> free_locs;
  Biotope();
  std::tuple<int, int> get_random_free_location();
};

class Ecosystem {
  void _delete_dead_organisms();
 public:
  int time;
  std::vector<Organism*> dead_organisms_ptrs;
  Biotope biotope;
  Ecosystem();
  void evolve();
  int get_num_organisms();
  int get_num_free_locations();
  void add_organism(Organism* organism_ptr);
  void remove_organism(Organism* organism_ptr);
};

class Organism {
 public:
  bool is_alive;
  Ecosystem* parent_ecosystem_ptr;
  std::tuple<int, int> location;
  int age;
  int death_age;
  Organism(std::tuple<int, int> location, Ecosystem* parent_ecosystem_ptr);
  void act();
  void do_age();
  void do_die();
};

#endif  // ECOSYSTEM_H_INCLUDED