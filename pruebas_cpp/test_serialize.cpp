// Example program
#include <iostream>
#include <string>
#include <fstream>
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

int main()
{
  json data;
  data["a"] = 2;
  data["b"] = "hola";
  cout << data;
  ofstream myfile;
  myfile.open ("example.json");
  myfile << data;
  myfile.close();

  json data2;
  ifstream myfile2;
  myfile2.open ("example.json");
  myfile2 >> data2;
  myfile2.close();

  cout << data2 << endl;
}
