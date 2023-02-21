#ifndef VAX_INFECTION_SCENARIO_READ_H
#define VAX_INFECTION_SCENARIO_READ_H
/**
 * @file vax_infection_scenario_read_many_boosters.h
 * @author Thao P. Le ()
 * @brief Functions required for reading in vaccination-infection scenario input
 * @version 0.1
 * @date 2023-02-02
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include <vector>
#include <random>
#include "abm/individual.h"
#include "nlohmann/json.hpp"

std::vector<Individual> read_individuals_from_input_many_boosters(std::string vaccination_infection_filename, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params);


#endif