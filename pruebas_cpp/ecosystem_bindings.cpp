#include <pybind11/pybind11.h>
#include "classes.hpp"

namespace py = pybind11;



PYBIND11_MODULE(eco, m) {
  py::enum_<OrganismType>(m, "OrganismType")
    .value("PLANT_A", OrganismType::PLANT_A)
    .value("PLANT_B", OrganismType::PLANT_B)
    .value("HERBIVORE", OrganismType::HERBIVORE)
    .value("CARNIVORE", OrganismType::CARNIVORE)
    .export_values();

  py::class_<Ecosystem>(m, "Ecosystem")
    .def(py::init<>())
    .def("initialize", &Ecosystem::initialize)
    .def("get_num_organisms", &Ecosystem::get_num_organisms)
    .def("create_new_organisms", &Ecosystem::create_new_organisms)
    .def("evolve", &Ecosystem::evolve);
}

