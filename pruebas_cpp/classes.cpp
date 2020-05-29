//
//  classes.cpp
//  Ecosystems
//
//  Created by Juan Luis Salas García on 28/05/2020.
//  Copyright © 2020 Juan Luis Salas García. All rights reserved.
//

#include "classes.hpp"

void Organism_node::set_location(intLocation new_location) {
  switch (this->org_type) {
    case PLANT_A:
      plant_A_ptr->set_location(new_location);
      break;
    case PLANT_B:
      plant_B_ptr->set_location(new_location);
      break;
    case HERBIVORE:
      herbivore_ptr->set_location(new_location);
      break;
    case CARNIVORE:
      carnivore_ptr->set_location(new_location);
      break;
    default:
      Error("Unknown organism type");
      break;
  }
};

intLocation Organism_node::get_location() {
  switch (this->org_type) {
    case PLANT_A:
      return plant_A_ptr->location;
      break;
    case PLANT_B:
      return plant_B_ptr->location;
      break;
    case HERBIVORE:
      return herbivore_ptr->location;
      break;
    case CARNIVORE:
      return carnivore_ptr->location;
      break;
    default:
      Error("Unknown organism type");
      break;
  }
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



// -----------------------------------------------------------------------
//                           B I O T O P E
// -----------------------------------------------------------------------


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
  floatLocation loc(3.2, 3.3);
  
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
  int BIOTOPE_SIZE_X = 500;
  int BIOTOPE_SIZE_Y = 500;
  this->size_x = BIOTOPE_SIZE_X;
  this->size_y = BIOTOPE_SIZE_Y;
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
  return this->organisms_map[location];
};

ErrorType Biotope::add_organism(Organism_node* new_organism_ptr, intLocation location) {
  // if(his->organisms_map[location] == nullptr) ???
  this->organisms_map[location] = new_organism_ptr;
  return No_error;
};

ErrorType Biotope::move_organism(intLocation old_location, intLocation new_location) {
  // if(his->organisms_map[new_location] == nullptr) ???
  // if(his->organisms_map[old_location] != nullptr) ???
  organisms_map[new_location] = organisms_map[old_location];
  organisms_map[old_location] = nullptr;
  organisms_map[new_location]->change_location_to(new_location);
  return No_error;
};

int Biotope::get_num_organisms() {
  return (int)this->organisms_map.size();
};

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
    return make_int_location(1/0, 1/0); // return Error;
  };
};

ErrorType Biotope::get_free_location_close_to(intLocation &free_location, intLocation center, int radius) {
  // Use this method only with small radiuses. Otherwise, it's very time-consuming.
  std::vector<intLocation> free_locations_found = {};
  for(int x = center.x() - radius;
      x <= center.x() + radius;
      x++) {
    for(int y = center.y() - radius;
        y <= center.y() + radius;
        y++) {
      if(this->organisms_map[intLocation(x, y)] == nullptr)
        free_locations_found.push_back(intLocation(x, y));
    };
  };
  if(free_locations_found.size() == 0) {
    return Error_No_free_location_found;
  } else {
    free_location = free_locations_found[
                                         this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_int(0, free_locations_found.size())
                                         ];
    return No_error;
  };
};

ErrorType Biotope::get_free_location_close_to(intLocation &free_location, intLocation center, int radius, int number_of_attempts) {
  // This method is assumed to be used by some organisms in order to move themselves to another location. For organisms that jump very far away each time, it's very time-consuming to collect every single empty location within such a large radius, just to randomly chose one of them. That's why they should try a number of times and resign from moving if they don't find a place to do it in those attempts:
  for(int i=0; i<number_of_attempts; i++) {
    intLocation new_location = center + this->parent_ecosystem_ptr->random_nums_gen.get_rand_intLocation(radius);
    if(this->organisms_map[new_location] == nullptr) {
      free_location = new_location;
      return No_error;
    };
  };
  return Error_No_free_location_found;
};

ErrorType Biotope::get_free_adjacent_location(intLocation &free_location, intLocation center) {
  shuffle(
          this->adjacent_locations.begin(),
          this->adjacent_locations.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng
          );
  for(intLocation location : this->adjacent_locations) {
    if(this->organisms_map[center + location] == nullptr) {
      free_location = center + location;
      return No_error;
    };
  };
  return Error_No_free_location_found;
};

ErrorType Biotope::get_adjacent_organism_of_type(intLocation &org_loc, intLocation center, std::type_info org_type) {
  shuffle(
          this->adjacent_locations.begin(),
          this->adjacent_locations.end(),
          this->parent_ecosystem_ptr->random_nums_gen.eng
          );
  for(intLocation location : this->adjacent_locations) {
    if(this->organisms_map[center + location] != nullptr) {
      if(typeid(*(this->organisms_map[center + location])) == org_type) {
        org_loc = center + location;
        return No_error;
      };
    };
  };
  return Error_No_free_location_found;
};




// -----------------------------------------------------------------------
//                           O R G A N I S M
// -----------------------------------------------------------------------


void Organism::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  
  // This function is called when an organism is created from scratch,
  // not by procreation of another organism.

  this->reset(location, biot_ptr, ecos_ptr);
};

void Organism::reset(intLocation location, Ecosystem* ecos_ptr) {
  this->reset(location, &(ecos_ptr->biotope), ecos_ptr);
};

void Organism::reset(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  this->node->next = nullptr;
  this->node->prev = nullptr;
  this->location = location;
  this->parent_ecosystem_ptr = ecos_ptr;
  this->parent_biotope_ptr = biot_ptr;
  this->is_alive = true;
};

void Organism::copy(Organism* parent) {
  // nothing to do here yet
};

void Organism::act() {};

void Organism::change_location_to(intLocation new_location) {
  this->location = new_location;
};

void Organism::do_procreate() {};

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

void Plant_A::Energy_reserve::update() { // do photosynthesis:
  this->data += -10 + 20 * (this->parent_biotope_ptr->sun_light->get_value(make_float_location(parent_organism_ptr->location)));
};

void Plant_A::Energy_reserve::set_value(float new_value) {
  this->data = new_value;
};

float Plant_A::Energy_reserve::get_value() {
  return data;
};

void Plant_A::Energy_reserve::add(float increment) {
  this->data += increment;
};

void Plant_A::Energy_reserve::subtract(float decrement) {
  this->data -= decrement;
};

Plant_A::Plant_A() : energy_reserve(nullptr, this, 0){};

void Plant_A::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->minimum_energy_reserve_for_procreating = initial_minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = initial_energy_reserve_at_birth;
  this->energy_reserve.set_value(initial_energy_reserve_at_birth);
};

/*
void Plant_A::reset(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::reset(location, biot_ptr, ecos_ptr);
};
*/

void Plant_A::act() {
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
};

void Plant_A::do_procreate() {
  // if decide_procreate() {
  // get location:
  intLocation free_location;
  if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, this->location) == No_error) {
    Plant_A* offspring = this->parent_ecosystem_ptr->plants_A_pool.get_new(free_location, this->parent_ecosystem_ptr);
    offspring->copy(this);
    offspring->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
    this->subtract_costs_of_procreating(offspring);
  };
  // };
};

void Plant_A::copy(Plant_A *parent) {
  this->minimum_energy_reserve_for_procreating = parent->minimum_energy_reserve_for_procreating;
  this->energy_reserve_at_birth = parent->energy_reserve_at_birth;
};

void Plant_A::mutate() {
  this->energy_reserve.set_value(this->energy_reserve_at_birth);
  this->energy_reserve_at_birth = this->parent_ecosystem_ptr->random_nums_gen.proportional_mutation(this->energy_reserve_at_birth, 0.015);
  this->minimum_energy_reserve_for_procreating = this->parent_ecosystem_ptr->random_nums_gen.uniform_mutation(this->minimum_energy_reserve_for_procreating, 7.5, this->energy_reserve_at_birth);
};

bool Plant_A::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_A::subtract_costs_of_procreating(Plant_A *offspring) {
  // proportional cost:
  this->energy_reserve.subtract(1.1 * offspring->energy_reserve.get_value());
  // fixed cost:
  this->energy_reserve.subtract(50);
};


// plant_B: plants that need much sunlight

Plant_B::Energy_reserve::Energy_reserve(Biotope *parentBiotope, Organism *parentOrganism, float initial_value) : parent_organism_ptr(parentOrganism), parent_biotope_ptr(parentBiotope), data(initial_value) {};

void Plant_B::Energy_reserve::update() {
  this->data += -25 + 34 * (this->parent_biotope_ptr->sun_light->get_value(make_float_location(parent_organism_ptr->location)));
};

void Plant_B::Energy_reserve::set_value(float new_value) {
  this->data = new_value;
};

float Plant_B::Energy_reserve::get_value() {
  return data;
};

void Plant_B::Energy_reserve::add(float increment) {
  this->data += increment;
};

void Plant_B::Energy_reserve::subtract(float decrement) {
  this->data -= decrement;
};

Plant_B::Plant_B() : energy_reserve(nullptr, this, 0) {};

void Plant_B::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve.set_value(ecos_ptr->random_nums_gen.get_uniform_rand_float(100, 1000));
};

void Plant_B::act() {
  this->energy_reserve.update(); // do photosynthesis
  if(this->decide_procreate()) this->do_procreate();
  if(this->energy_reserve.data < 100) do_die(); // Constraint
  // if(not this->is_alive) break;
  this->do_age();
};

void Plant_B::do_procreate() {
  // if decide_procreate() {
  // get location:
  intLocation free_location;
  if(this->parent_biotope_ptr->get_free_adjacent_location(free_location, this->location) == No_error) {
    Plant_B* offspring = this->parent_ecosystem_ptr->plants_B_pool.get_new(free_location, this->parent_ecosystem_ptr);
    // offspring->copy(this);  // this isn't necessary
    offspring->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
    this->subtract_costs_of_procreating(offspring);
  };
  // };
};

void Plant_B::do_age() {
  this->age += 1;
  if (this->age > this->death_age) {
    this->do_die();
  };
};

bool Plant_B::decide_procreate() {
  return this->energy_reserve.get_value() > this->minimum_energy_reserve_for_procreating;
};

void Plant_B::subtract_costs_of_procreating(Plant_B *offspring) {
  // proportional cost:
  this->energy_reserve.subtract(1.1 * offspring->energy_reserve.get_value());
};

// *** HERBIVORE: ***

void Herbivore::initialize(intLocation location, Biotope* biot_ptr, Ecosystem* ecos_ptr) {
  Organism::initialize(location, biot_ptr, ecos_ptr);
  this->energy_reserve = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(500, 2000);
  this->strength = this->parent_ecosystem_ptr->random_nums_gen.get_uniform_rand_float(0.5, 20);
  this->can_eat_plant_type = this->parent_ecosystem_ptr->random_nums_gen.true_with_probability(0.5) ? 'A' : 'B';
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
  intLocation new_location;
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
  intLocation prey_location;
  if(
     this->parent_biotope_ptr
     ->get_adjacent_organism_of_type(
         prey_location,
         this->location,
         Plant_A
         ) == No_error) {
    this->do_eat(prey_location);
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
    Herbivore* offspring = this->parent_ecosystem_ptr->herbivores_pool.get_new(free_location, this->parent_ecosystem_ptr);
    offspring->copy(this);
    offspring->mutate();
    // Add offspring to ecosystem:
    this->parent_ecosystem_ptr->insert_new_organism_before(offspring, this);
    this->subtract_costs_of_procreating(offspring);
  };
  // };
};

void Herbivore::reset(intLocation location, Ecosystem* parent_ecosystem_ptr) {
  Organism::reset(location, parent_ecosystem_ptr);
};



void Herbivore::copy(Herbivore* parent);


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
    Carnivore* offspring = this->parent_ecosystem_ptr->carnivores_pool.get_new(free_location, this->parent_ecosystem_ptr);
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




// -----------------------------------------------------------------------
//                           E C O S Y S T E M
// -----------------------------------------------------------------------


void Ecosystem::clear_ghost_organisms() {
  for (auto &ghost_organism_ptr : this->ghost_organisms_ptrs) {
    this->node_maker.set_available(ghost_organism_ptr);
  };
  this->ghost_organisms_ptrs.clear();
};

Ecosystem::Ecosystem() {
  this->biotope_ptr = Biotope(this);
  this->random_nums_gen.set_seed(0);
  this->cycle = 0;
  const int INITIAL_NUM_ORGANISMS = 200000;
  this->first_organism_node = nullptr;
  this->last_organism_node = nullptr;
  this->ghost_organisms_ptrs = {};
  vector<int> free_locs(this->biotope.size_x * this->biotope.size_y);
  iota (begin(free_locs), end(free_locs), 0);
  shuffle(free_locs.begin(), free_locs.end(),
          this->random_nums_gen.eng);
  int free_loc_int, loc_x, loc_y;
  for (int i=0; i < INITIAL_NUM_ORGANISMS; i++) {
    free_loc_int = free_locs.back(); // to do: use Biotope::get_free_locations()
    free_locs.pop_back();
    loc_x = free_loc_int / this->biotope.size_y;
    loc_y = free_loc_int % this->biotope.size_y;
    Organism* o = this->organisms_pool.get_new(make_pair(loc_x, loc_y), this);
    this->append_organisms(o);
  };
};

void Ecosystem::insert_new_organism_before(Organism* new_organism, Organism* reference_organism) {
  new_organism->prev = reference_organism->prev;
  new_organism->next = reference_organism;
  reference_organism->prev = new_organism;
  new_organism->prev->next = new_organism;
  this->biotope.organisms_map[new_organism->location] = new_organism;
};

void Ecosystem::add_new_organisms(int number_of_new_organisms) {
  for (int i=0; i < number_of_new_organisms; i++) {
    intLocation new_location = this->biotope.get_one_free_location();
    Organism* o = this->organisms_pool.get_new(new_location, this);
    this->append_organisms(o);
  };
};

void Ecosystem::append_organisms(Organism* organism) {
  if (this->first_organism_node == nullptr) {
    this->first_organism_node = organism;
  };
  while (organism != nullptr) {
    organism->prev = this->last_organism_node;
    if (this->last_organism_node != nullptr)
      this->last_organism_node->next = organism;
    this->last_organism_node = organism;
    this->biotope.organisms_map[organism->location] = organism;
    organism = organism->next;
  };
};

void Ecosystem::evolve() {
  this->clear_ghost_organisms();
  this->biotope.evolve();
  Organism* organism = this->first_organism_node;
  while (organism != nullptr) {
    if (organism->is_alive) {
      organism->act();
    };
    organism = organism->next;
  };
  this->cycle += 1;
};

void Ecosystem::kill_and_remove_organism(Organism_node* organism_node) {
  organism_node->kill();
  biotope.organisms_map.erase(organism_node->get_location());
  organism_node->unlink();
  this->ghost_organisms_ptrs.push_back(organism_node);
};

void Ecosystem::add_new_organisms(OrganismType organism_type, int number_of_new_organisms) {
  for(int i = 0; i < number_of_new_organisms; i++) {
    intLocation location = this->biotope.get_one_free_location();
    Organism_node* new_node = this->create_new_organism(organism_type);
    switch (organism_type) {
      case PLANT_A:
        new_node->plant_A_ptr->initialize(location, &(this->biotope), this);
        break;
      case PLANT_B:
        new_node->plant_B_ptr->initialize(location, &(this->biotope), this);
        break;
      case HERBIVORE:
        new_node->herbivore_ptr->initialize(location, &(this->biotope), this);
        break;
      case CARNIVORE:
        new_node->carnivore_ptr->initialize(location, &(this->biotope), this);
        break;
    };
    this->append_organism(new_node);
  };
};

Organism_node* Ecosystem::create_new_organism(OrganismType organism_type) {
  return this->node_maker.get_new(organism_type);
};

int Ecosystem::get_num_organisms() {
  return (int)this->biotope.organisms_map.size();
};




