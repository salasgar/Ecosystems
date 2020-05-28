#include <chrono>
//#include <random>
#include <iostream>
#include <numeric>
#include "organism.hpp"
#include "math.h"
#define _USE_MATH_DEFINES

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

// class Organism:

void Organism::reset(intLocation location,
                     Base_ecosystem* parent_ecosystem_ptr) {
  this->next = nullptr;
  this->prev = nullptr;
  this->location = location;
  this->parent_ecosystem_ptr = parent_ecosystem_ptr;
  this->is_alive = true;
  // const int MAX_AGE = 2000;
};

void Organism::copy(Organism* model_organism) {
  // nothing to do here yet
};

void Organism::act() {};

void Organism::change_location_to(intLocation new_location) {
  this->location = new_location;
};

void Organism::do_procreate() {
  // if decide_procreate() {
  // get location:
  intLocation free_location(0, 0);
  if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, this->location) == NoError) {
    Organism* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
    offspring->copy(this);
    offspring->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
    // this->subtract_costs_of_procreating(offspring);
  };
  // };
};

void Organism::mutate() {
  // nothing to do here yet
};

void Organism::do_die() {
  this->is_alive = false;
  this->parent_ecosystem_ptr->kill_and_remove_organism(this->location);
};

void Organism::unlink() {
  if (this->next != nullptr)
    this->next->prev = this->prev;
  if (this->prev != nullptr)
    this->prev->next = this->next;
};



// ******************************************************************
//                           P L A N T S
// ******************************************************************

// plant_A: plants that can live with little sunlight

// class Plant_A::Energy_reserve
Plant_A::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope),
data(initial_value)
{};

float Plant_A::Energy_reserve::get_value() {
  return data;
}

void Plant_A::Energy_reserve::update() { // do photosynthesis:
  this->data += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(make_float_location(parent_organism_ptr->location)));
};

void Plant_A::Energy_reserve::set_value(float new_value) {
  this->data = new_value;
};
// end of definition of Plant_A::Energy_reserve

Plant_A::Plant_A() : energy_reserve(this->parent_biotope_ptr, this, this->initial_energy_reserve_at_birth){
  this->minimum_energy_reserve_for_procreating = initial_minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = initial_energy_reserve_at_birth;
};

void Plant_A::do_procreate() {
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) == NoError) {
      Plant_A* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->subtract_costs_of_procreating(offspring);
    };
  // };
};

void Plant_A::copy(Organism* model_organism) {
  this->minimum_energy_reserve_for_procreating = model_organism->minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = model_organism->energy_reserve_at_birth;
};

void Plant_A::mutate() {
  this->energy_reserve.set_value(this->energy_reserve_at_birth);
  this->energy_reserve_at_birth = this->parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->energy_reserve_at_birth, maximum_proportion = 0.015);
  this->minimum_energy_reserve_for_procreating = this->parent_ecosystem_ptr->random_nums_gen.uniform_mutation(this->minimum_energ_reserve_for_procreating, maximum_increment = 7.5, minimum_value = this->energy_reserve_at_birth);
};

bool Plant_A::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_A::act() {
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
};

void Plant_A::subtract_costs_of_procreating(Plant_A *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
  // fixed cost:
  this->energy_reserve -= 50;
};


// plant_B: plants that need much sunlight

Plant_B::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope), data(initial_value) {};

void Plant_B::Energy_reserve::update() {
  this->data += -25 + 34 * (this->parent_biotope_ptr->sun_light->get_value(parent_organism_ptr->location));
};

Plant_B::Plant_B(Biotope *parentBiotope) : energy_reserve(parentBiotope, this, 1000.0), age(0) {};

void Plant_B::do_age() {
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  };
};

void Plant_B::do_procreate() {
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) == NoError) {
      Plant_B* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->subtract_costs_of_procreating(offspring);
    };
  // };
};

bool Plant_B::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_B::act() {
  this->do_age();
  if(not this->is_alive) break;
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
};

void Plant_B::subtract_costs_of_procreating(Plant_B *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
};

Herbivore::Herbivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

void Herbivore::act() {
  this->do_hunt();
  this->do_move();
  if(this->can_procreate()) {
    this->do_procreate();
  };
  this->substract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Herbivore::do_move() {
  intLocation new_location();
  if(
     this->parent_biotope_ptr->get_free_location_close_to(
        new_location,
        this->location,
        4.5,
        2) == No_error
     ) {
    this->change_location_to(new_location);
  };
};

void Herbivore::do_hunt() {
  intLocation prey_location();
  if(
    this->parent_biotope_ptr
      ->get_adjacent_organism_of_type(
          prey_location,
          this->location,
          this->favorite_food
      ) == No_error) {
    this->do_eat(this->parent_biotope_ptr->organisms_map[prey_location]);
  };
};

void Herbivore::do_eat(Plant_A *plant_a) {
  this->energy_reserve += plant_a->energy_reserve;
  plant_a->do_die();
};

void Herbivore::do_eat(Plant_B *plant_b) {
  this->energy_reserve += plant_b->energy_reserve;
  plant_b->do_die();
};

void Herbivore::do_procreate() {
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) == NoError) {
      Herbivore* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->subtract_costs_of_procreating(offspring);
    };
  // };
};

void Herbivore::mutate() {
  this->energy_reserve = 500;
  this->strength =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation(this->strength, 0.05, 0.01);
  if(typeid(this->favorite_food) == typeid(Plant_A)) {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.1)) {
      this->favorite_food = typeid(Plant_B);
    }
  }
  else {
    if(this->parent_ecosystem_ptr->random_nums_gen
       .true_with_probability(0.25))
    {
      this->favorite_food = typeid(Plant_A);
    };
  };
};

bool Herbivore::can_procreate() {
  return (this->energy_reserve > 2000);
};

void Herbivore::substract_costs_of_being_alive() {
  this->energy_reserve -= this->strength;
  this->energy_reserve -= 5;
}
  
void Herbivore::substract_costs_of_procreating(Herbivore *offspring) {
  // fixed cost:
  this->energy_reserve -= 600;
};


// *****************  C A R N I V O R E  ******************
Carnivore::Carnivore(Biotope *parentBiotope) {
  parent_biotope_ptr = parentBiotope;
};

void Carnivore::act() {
  this->do_hunt();
  if(this->decide_move()) {
    this->do_move();
  };
  this->do_hunt(); // yes, again
  if(this->decide_procreate()) {
    this->do_procreate();
  };
  this->substract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Carnivore::do_move() {
  intLocation new_location();
  if(
     this->parent_biotope_ptr->get_free_location_close_to(
        new_location,
        this->location,
        6.5,
        4) == No_error
     ) {
    this->subtract_costs_of_moving(new_location);
    this->change_location_to(new_location);
  };
};

void Carnivore::do_hunt() {
  intLocation prey_location();
  if(this->parent_biotope_ptr->get_adjacent_organism_of_type(
                                                          prey_location,
                                                          this->location,
                                                          typeid(Herbivore)
                                                             ) == No_error) {
    this->do_try_to_eat(this->parent_biotope_ptr->organisms_map[prey_location]);
  };
};

void Carnivore::do_try_to_eat(Herbivore *herbivore) {
  if(this->parent_ecosystem_ptr->random_nums_gen
     .true_with_probability(this->strength / (this->strength + herbivore->strength))) {
    this->do_eat(herbivore);
  };
};
  
void Carnivore::do_eat(Herbivore *herbivore) {
  this->energy_reserve += herbivore->energy_reserve;
  hervibore->do_die();
};

void Carnivore::do_procreate() {
  // if decide_procreate() {
    // get location:
    intLocation free_location;
    if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, center = this->location) == NoError) {
      Carnivore* offspring = this->parent_ecosystem_ptr->organisms_pool.get_new(free_location, this->parent_ecosystem_ptr);
      offspring->copy(this);
      offspring->mutate();
      // Add offspring to ecosystem:
      this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
      this->subtract_costs_of_procreating(offspring);
    };
  // };
};

void Carnivore::mutate() {
  this->energy_reserve *= 0.25;
  this->strength =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation(this->strength, 0.05, 0.01);
  this->moving_frequency = parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->moving_frequency, 0.1, 0.01, 1.0);
  this->moving_time = 0;
};

bool Carnivore::decide_move() {
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

bool Carnivore::decide_procreate() {
  return (this->energy_reserve > 5000);
};

/*
 bool Carnivore::can_eat(Organism *organism) {
  if(typeid(*organism) == typeid(Herbivore)) {
    return true;
  }
  else {
    return false;
  }
};
*/

void Carnivore::substract_costs_of_being_alive() {
  this->energy_reserve -= this->strength;
  this->energy_reserve -= 5;
}

void Carnivore::substract_costs_of_moving(intLocation new_location) {
  this->energy_reserve -= 2.5 * taxi_distance(this->location, new_location);
};

void Carnivore::substract_costs_of_procreating(Carnivore *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.5 * offspring->energy_reserve;
  // fixed cost:
  this->energy_reserve -= 100;
};
