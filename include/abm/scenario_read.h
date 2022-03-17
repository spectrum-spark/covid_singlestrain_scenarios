#ifndef SCENARIO_READ_H
#define SCENARIO_READ_H
/**
 * @file scenario_read.h
 * @author Thao P. Le ()
 * @brief Functions required for reading in vaccination-infection scenario input
 * @version 0.1
 * @date 2022-03-16
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include <vector>
#include <random>
#include "abm/individual.h"
#include "nlohmann/json.hpp"

std::vector<Individual> read_individuals_assignment(std::string vaccination_infection_filename, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params);

std::vector<Individual> read_individuals_data(std::string neuts_vaccination_infection_filename, std::vector<double> &age_brackets, nlohmann::json &ve_params);


#endif