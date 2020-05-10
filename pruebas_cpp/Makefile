py:
	clang++ -O3 -undefined dynamic_lookup -shared -std=c++17 -fPIC `python -m pybind11 --includes` ecosystem.cpp ecosystem_bindings.cpp -o eco.so
cli:
	clang++ -O3 -std=c++17 test_main.cpp ecosystem.cpp -o test_main
prof:
	clang++ -g -O3 -std=c++17 test_main.cpp ecosystem.cpp -o test_main