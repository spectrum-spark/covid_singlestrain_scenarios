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
#include<vector>

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

  // state infection_status; // At one point this wil lbe built into the code instead of characters. 

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
  double  transmissibility = std::nan("1"); // Assigned at time of exposure. Is a function of vaccination. This is a constant throughout transmission so reassigned here at exposure (else just use vaccine::get_transmissibility(t).
  
  // When does event occur.
  double  time_of_exposure         = std::nan("1");
  double  time_of_symptom_onset    = std::nan("2");
  double  time_of_infection        = std::nan("3");
  double  time_of_recovery         = std::nan("4");

  // Latch to determine if pre-symptomatic time is over.
  bool    check_symptoms           = true; // Symptomatic latch.
  
  // Future development.
  int cluster_number = -1; // We can track the clusters through time. That could be fun. It can be passed from exposure to exposure.

};


/**
 * @brief Define what properties a base Individual object requires. 
 * 
 */
class Individual{
  private:

  protected:

  public:

  /**
   * @brief Construct a new Individual object
   * @details Create an individual using the output from QUANTIUM.
   * 
   * @param age 
   * @param age_bracket 
   */
  Individual(double& age, int& age_bracket); 
  
  int   age_bracket; /**< Age bracket of the individual */
  int   secondary_infections; /**< The number of individuals that they have infected. */ 
  
  double age; /**< Age of the individual.*/
  double log10_neutralising_antibodies; /**< Level of neutralising antibodies.*/ 
  double old_log10_neutralising_antibodies; /**< Old level of neutralising antibodies (the value that it was at the time of the boost, but before it was boosted).*/

  double  time_last_boost; /**< Time of the last boost to neutralising antibodies. */
  double  decay_rate; /**< Rate of neutralising antibody decay. This could be defined upon creation of the individual? */ 

  double  time_isolated; /**< The time an individual starts isolation.*/
  // const double xi; /**< Base susceptibility */ 

  bool isCovidNaive; /**< Has the individual been infected previously? This is required for determining the height of the boost. */ 
  bool isVaccinated; /**< Has the individual recieved a vaccine dose. */

  /**
   * @brief Disease status of the individual stored in an object. 
   * 
   */
  Disease covid; /**< Set up the disease parameters for the individual. */ // It would be cool to have some pointer indirection here and allow for an arbitrary disease. 

  // std::vector<Vaccine> vaccinations; /**< Dynamic array that stores vaccination times for the individual */ 
};
#endif