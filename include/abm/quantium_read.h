#ifndef QUANTIUM_READ_H
#define QUANTIUM_READ_H
/**
 * @file quantium_read.h
 * @author Eamon Conway (conway.e@wehi.edu.au)
 * @brief Functions required for using Quantium data. 
 * @version 0.1
 * @date 2021-11-30
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include <vector>
#include <random>
#include "abm/individual.h"

/**
 * @brief Read in the age generations. 
 * 
 * @param dim_age_filename 
 * @param max_age 
 * @return std::vector<std::uniform_real_distribution<double>> 
 */
std::vector<std::uniform_real_distribution<double>> read_age_generation(std::string dim_age_filename, double max_age);

/**
 * @brief This is an unsafe file, it does not check format and assumes that it is the same as what was given to my by Quantium. 
 * 
 * @param vaccinations_filename 
 * @param generate_age
 * @return std::vector<Individual> 
 */
std::vector<Individual> read_individuals(std::string vaccinations, std::vector<std::uniform_real_distribution<double>>& generate_age,std::vector<double> & age_brackets);
#endif