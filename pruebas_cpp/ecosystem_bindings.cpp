#include <pybind11/pybind11.h>
#include "classes.hpp"

namespace py = pybind11;


PYBIND11_MODULE(eco, m) {
  py::enum_<OrganismType>(m, "OrganismType")
    .value("NULL_ORGANISM_TYPE", OrganismType::NULL_ORGANISM_TYPE)
    .value("ALL_TYPES", OrganismType::ALL_TYPES)
    .value("PLANT_A", OrganismType::PLANT_A)
    .value("PLANT_B", OrganismType::PLANT_B)
    .value("HERBIVORE", OrganismType::HERBIVORE)
    .value("CARNIVORE", OrganismType::CARNIVORE)
    .export_values();

  py::enum_<OrganismAttribute>(m, "OrganismAttribute")
    .value("ENERGY_RESERVE", OrganismAttribute::ENERGY_RESERVE)
    .value("AGE", OrganismAttribute::AGE)
    .value("DEATH_AGE", OrganismAttribute::DEATH_AGE)
    .value("GENERATION", OrganismAttribute::GENERATION)
    .value("PHOTOSYNTHESIS_CAPACITY", OrganismAttribute::PHOTOSYNTHESIS_CAPACITY)
    .value("STRENGTH", OrganismAttribute::STRENGTH)
    .value("MINIMUM_ENERGY_RESERVE_FOR_PROCREATING", OrganismAttribute::MINIMUM_ENERGY_RESERVE_FOR_PROCREATING)
    .value("ENERGY_RESERVE_AT_BIRTH", OrganismAttribute::ENERGY_RESERVE_AT_BIRTH)
    .value("EATABLE_PLANT_TYPE", OrganismAttribute::EATABLE_PLANT_TYPE)
    .value("IDEAL_TEMPERATURE", OrganismAttribute::IDEAL_TEMPERATURE)
    .value("MAX_TEMPERATURE_DEVIATION", OrganismAttribute::MAX_TEMPERATURE_DEVIATION)
    .value("MOVING_FREQUENCY", OrganismAttribute::MOVING_FREQUENCY)
    .export_values();
  
  py::enum_<BiotopeAttribute>(m, "BiotopeAttribute")
    .value("SUN_LIGHT", BiotopeAttribute::SUN_LIGHT)
    .value("TEMPERATURE", BiotopeAttribute::TEMPERATURE)
    .export_values();


  py::class_<Ecosystem>(m, "Ecosystem")
    .def(py::init<>())
    .def("initialize", &Ecosystem::initialize)
    .def("create_new_organisms", &Ecosystem::create_new_organisms)
    .def("evolve", &Ecosystem::evolve)
    .def("get_attribute_matrix", &Ecosystem::get_attribute_matrix)
    .def("keep_number_of_organisms_above", &Ecosystem::keep_number_of_organisms_above)
    .def("get_num_organisms", &Ecosystem::get_num_organisms)
    .def("get_num_organisms_of_type", &Ecosystem::get_num_organisms_of_type)
    .def("mean_of_attribute", &Ecosystem::mean_of_attribute)
    .def("variance_of_attribute", &Ecosystem::variance_of_attribute)
    .def("max_of_attribute", &Ecosystem::max_of_attribute)
    .def("min_of_attribute", &Ecosystem::min_of_attribute)
    .def("mean_of_attribute_several_types", &Ecosystem::mean_of_attribute_several_types)
    .def("variance_of_attribute_several_types", &Ecosystem::variance_of_attribute_several_types)
    .def("max_of_attribute_several_types", &Ecosystem::max_of_attribute_several_types)
    .def("min_of_attribute_several_types", &Ecosystem::min_of_attribute_several_types);

  py::class_<Matrix>(m, "Matrix", py::buffer_protocol())
    .def(py::init<Ecosystem &, OrganismAttribute, OrganismType>())
    .def(py::init<Ecosystem &, BiotopeAttribute>())
    .def_buffer([](Matrix &m) -> py::buffer_info {
      return py::buffer_info(
        m.data(),                               /* Pointer to buffer */
        sizeof(float),                          /* Size of one scalar */
        py::format_descriptor<float>::format(), /* Python struct-style format descriptor */
        2,                                      /* Number of dimensions */
        { m.rows(), m.cols() },                 /* Buffer dimensions */
        { sizeof(float) * m.cols(),             /* Strides (in bytes) for each index */
          sizeof(float) }
      );
    });

}

