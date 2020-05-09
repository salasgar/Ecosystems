#include <pybind11/pybind11.h>
#include "ecosystem.h"

namespace py = pybind11;

PYBIND11_MODULE(eco, m) {
  py::class_<Ecosystem>(m, "Ecosystem")
    .def(py::init<>())
    .def("get_num_organisms", &Ecosystem::get_num_organisms)
    .def("get_num_free_locations", &Ecosystem::get_num_free_locations)
    .def("evolve", &Ecosystem::evolve);
}

