# coding: utf-8
import os
cpp_code = """
#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j + $x;
}

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
}
"""
with open('example.cpp', 'w') as f:
    f.write(str(cpp_code.replace('$x', '1')))
    
os.system("clang -O3 -undefined dynamic_lookup -shared -std=c++11 -fPIC `python -m pybind11 --includes` example.cpp -o example.so")
import example
print(example.add(1, 1))
os.remove('example.cpp')
os.remove('example.so')
