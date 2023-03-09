#ifndef IBM_SIMULATION_H
#define IBM_SIMULATION_H
/**
 * @file ibm_simulation_4th_doses.h
 * @author Eamon Conway (conway.e@wehi.edu.au)
 * @brief
 * @version 0.1
 * @date 2021-11-23
 *
 * @copyright Copyright (c) 2021
 *
 */
#include <functional>
#include <random>
#include <vector>

#include "abm/abm_json.tpp"
#include "abm/individual.h"

/**
 * @brief
 *
 */
class DiseaseOutput {
 private:
  VaccineType vaccine;
  double age;
  double time_symptom_onset;
  double time_isolated;
  double log10neuts_at_exposure;
  int secondary_infections;
  int number_infections;
  bool symptomatic;
  int cluster_number;

 public:
  DiseaseOutput(const Individual& person);
  friend std::ostream& operator<<(std::ostream& os, const DiseaseOutput& covid);
  const double & getTimeSymptoms() const;
  int countInfection(const double & t);
};

/**
 * @brief
 *
 */
class disease_model {
 private:
  // Output files.
  std::vector<DiseaseOutput> output;  // Output file. Dynamically add.
  // Neutralising antibody components - make private as they wont change.
  double k;
  double c50_acquisition;
  double c50_symptoms;
  double c50_transmission;
  double sd_log10_neut_titres;
  double log10_mean_neut_infection;
  double log10_mean_neut_AZ_dose_1;
  double log10_mean_neut_AZ_dose_2;
  double log10_mean_neut_Pfizer_dose_1;
  double log10_mean_neut_Pfizer_dose_2;
  double log10_mean_neut_Pfizer_dose_3;
  double log10_mean_neut_bivalent_booster;
  // double log10_mean_additional_neut;
  double log10_omicron_neut_fold;
  double priorStrainFold;

  std::function<double(double&)> mobility_;

 public:
  /**
   * @brief Print all parameters in covid.
   *
   */
  void print_params();

  /**
   * @brief Construct a new disease model object
   *
   * @param beta_C_in double vector
   * @param q
   * @param xi
   * @param contact_matrix_in
   * @param b
   * @param w
   * @param ve_params
   */

    /**
     * @brief Construct a new disease model object with the priorStrainFold 
     */
    disease_model(
      std::vector<double> beta_C_in, std::vector<double> q,
      std::vector<double> xi,
      std::vector<std::vector<double>> contact_matrix_in, std::vector<double> b,
      std::vector<double> w, nlohmann::json& ve_params,
      std::function<double(double&)> mobility_function =
          [](double& t) -> double { return 1.0; },double priorStrainFold = 1.0);

  /**
   * @brief Construct a new disease model object
   *
   * @param beta_C
   * @param q
   * @param xi
   * @param contact_matrix_in
   * @param b
   * @param w
   */
  disease_model(double beta_C, double q, double xi,
                std::vector<std::vector<double>> contact_matrix_in,
                std::vector<double> b, std::vector<double> w);


    /**
     * @brief Assigns log10_mean_neut_bivalent_booster if/when bivalent boosting is happening
     * 
     */
    void set_bivalent_booster(double bivalentBoosterParam);

  std::vector<double> beta_C; /**<  Community transmission probability.*/
  std::vector<double> xi;     /**< Age stratified susceptibility. */
  std::vector<double> q;      /**< Probability of symptoms */
  std::vector<std::vector<double>>
      contact_matrix; /**< Contacts per day in each age bracket.*/

  const std::vector<std::vector<double>>
      contact_matrix_base; /**< Contacts per day in each age bracket.*/

  // Distributions! The disease model should initialise some distributions that
  // wil be used!
  std::gamma_distribution<double>
      gen_tau_E; /**< Time moving from exposed to infected. */
  std::gamma_distribution<double>
      gen_tau_S; /**< Time from infected to symptoms. */
  std::gamma_distribution<double>
      gen_tau_R; /**< Time from infected to recovered. */
  std::piecewise_constant_distribution<double>
      gen_tau_isolation; /**< Time before symptoms the Individual is isolated.*/

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
   * @param newly_symptomatic Reference to an empty dynamic array that will be
   * filled with an index corresponding to all individuals that become
   * infectious between t0 and t1.
   * @return double Returns the new current time, t1.
   */
  double covid_ascm(std::vector<Individual>& residents,
                    std::vector<std::vector<int>>& age_ref, double t0,
                    double t1, double dt, std::vector<size_t>& E,
                    std::vector<size_t>& I,
                    std::vector<size_t>& newly_symptomatic);

  /**
   * @brief Run a single step of the COVID-19 Age Stratified Contact Model.
   *
   * @param residents Vector containing all individuals.
   * @param age_ref
   * @param t0 Start time.
   * @param dt Size of timestep to be taken.
   * @param E Vector of indices to exposed individuals.
   * @param I Vector of indices to infectious individuals.
   * @param newly_symptomatic Reference to an empty dynamic array that will be
   * filled with an index corresponding to all individuals that become
   * infectious between t0 and t1.
   * @return double Returns the new time t0 + dt.
   */
  double covid_one_step_ascm(std::vector<Individual>& residents,
                             std::vector<std::vector<int>>& age_ref, double t0,
                             double dt, std::vector<size_t>& E,
                             std::vector<size_t>& I,
                             std::vector<size_t>& newly_symptomatic);

  /**
   * @brief Run the infection model for an infected individual.
   *
   * @param t The current time.
   * @param infected_individual Reference to the infected individual of
   * interest.
   * @param residents Vector containing all individuals.
   * @param age_ref
   * @param dt Size of timestep.
   * @param[in,out] newly_exposed Reference to an empty dynamic array that will
   * be filled with the indices of newly exposed individuals.
   * @param mobility How much is the number of contacts made scaled by.
   */
  void infection_ascm(double t, Individual& infected_individual,
                      std::vector<Individual>& residents,
                      std::vector<std::vector<int>>& age_ref, double dt,
                      std::vector<size_t>& newly_exposed);

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
  bool distribution_exposed_update(Individual& person, size_t& ind_number,
                                   std::vector<size_t>& newly_infectious,
                                   double& t);

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
  bool distribution_infected_update(Individual& person, size_t& ind_number,
                                    std::vector<size_t>& newly_symptomatic,
                                    double& t);

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
  double covid_ascm_R0(std::vector<Individual>& residents,
                       std::vector<std::vector<int>>& age_ref, double t0,
                       double t1, double dt, std::vector<size_t>& E,
                       std::vector<size_t>& I,
                       std::vector<size_t>& newly_symptomatic);

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
  double covid_one_step_ascm_R0(std::vector<Individual>& residents,
                                std::vector<std::vector<int>>& age_ref,
                                double t0, double dt, std::vector<size_t>& E,
                                std::vector<size_t>& I,
                                std::vector<size_t>& newly_symptomatic);

  // Seed infection
  void seed_exposure(Individual& resident, double& t);

  // Functions for each event.
  void expose_individual(Individual& person, double& t);
  void infect_individual(Individual& person);
  void recover_individual(Individual& person);
  void susceptible_individual(Individual& person);

  double getSusceptibility(const Individual& person,
                           double& t);  // (1-ProtectInfection)*xi
  double getProbabilitySymptomatic(const Individual& person,
                                   double& t);  // (1- PS)*q
  void assignTransmissibility(Individual& person, double& t,
                              bool& asymptomatic);  // (1-PO)

  double getProtectionInfection(const Individual& person, double& t);
  double getProtectionSymptoms(const Individual& person, double& t);
  double getProtectionOnwards(const Individual& person, double& t);

  double calculateNeuts(const Individual& person, double& t);
  void boostNeutsInfection(Individual& person, double& t);

  // Vaccination.
  void boostNeutsVaccination(Individual& person, double& t,
                             VaccineType& vaccine);

  double getNeutsNaive(const Individual& person, const double& t,
                       const VaccineType& vaccine);
  double getNeutsWithExposure(const Individual& person, const double& t,
                               const VaccineType& vaccine);


  // Get some output. 
  int getTotalFirstInfections(const double & t);
  
  // friend std::ostream& operator<<(std::ostream& os, const
  // std::vector<DiseaseOutput>& covid); /**< Overloaded ostream for output */
  friend std::ostream& operator<<(std::ostream& os, const disease_model& covid);
};

std::ostream& operator<<(std::ostream& os, const DiseaseOutput& covid);
std::ostream& operator<<(std::ostream& os,
                         const std::vector<DiseaseOutput>& covid);
std::ostream& operator<<(std::ostream& os, const disease_model& covid);
#endif