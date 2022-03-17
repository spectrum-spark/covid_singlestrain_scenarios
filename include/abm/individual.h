#ifndef WANEWORLD_ABM_INDIVIDUAL_H
#define WANEWORLD_ABM_INDIVIDUAL_H
/**
 * @file individual.h
 * @author Eamon Conway (conway.e@wehi.edu.au)
 * @brief 
 * @version 0.1
 * @date 2021-11-15
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include <vector>
#include <iostream>
#include "nlohmann/json.hpp"

enum class VaccineType {AZ1, AZ2, Pfizer1, Pfizer2, Moderna1, Moderna2, Booster,Unvaccinated};

std::ostream& operator<<(std::ostream& os, const VaccineType& vaccine);

/**
 * @brief 
 * 
 */
class Disease
{
    public:
  /**
   * @enum Define all possible states that the DiseaseModel can have. 
   * 
   */
  // enum class state{
  //   S, /**< Susceptible flag. */
  //   E, /**< Exposed flag. */
  //   I, /**< Infectious flag. */
  //   R  /**< Recovered flag (may be ignored in the waning immunity project). */
  // };

  // state infection_status; // At one point this will be built into the code instead of characters. 

  /**
   * @brief Construct a new disease object
   * 
   */
  Disease(char );

  // Public member data
  char    infection_status;               //  Determine if individual is S E I R or whatever you want really... 
  bool    asymptomatic = false;           //  Is the individual asymptomatic. 
  bool    severe = false;                 //  Is this a severe disease.
  
  // Variables that are assigned at time of exposure.
  double  transmissibility; // Assigned at time of exposure. Is a function of vaccination. This is a constant throughout transmission so reassigned here at exposure (else just use vaccine::get_transmissibility(t).
   
  // When does event occur.
  double  time_of_exposure;
  double  time_of_symptom_onset;
  double  time_of_infection;
  double  time_of_recovery;

  double log10_neuts_at_exposure; // For storing and outputs. 

  // Latch to determine if pre-symptomatic time is over.
  bool    check_symptoms; // Symptomatic latch.
  
  // Future development.
  int cluster_number; // We can track the clusters through time. That could be fun. It can be passed from exposure to exposure. -1 will be the default value. 

  VaccineType vaccine_at_exposure;
  friend std::ostream& operator<<(std::ostream& os, const Disease& covid); /**< Overloaded ostream for output */

};

// /**
//  * @brief Define the properties of a vaccination. 
//  * 
//  */
// class Vaccination {
//   private:

//   protected:

//   public:

//   double time;
//   VaccineType vaccine;
// };

/**
 * @brief Define what properties a base Individual object requires. 
 * 
 */
class Individual{
  private:
  

  protected:

  public:
  using VaccineHistory = std::vector<std::pair<double, VaccineType>>;

  /**
   * @brief Construct a new Individual object
   * @details Create an individual using the output from QUANTIUM.
   * 
   * @param age 
   * @param age_bracket 
   */
  Individual(double& age, std::vector<double>& age_brackets, std::vector<std::pair<double,VaccineType>>& Vaccinations, nlohmann::json& ve_params); 

  Individual(double& age, std::vector<double>& age_brackets, std::vector<std::pair<double,VaccineType>>& Vaccinations, nlohmann::json& ve_params, size_t &num_infections, double &time_of_past_infection); 

  Individual(double& age, std::vector<double>& age_brackets, std::vector<std::pair<double,VaccineType>>& Vaccinations, nlohmann::json& ve_params, size_t &num_infections, double &time_of_past_infection, double &log10_neuts, bool &isCovidNaive, bool &isVaccinated);
  
  bool isCovidNaive; /**< Has the individual been infected previously? This is required for determining the height of the boost. Currently unused. */ 
  bool isVaccinated; /**< Has the individual recieved two doses of vaccine. */

  int   age_bracket; /**< Age bracket of the individual */
  int   secondary_infections; /**< The number of individuals that they have infected. */
  int number_infections;  /**< The number of infections they have received. */

  double time_past_infection;  /**< Time of past infection if any */
  
  double age; /**< Age of the individual.*/
  double log10_neutralising_antibodies; /**< Level of neutralising antibodies.*/ 
  double old_log10_neutralising_antibodies; /**< Old level of neutralising antibodies (the value that it was at the time of the boost, but before it was boosted).*/
  double  time_last_boost; /**< Time of the last boost to neutralising antibodies. */
  double  decay_rate; /**< Rate of neutralising antibody decay. This could be defined upon creation of the individual? */ 
  double  time_isolated; /**< The time an individual starts isolation.*/
 
  Disease covid; /**< Set up the disease parameters for the individual. */ // It would be cool to have some pointer indirection here and allow for an arbitrary disease. 

  VaccineHistory vaccinations; /**< Dynamic array that stores vaccination times for the individual */ 
  
  friend std::ostream& operator<<(std::ostream& os, const Individual& person); /**< Overloaded ostream for output */
};
#endif