//
//  classes.cpp
//  Ecosystems
//
//  Created by Juan Luis Salas García on 28/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#ifndef classes_cpp
#define classes_cpp

#include "classes.hpp"


// ***********************************************************************
//                        N O D E   M A K E R
// ***********************************************************************

void Organism_node::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  switch (this->org_type) {
    case PLANT_A:
      this->plant_A_ptr->initialize(location, biot_ptr, ecos_ptr);
      break;
    case PLANT_B:
      this->plant_B_ptr->initialize(location, biot_ptr, ecos_ptr);
      break;
    case HERBIVORE:
      this->herbivore_ptr->initialize(location, biot_ptr, ecos_ptr);
      break;
    case CARNIVORE:
      this->carnivore_ptr->initialize(location, biot_ptr, ecos_ptr);
      break;
    default:
      Error("Unknown organism type");
      break;
  };
};

void Organism_node::set_location(intLocation new_location) {
  switch (this->org_type) {
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
      Error("Unknown organism type");
      break;
  };
};

intLocation Organism_node::get_location() {
  switch (this->org_type) {
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
      Error("Unknown organism type");
      break;
  };
};

bool Organism_node::is_alive() {
  switch (this->org_type) {
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
      Error("Unknown organism type");
      break;
  };
};

void Organism_node::act_if_alive() {
  switch (this->org_type) {
    case PLANT_A:
      if(this->plant_A_ptr->is_alive) this->plant_A_ptr->act();
      break;
    case PLANT_B:
      if(this->plant_B_ptr->is_alive) this->plant_B_ptr->act();
      break;
    case HERBIVORE:
      if(this->herbivore_ptr->is_alive) this->herbivore_ptr->act();
      break;
    case CARNIVORE:
      if(this->carnivore_ptr->is_alive) this->carnivore_ptr->act();
      break;
    default:
      Error("Unknown organism type");
      break;
  };
};

void Organism_node::unlink() {
  if (this->next != nullptr)
    this->next->prev = this->prev;
  if (this->prev != nullptr)
    this->prev->next = this->next;
};

void Organism_node::insert_before(Organism_node* reference_organism) {
  this->prev = reference_organism->prev;
  this->next = reference_organism;
  reference_organism->prev = this;
  if(this->prev != nullptr) this->prev->next = this;
};

template <class T>
void Objects_pool<T>::create_more_objects() {
  this->objects_pool.push_back(std::vector<T>(this->buffer_size));
  for (auto &o : this->objects_pool.back()) {
    this->available_objects.push(&o);
  }
};

template <class T>
Objects_pool<T>::Objects_pool() {
  this->buffer_size = 100000;
  this->create_more_objects();
};

template <class T>
T* Objects_pool<T>::get_new() {
  if (this->available_objects.empty()) {
    this->create_more_objects();
  };
  T* object_ptr = this->available_objects.top();
  this->available_objects.pop();
  return object_ptr;
};

template <class T>
void Objects_pool<T>::set_available(T *object_ptr) {
  this->available_objects.push(object_ptr);
};

Organism_node* Node_maker::get_new(OrganismType org_type_) {
  Organism_node* new_node = organism_nodes_pool.get_new();
  new_node->org_type = org_type_;
  switch (org_type_) {
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
       Error("Unknown organism type");
       break;
  };
  return new_node;
};

void Node_maker::set_available(Organism_node* org_node) {
  switch (org_node->org_type) {
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
      Error("Unknown organism type");
      break;
  };
  this->organism_nodes_pool.set_available(org_node);
};



// ***********************************************************************
//                           B I O T O P E
// ***********************************************************************


Sun_light::Sun_light(Biotope &parent_biotope, Ecosystem &parent_ecosystem)
: parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem) {}; // El tamaño de la matriz es 0x0, es decir, que no hay matriz.

float Sun_light::get_value(floatLocation location) {
  return (1 + abs(sin(2 * M_PI * parent_ecosystem_ptr->cycle / 365.0))) * (1 + abs(sin(M_PI * location.second / float(parent_biotope_ptr->size_y))));
};

Temperature::Temperature(Biotope &parent_biotope, Ecosystem &parent_ecosystem)
    : parent_biotope_ptr(&parent_biotope), parent_ecosystem_ptr(&parent_ecosystem),
      data({-10, 10, 30, 30, 10, -10})
{
  // El tamaño de la matriz es 0x6, es decir, que hay 5 zonas climáticas que dependen únicamente de la latitud y no de la longitud.
};

float Temperature::get_value(intLocation location) {
  float y_float = float((data.size() - 1) * location.second)/this->parent_biotope_ptr->size_y;
  int y_int = int(std::trunc(y_float));
  y_float -= y_int;
  return data[y_int]*(1-y_float) + data[y_int + 1] * y_float;
};

void Temperature::update() {
  for(int y=0; y<data.size(); y++) {
    data[y] *= 0.95; // cada ciclo se pierde un 5% de la temperatura
    floatLocation loc(
                      0.0,
                      float(y * parent_biotope_ptr->size_y) / (data.size()-1)
                      );
    data[y] += parent_biotope_ptr->sun_light->get_value(loc); // y se gana tanta temperatura como luz solar haya en cada franja climática.
  }
};

Biotope::Biotope(Ecosystem* parent_ecosystem) {
  this->parent_ecosystem_ptr = parent_ecosystem;
  this->size_x = 500;
  this->size_y = 500;
  this->area = this->size_x * this->size_y;
  this->free_locs = std::vector<int> (this->size_x * this->size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng);
  this->free_locs_counter = 0;
  this->adjacent_locations = std::vector<intLocation> {
    make_int_location(-1, -1),
    make_int_location(-1,  0),
    make_int_location(-1,  1),
    make_int_location( 0, -1),
    make_int_location( 0,  1),
    make_int_location( 1, -1),
    make_int_location( 1,  0),
    make_int_location( 1,  1)
  };
};

ErrorType Biotope::evolve() {
  // Update those biotope features that need to be updated:
  this->temperature->update();
  return No_error;
};

Organism_node* Biotope::get_organism(intLocation location) {
  // TO DO: Check whether location belongs to this world or not
  return this->organisms_map[this->normalize(location)];
};

void Biotope::set_organism(intLocation location, Organism_node* new_organism_ptr) {
  this->organisms_map[this->normalize(location)] = new_organism_ptr;
};

void Biotope::set_organism(Organism_node* new_organism_ptr) {
  this->set_organism(new_organism_ptr->get_location(), new_organism_ptr);
};

void Biotope::remove_organism(Organism_node *organism_node) {
  this->organisms_map.erase(this->normalize(organism_node->get_location()));
};

ErrorType Biotope::move_organism(intLocation old_location, intLocation new_location) {
  // if(his->organisms_map[new_location] == nullptr) ???
  // if(his->organisms_map[old_location] != nullptr) ???
  organisms_map[new_location] = organisms_map[old_location];
  organisms_map[old_location] = nullptr;
  organisms_map[new_location]->set_location(new_location);
  return No_error;
};

int Biotope::get_num_organisms() {
  return (int)this->organisms_map.size();
};

// get random location in the biotope, NOT NECESSRAY AN EMPTY LOCATION:
intLocation Biotope::get_random_location() {
  this->free_locs_counter++;
  this->free_locs_counter %= this->area;
  if(this->free_locs_counter == 0)
    shuffle(this->free_locs.begin(), this->free_locs.end(),
            parent_ecosystem_ptr->random_nums_gen.eng);
  int packed_location = this->free_locs[this->free_locs_counter];
  return make_int_location(
                           packed_location / this->size_y,
                           packed_location % this->size_y
                           );
};

vector<intLocation> Biotope::get_free_locations(int number_of_locations) {
  if(number_of_locations + this->get_num_organisms() > this->area)   // should it return error ??
    number_of_locations = this->area - this->get_num_organisms();
  vector<intLocation> free_locations;
  free_locations.reserve(number_of_locations); // reserve memory for number_of_locations locations
  for(int i=0; i<number_of_locations; i++) {
    intLocation loc = this->get_random_location();
    while(this->organisms_map[loc] != nullptr)
      loc = this->get_random_location();
    free_locations.push_back(loc);
  };
  return free_locations;
};

intLocation Biotope::get_one_free_location() {
  if(this->get_num_organisms() < this->area) {
    intLocation loc = this->get_random_location();
    while(organisms_map[loc] != nullptr)
      loc = this->get_random_location();
    return loc;
  }
  else {
    Error("No free locations found"); // return Error;
    return NULL_LOCATION;
  };
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
      if(this->organisms_map[new_loc] == nullptr)
        free_locations_found.push_back(new_loc);
    };
  };
  if(free_locations_found.size() == 0) {
    return NULL_LOCATION;
  } else {
    return this->normalize(free_locations_found[
      this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_int(0, (int) free_locations_found.size())
    ]);
  };
};

intLocation Biotope::get_free_location_close_to(intLocation center, int radius, int number_of_attempts) {
  // This method is assumed to be used by some organisms in order to move themselves to another location. For organisms that jump very far away each time, it's very time-consuming to collect every single empty location within such a large radius, just to randomly chose one of them. That's why they should try a number of times and resign from moving if they don't find a place to do it in those attempts:
  for(int i=0; i<number_of_attempts; i++) {
    intLocation new_location = this->normalize(center + this->parent_ecosystem_ptr->random_nums_gen.get_rand_intLocation(radius));
    if(this->organisms_map[new_location] == nullptr) {
      return new_location;
    };
  };
  return NULL_LOCATION;
};

intLocation Biotope::get_free_adjacent_location(intLocation center) {
  shuffle(
          this->adjacent_locations.begin(),
          this->adjacent_locations.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng
          );
  for(intLocation location : this->adjacent_locations) {
    intLocation new_loc = this->normalize(center + location);
    if(this->organisms_map[new_loc] == nullptr) {
      return new_loc;
    };
  };
  return NULL_LOCATION;
};

Organism_node* Biotope::get_adjacent_organism_of_type(intLocation center, OrganismType org_type) {
  shuffle(
          this->adjacent_locations.begin(),
          this->adjacent_locations.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng
          );
  for(intLocation location : this->adjacent_locations) {
    intLocation new_loc = this->normalize(center + location);
    if(this->organisms_map[new_loc] != nullptr) {
      if(this->organisms_map[new_loc]->org_type == org_type) {
        return this->organisms_map[new_loc];
      };
    };
  };
  return nullptr;
};

intLocation Biotope::normalize(intLocation location) {
  return intLocation(
    location.x() % this->size_x,
    location.y() % this->size_y
  );
};


// ***********************************************************************
//                           O R G A N I S M
// ***********************************************************************


void Organism::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  
  // This function is called when an organism is created from scratch,
  // not by procreation of another organism.
  
  this->location = location;
  this->parent_ecosystem_ptr = ecos_ptr;
  this->parent_biotope_ptr = biot_ptr;
  this->is_alive = true;
};

void Organism::copy(Organism* parent) {
  // nothing to do here yet
};

void Organism::act() {};

void Organism::set_location(intLocation new_location) {
  this->location = new_location;
};

void Organism::do_procreate() {};

void Organism::mutate() {
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

void Plant_A::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->minimum_energy_reserve_for_procreating = initial_minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = initial_energy_reserve_at_birth;
  this->energy_reserve = this->initial_energy_reserve_at_birth;
};

void Plant_A::act() {
  // do photosynthesis:
  this->energy_reserve += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(make_float_location(this->location)));
  // procreate:
  if(this->decide_procreate()) this->do_procreate();
  // constraint:
  if(this->energy_reserve < 100) do_die();
};

void Plant_A::do_procreate() {
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    Organism_node* offspring = this->parent_ecosystem_ptr->node_maker.get_new(PLANT_A);
    offspring->plant_A_ptr->copy(this);
    offspring->plant_A_ptr->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->plant_A_ptr);
  };
};

void Plant_A::copy(Plant_A *parent) {
  this->minimum_energy_reserve_for_procreating = parent->minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = parent->energy_reserve_at_birth;
};

void Plant_A::mutate() {
  this->energy_reserve = this->energy_reserve_at_birth;
  this->energy_reserve_at_birth = this->parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->energy_reserve_at_birth, 0.015);
  this->minimum_energy_reserve_for_procreating = this->parent_ecosystem_ptr->random_nums_gen.uniform_mutation(this->minimum_energy_reserve_for_procreating, 7.5, this->energy_reserve_at_birth);
};

bool Plant_A::decide_procreate() {
  return this->energy_reserve > this->minimum_energy_reserve_for_procreating;
};

void Plant_A::subtract_costs_of_procreating(Plant_A *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
  // fixed cost:
  this->energy_reserve -= 50;
};


// ******************************************************************
//                         P L A N T   B
// ******************************************************************
// plant_B: plants that need much sunlight

void Plant_B::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = ecos_ptr->random_nums_gen.get_uniform_rand_float(100, 1000);
};

void Plant_B::act() {
  // do photosynthesis:
  this->energy_reserve += -25 + 34 * (this->parent_biotope_ptr->sun_light->get_value(make_float_location(this->location)));
  // procreate:
  if(this->decide_procreate()) this->do_procreate();
  // constraint:
  if(this->energy_reserve < 100) do_die();
  // if(not this->is_alive) break;
  // age:
  this->do_age();
};

void Plant_B::do_procreate() {
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    Organism_node* offspring = this->parent_ecosystem_ptr->node_maker.get_new(PLANT_B);
    // offspring->plant_B_ptr->copy(this);  // this isn't necessary
    // offspring->plant_B_ptr->mutate();    // this isn't necessary
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->plant_B_ptr);
  };
};

void Plant_B::do_age() {
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  };
};

bool Plant_B::decide_procreate() {
  return (this->energy_reserve > this->minimum_energy_reserve_for_procreating);
};

void Plant_B::subtract_costs_of_procreating(Plant_B *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.1 * offspring->energy_reserve;
};


// ******************************************************************
//                       H E R B I V O R E
// ******************************************************************

void Herbivore::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(500, 2000);
  this->strength = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 20);
  this->eatable_plant_type = this->parent_ecosystem_ptr->random_nums_gen.true_with_probability(0.5) ? PLANT_A : PLANT_B;
};

void Herbivore::act() {
  this->do_hunt();
  this->do_move();
  if(this->can_procreate()) {
    this->do_procreate();
  };
  this->subtract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Herbivore::do_move() {
  intLocation new_location = this->parent_biotope_ptr
    ->get_free_location_close_to(this->location, 4.5, 2);
  if(new_location != NULL_LOCATION) {
    this->parent_biotope_ptr->move_organism(this->location, new_location);
  };
};

void Herbivore::do_hunt() {
  Organism_node* food = this->parent_biotope_ptr
  ->get_adjacent_organism_of_type(this->location, this->eatable_plant_type);
  if(food != nullptr) {
    this->do_eat(food);
  };
};

void Herbivore::do_eat(Organism_node* food) {
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
      Error("Incorrect organism type");
      break;
  };
};

void Herbivore::do_procreate() {
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    Organism_node* offspring = this->parent_ecosystem_ptr->node_maker.get_new(HERBIVORE);
    offspring->herbivore_ptr->copy(this);
    offspring->herbivore_ptr->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->herbivore_ptr);
  };
};

void Herbivore::copy(Herbivore* parent) {
  this->strength = parent->strength;
  this->eatable_plant_type = parent->eatable_plant_type;
};

void Herbivore::mutate() {
  this->energy_reserve = 500;
  this->strength =
  parent_ecosystem_ptr->random_nums_gen
  .proportional_mutation(this->strength, 0.05, 0.01);
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
};

bool Herbivore::can_procreate() {
  return (this->energy_reserve > 2000);
};

void Herbivore::subtract_costs_of_being_alive() {
  this->energy_reserve -= this->strength;
  this->energy_reserve -= 5;
}

void Herbivore::subtract_costs_of_procreating(Herbivore *offspring) {
  // fixed cost:
  this->energy_reserve -= 600;
};


// ******************************************************************
//                       C A R N I V O R E
// ******************************************************************

void Carnivore::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(1500, 4000);
  this->strength = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 20);
  this->ideal_temperature = biot_ptr->temperature->get_value(location);
  this->max_temperature_deviation = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 40);
  this->moving_frequency = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.2, 1);
  this->moving_time = 0.0;
};


void Carnivore::act() {
  this->do_hunt();
  if(this->decide_move()) {
    this->do_move();
  };
  this->do_hunt(); // yes, again
  if(this->decide_procreate() and this->can_procreate()) {
    this->do_procreate();
  };
  this->subtract_costs_of_being_alive();
  if(this->energy_reserve<10) {
    this->do_die();
  };
};

void Carnivore::do_move() {
  intLocation new_location = this->parent_biotope_ptr
  ->get_free_location_close_to(this->location, 6.5, 4);
  if(new_location != NULL_LOCATION) {
    this->subtract_costs_of_moving(new_location);
    this->parent_biotope_ptr->move_organism(this->location, new_location);
  };
};

void Carnivore::do_hunt() {
  Organism_node* food = this->parent_biotope_ptr
  ->get_adjacent_organism_of_type(this->location, HERBIVORE);
  if(food != nullptr) {
    this->do_try_to_eat(food->herbivore_ptr);
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
  herbivore->do_die();
};

void Carnivore::do_procreate() {
  // get location:
  intLocation free_location = this->parent_biotope_ptr->get_free_adjacent_location(this->location);
  if(free_location != NULL_LOCATION) {
    Organism_node* offspring = this->parent_ecosystem_ptr->node_maker.get_new(CARNIVORE);
    offspring->carnivore_ptr->copy(this);
    offspring->carnivore_ptr->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this->node);
    this->subtract_costs_of_procreating(offspring->carnivore_ptr);
  };
};

void Carnivore::copy(Carnivore* parent) {
  this->strength = parent->strength;
  this->ideal_temperature = parent->ideal_temperature;
  this->max_temperature_deviation = parent->max_temperature_deviation;
  this->moving_frequency = parent->moving_frequency;
  this->moving_time = 0.0;
};

void Carnivore::mutate() {
  this->energy_reserve *= 0.25;
  
  this->strength =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation(this->strength, 0.05, 0.01);
    
  this->ideal_temperature = parent_ecosystem_ptr->random_nums_gen
  .uniform_mutation(this->ideal_temperature, 3.5);
  
  this->max_temperature_deviation =
    parent_ecosystem_ptr->random_nums_gen
    .proportional_mutation(this->max_temperature_deviation, 0.25);
  
  this->moving_frequency = parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->moving_frequency, 0.1, 0.0, 1.0);
  
  this->moving_time = 0.0;
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

bool Carnivore::can_procreate() {
  return (
    std::abs(
      this->parent_biotope_ptr->temperature->get_value(this->location)
      - this->ideal_temperature
    ) <= this->max_temperature_deviation
  );
};

void Carnivore::subtract_costs_of_moving(intLocation new_location) {
  this->energy_reserve -= 2.5 * taxi_distance(this->location, new_location);
  this->energy_reserve -= 0.2 * this->max_temperature_deviation;
};

void Carnivore::subtract_costs_of_procreating(Carnivore *offspring) {
  // proportional cost:
  this->energy_reserve -= 1.5 * offspring->energy_reserve;
  this->energy_reserve -= this->max_temperature_deviation;
  // fixed cost:
  this->energy_reserve -= 100;
};

void Carnivore::subtract_costs_of_being_alive() {
  this->energy_reserve -= this->strength;
  this->energy_reserve -= 5;
  this->energy_reserve -= 0.1 * this->max_temperature_deviation;
};



// ******************************************************************
//                           E C O S Y S T E M
// ******************************************************************

Ecosystem::Ecosystem() : biotope(this) {
  this->random_nums_gen.set_seed(0);
  this->cycle = 0;
  this->first_organism_node = nullptr;
  this->last_organism_node = nullptr;
  this->ghost_organisms_ptrs = {};
};

void Ecosystem::create_new_organisms(OrganismType organism_type, int number_of_new_organisms) {
  for(int i = 0; i < number_of_new_organisms; i++) {
    this->create_one_new_organism(organism_type);
  };
};

void Ecosystem::create_one_new_organism(OrganismType organism_type) {
  Organism_node* new_organism = this->node_maker.get_new(organism_type);
  intLocation location = this->biotope.get_one_free_location();
  new_organism->initialize(location, &(this->biotope), this);
  this->biotope.set_organism(location, new_organism);
  this->append_organism(new_organism);
};

void Ecosystem::append_first_organism(Organism_node *first_organism) {
  this->first_organism_node = first_organism;
  this->last_organism_node = first_organism;
  first_organism->prev = nullptr;
  first_organism->next = nullptr;
  this->biotope.set_organism(first_organism);
};

void Ecosystem::append_organism(Organism_node* new_organism) {
  if(this->first_organism_node == nullptr) {
    this->append_first_organism(new_organism);
  }
  else {
    this->insert_new_organism_before(new_organism, this->first_organism_node);
    this->first_organism_node = new_organism;
  };
};

void Ecosystem::insert_new_organism_before(Organism_node* new_organism, Organism_node* reference_organism) {
  // We assume that:
  //    this->first_organism_node != nullptr
  //    reference_organism != nullptr
  this->biotope.set_organism(new_organism);
  if(reference_organism == this->first_organism_node) {
    this->first_organism_node = new_organism;
  };
  new_organism->insert_before(reference_organism);
};

void Ecosystem::append_organisms_list(Organism_node* organism) {
  if (this->first_organism_node == nullptr) {
    this->first_organism_node = organism;
  };
  while (organism != nullptr) {
    organism->prev = this->last_organism_node;
    if (this->last_organism_node != nullptr)
      this->last_organism_node->next = organism;
    this->last_organism_node = organism;
    this->biotope.set_organism(organism);
    organism = organism->next;
  };
};

int Ecosystem::get_num_organisms() {
  return (int)this->biotope.get_num_organisms();
};

void Ecosystem::evolve() {
  this->clear_ghost_organisms();
  Organism_node* organism = this->first_organism_node;
  while (organism != nullptr) {
    organism->act_if_alive();
    organism = organism->next;
  };
  this->biotope.evolve();
  this->cycle += 1;
};

void Ecosystem::move_dead_organism_to_ghost_list(intLocation location) {
  this->move_dead_organism_to_ghost_list(this->biotope.get_organism(location));
};

void Ecosystem::move_dead_organism_to_ghost_list(Organism* org) {
  this->move_dead_organism_to_ghost_list(org->node);
};

void Ecosystem::move_dead_organism_to_ghost_list(Organism_node* organism_node) {
  this->biotope.remove_organism(organism_node);
  organism_node->unlink();
  this->ghost_organisms_ptrs.push_back(organism_node);
};

void Ecosystem::clear_ghost_organisms() {
  for (auto &ghost_organism_ptr : this->ghost_organisms_ptrs) {
    this->node_maker.set_available(ghost_organism_ptr);
  };
  this->ghost_organisms_ptrs.clear();
};




#endif /* classes_cpp */
