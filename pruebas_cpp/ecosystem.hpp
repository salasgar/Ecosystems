#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
#include <random>
#include <stack>
#include <vector>
#include "pool_of_organisms.hpp"
#include "biotope.hpp"
#include "organism.hpp"


class Sun_light;
class Temperature;
class Ecosystem;
class Biotope;
class Organism;
class OrganismsPool;
class RandomNumbersGenerator;

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
 // methods:
  Ecosystem();
  void append_organisms(Organism* organisms);
  void evolve();
  void kill_and_remove_organism(Organism* organism);
  int get_num_organisms();
};

#endif  // ECOSYSTEM_H_INCLUDED
