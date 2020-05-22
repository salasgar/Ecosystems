#ifndef ECOSYSTEM_H_INCLUDED
#define ECOSYSTEM_H_INCLUDED
#include <map>
#include <utility>
#include <set>
//#include <random>
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
  void insert_new_organism_before(Organism* new_organism, Organism* reference_organism);
  void append_organisms(Organism* organisms);
  void evolve();
  void kill_and_remove_organism(Organism* organism);
  void add_new_organisms(int number_of_new_organisms);
  int get_num_organisms();
};

#endif  // ECOSYSTEM_H_INCLUDED

/*
 COMANDOS GIT:
 
 git add -u
 git commit -m "Rename few files"
 git push origin pruebas_cpp
 
 */
