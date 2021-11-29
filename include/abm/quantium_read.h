#ifndef QUANTIUM_READ_H
#define QUANTIUM_READ_H
#include <vector>
#include <random>
std::vector<std::uniform_real_distribution<double>> read_age_generation(std::string dim_age_filename, double max_age);
#endif