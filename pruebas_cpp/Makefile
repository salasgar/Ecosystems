py:
	clang++ -O3 -undefined dynamic_lookup -shared -std=c++17 -fPIC `python -m pybind11 --includes` basic_tools.cpp classes.cpp ecosystem_bindings.cpp -o eco.so
cli:
	clang++ -O3 -std=c++17 test_main.cpp basic_tools.cpp classes.cpp -o test_main
