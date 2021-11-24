#ifndef IBM_SIMULATION_H
#define IBM_SIMULATION_H
/**
 * @file ibm_simulation.h
 * @author Eamon Conway (conway.e@wehi.edu.au)
 * @brief 
 * @version 0.1
 * @date 2021-11-23
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include <vector>
#include <random>
#include "abm/individual.h"

/**
 * @brief 
 * 
 */
class disease_model{
  public:
  /**
   * @brief Construct a new disease model object
   * 
   * @param beta_C_in 
   * @param contact_matrix_in 
   * @param b 
   * @param w 
   */
  disease_model(std::vector<double> beta_C_in, std::vector<std::vector<double>> contact_matrix_in,std::vector<double> b,std::vector<double> w);

  /**
   * @brief Construct a new disease model object
   * 
   * @param beta_H 
   * @param beta_C 
   * @param contact_matrix_in 
   * @param b 
   * @param w 
   */
  disease_model(double beta_C, std::vector<std::vector<double>> contact_matrix_in,std::vector<double> b,std::vector<double> w);

  std::vector<double> beta_C; /**<  Community transmission probability.*/
  

  std::vector<std::vector<double>> contact_matrix; /**< Contacts per day in each age bracket.*/
  
  // Distributions! The disease model should initialise some distributions that wil be used!
  std::gamma_distribution<double> gen_tau_E; /**< Time moving from exposed to infected. */
  std::gamma_distribution<double> gen_tau_S; /**< Time from infected to symptoms. */
  std::gamma_distribution<double> gen_tau_R; /**< Time from infected to recovered. */
  std::piecewise_constant_distribution<double> gen_tau_isolation; /**< Time before symptoms the Individual is isolated.*/
  
  
  /**
   * @brief COVID-19 Age Stratified Contact Model. 
   * 
   * @param residents Vector containing all individuals. 
   * @param age_ref 
   * @param t0 Start time. 
   * @param t1 Finish time. 
   * @param dt Size of timestep to be taken (dt <= t1-t0).
   * @param E Vector of indices to exposed individuals. 
   * @param I Vector of indices to infectious individuals. 
   * @param newly_symptomatic Reference to an empty dynamic array that will be filled with an index corresponding to all individuals that become infectious between t0 and t1. 
   * @return double Returns the new current time, t1. 
   */
  double  covid_ascm(std::vector<Individual>& residents,  std::vector<std::vector<int>>& age_ref, double t0, double t1, double dt, std::vector<size_t>& E, std::vector<size_t>& I, std::vector<size_t>& newly_symptomatic);

  /**
   * @brief Run a single step of the COVID-19 Age Stratified Contact Model. 
   * 
   * @param residents Vector containing all individuals. 
   * @param age_ref 
   * @param t0 Start time. 
   * @param dt Size of timestep to be taken.
   * @param E Vector of indices to exposed individuals. 
   * @param I Vector of indices to infectious individuals. 
   * @param newly_symptomatic Reference to an empty dynamic array that will be filled with an index corresponding to all individuals that become infectious between t0 and t1. 
   * @return double Returns the new time t0 + dt. 
   */
  double  covid_one_step_ascm(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double dt, std::vector<size_t>& E, std::vector<size_t>& I, std::vector<size_t>& newly_symptomatic);

  /**
   * @brief Run the infection model for an infected individual. 
   * 
   * @param t The current time. 
   * @param infected_individual Reference to the infected individual of interest. 
   * @param residents Vector containing all individuals. 
   * @param age_ref 
   * @param dt Size of timestep. 
   * @param[in,out] newly_exposed Reference to an empty dynamic array that will be filled with the indices of newly exposed individuals. 
   */
  void    infection_ascm(double t, Individual&infected_individual, std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double dt, std::vector<size_t>& newly_exposed);

  /**
   * @brief 
   * 
   * @param person 
   * @param ind_number 
   * @param newly_infectious 
   * @param t 
   * @return true 
   * @return false 
   */
  bool    distribution_exposed_update(Individual& person, size_t& ind_number, std::vector<size_t>& newly_infectious, double& t);

  /**
   * @brief 
   * 
   * @param person 
   * @param ind_number 
   * @param newly_symptomatic 
   * @param t 
   * @return true 
   * @return false 
   */
  bool    distribution_infected_update(Individual& person, size_t& ind_number, std::vector<size_t>& newly_symptomatic, double& t);

  /**
   * @brief 
   * 
   * @param residents 
   * @param age_ref 
   * @param t0 
   * @param t1 
   * @param dt 
   * @param E 
   * @param I 
   * @param newly_symptomatic 
   * @return double 
   */
  double covid_ascm_R0(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double t1, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic);

  /**
   * @brief 
   * 
   * @param residents 
   * @param age_ref 
   * @param t0 
   * @param dt 
   * @param E 
   * @param I 
   * @param newly_symptomatic 
   * @return double 
   */
  double  covid_one_step_ascm_R0(std::vector<Individual>& residents,  std::vector<std::vector<int>>& age_ref, double t0, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic);  

  // Seed infection
  void seed_infection(Individual&resident);
  void seed_infection(Individual&resident);
  void seed_exposure(Individual& resident);
  void seed_exposure(Individual& resident, double& t);

  // Expose infect and recover an Individual. 
  void expose_individual(Individual&);
  void infect_individual(Individual&);
  void recover_individual(Individual&);
  void susceptible_individual(Individual& resident);

  // Expose infect and recover an Individual.
  void expose_individual(Individual&, double&);
  void infect_individual(Individual&, double&);
  void recover_individual(Individual&, double&);
  void susceptible_individual(Individual& resident, double&);
};
#endif
