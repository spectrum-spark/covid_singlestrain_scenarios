/**
 * @file main_generate_initial_conditions.cpp
 * @author ..
 * @brief generate initial conditions for the start of the actual 'winter wave'
 * output: files containing age, date of vaccinations and infections, and final log10 neuts;
 * the log10neuts and age are the important inputs [as are vaccination history and infections, I guess]
 * @version 0.1
 * @date 2022-03-15
 *
 * @copyright Copyright (c) 2022
 *
 */

#include <sys/stat.h>
#include <sys/types.h>

#include <fstream>
#include <iostream>
#include <sstream>

#include "abm/abmrandom.h"
#include "abm/ibm_simulation.h"
#include "abm/quantium_read.h"
#include "nlohmann/json.hpp"

nlohmann::json load_json(std::string filename)
{
    std::ifstream json_stream(filename);
    if (!json_stream.is_open())
    {
        throw std::logic_error("Json is not found. \n FILENAME : " + filename +
                               "\n");
    }
    // Convert input to json.
    nlohmann::json json_output;
    json_stream >> json_output;
    json_stream.close(); // Close the file.

#ifdef DUMP_INPUT
    // Dump json output to terminal. Final checks.
    std::cout << filename << std::endl;
    std::cout << json_output.dump(4) << "\n\n";
#endif

    return json_output;
}

int main(int argc, char *argv[])
{
    // Read in parameters.
    if (argc == 1)
    {
        std::cout << "ERROR: Parameter file not loaded!" << std::endl;
        return 1;
    }
    if (argc != 6)
    { // todo: fill this in once I know the number of input parameters needed
        std::cout << "ERROR did not load enough values" << std::endl;
        return 1;
    }

    // Neut parameters read in here.
    std::string neut_parameters_filename(argv[1]);
    nlohmann::json neuts_json = load_json(neut_parameters_filename);

    // double sd_log10_neut_titres = neuts_json["sd_log10_neut_titres"];
    // double k = exp(static_cast<double>(neuts_json["log_k"]));
    // double c50_acquisition = neuts_json["c50_acquisition"];
    // double c50_symptoms = neuts_json["c50_symptoms"];
    // double c50_transmission = neuts_json["c50_transmission"];
    // double log10_mean_neut_infection = neuts_json["log10_mean_neut_infection"];
    // double log10_mean_neut_AZ_dose_1 = neuts_json["log10_mean_neut_AZ_dose_1"];
    // double log10_mean_neut_AZ_dose_2 = neuts_json["log10_mean_neut_AZ_dose_2"];
    // double log10_mean_neut_Pfizer_dose_1 = neuts_json["log10_mean_neut_Pfizer_dose_1"];
    // double log10_mean_neut_Pfizer_dose_2 = neuts_json["log10_mean_neut_Pfizer_dose_2"];
    // double log10_mean_neut_Pfizer_dose_3 = neuts_json["log10_mean_neut_Pfizer_dose_3"];
    // double log10_mean_additional_neut = neuts_json["log10_mean_additional_neut"];
    // double decay_rate = neuts_json["neut_decay"];

// construct individuals
// create residents
// assign initial neutralising antibodies to all residents 

// generate, for each individual, vaccination dates and infection dates according to input values about total number of vaccinations and infections 

// then, potentially, construct mostly empty disease model object and then use its to apply the effect of vaccination and infection and thus modify the neuts:

// initial neuts prior vaccination and infection

// update neuts occording to vaccination dates and infection dates and decay appropriately using boostNeutsVaccination for each vaccination
// and assigning covid.vaccine_at_exposure + boostNeutsInfection for each infection

// double disease_model::calculateNeuts(const Individual &person, double &t) {
//   return person.log10_neutralising_antibodies -
//          person.decay_rate * (t - person.time_last_boost) /
//              log(10.0);  // We are working in log neuts so if exponential is in
//                          // base e then k is log10(e)*k. Decay rate can be put in disease model as it does not depend upon the individual in our current implementation. This is something to look at. 
// }

// Set Neut levels!  You have been exposed to covid your neutralising
  // antibodies will now do a thing.
//   boostNeutsInfection(resident, t);  // What do the neuts go to (also assigns
//                                      // old Neutralising antibody levels)

//   // Set statistics for tracking - required for log10 neuts.
//   // Write log10 neuts for MOC.
//   resident.covid.log10_neuts_at_exposure =
//       resident.old_log10_neutralising_antibodies;


//   resident.secondary_infections = 0;
//   ++resident.number_infections; // Increase the times theyve been infected. 



// static void assignNewNeutValue(const double &log10_neuts,
//                                const double &sd_log10_neuts, Individual &person,
//                                double &t) {
//   // Might include ucrrent neuts as inputs.
//   std::normal_distribution<double> sample_neuts(log10_neuts, sd_log10_neuts);
//   double new_neuts = sample_neuts(generator);


//   if (new_neuts >= person.old_log10_neutralising_antibodies) {
//     person.log10_neutralising_antibodies = new_neuts;
//   } else {
//     person.log10_neutralising_antibodies =
//         person.old_log10_neutralising_antibodies;
//   }

//   person.time_last_boost = t;
// }





// void disease_model::boostNeutsInfection(Individual &person, double &t) {

//   person.old_log10_neutralising_antibodies =
//       calculateNeuts(person, t);  // Assign the old neuts here.
  
//   const VaccineType &vaccination = person.covid.vaccine_at_exposure;

//   double log10_neuts; 

//   switch (vaccination) {
//     case VaccineType::AZ1:
//       log10_neuts = log10_mean_neut_AZ_dose_1 + log10_mean_additional_neut;
//       break;
//     case VaccineType::AZ2:
//       log10_neuts = log10_mean_neut_AZ_dose_2+ log10_mean_additional_neut;
//       break;
//     case VaccineType::Pfizer1:
//       log10_neuts = log10_mean_neut_Pfizer_dose_1 + log10_mean_additional_neut;
//       break;
//     case VaccineType::Pfizer2:
//       log10_neuts = log10_mean_neut_Pfizer_dose_2 + log10_mean_additional_neut;
//       break;
//     case VaccineType::Moderna1:
//       log10_neuts = log10_mean_neut_Pfizer_dose_1 + log10_mean_additional_neut;
//       break;
//     case VaccineType::Moderna2:
//       log10_neuts = log10_mean_neut_Pfizer_dose_2 + log10_mean_additional_neut;
//       break;
//     case VaccineType::Booster:
//       log10_neuts = log10_mean_neut_Pfizer_dose_3 + log10_mean_additional_neut;
//       break;
//     case VaccineType::Unvaccinated:
//       log10_neuts = log10_mean_neut_infection;
//       break;
//     default:
//       throw std::logic_error(
//           "Unrecognised vaccation in boostNeutsInfection. \n");
//   }
  
//   assignNewNeutValue(log10_neuts, sd_log10_neut_titres, person, t);
// }




// void disease_model::boostNeutsVaccination(Individual &person, double &t,
//                                           VaccineType &vaccine) {
//   person.old_log10_neutralising_antibodies = calculateNeuts(person, t);
//   // We can do fold increase in neuts here depending upon the individuals
//   // previous exposure ( + log10(N) would be an N fold increase)
//   double log10_boost;

//   switch (vaccine) {
//     case VaccineType::AZ1:
//       log10_boost = log10_mean_neut_AZ_dose_1;
//       break;
//     case VaccineType::AZ2:
//       log10_boost = log10_mean_neut_AZ_dose_2;
//       break;
//     case VaccineType::Pfizer1:
//       log10_boost = log10_mean_neut_Pfizer_dose_1;
//       break;
//     case VaccineType::Pfizer2:
//       log10_boost = log10_mean_neut_Pfizer_dose_2;
//       break;
//     case VaccineType::Moderna1:
//       log10_boost = log10_mean_neut_Pfizer_dose_1;
//       break;
//     case VaccineType::Moderna2:
//       log10_boost = log10_mean_neut_Pfizer_dose_2;
//       break;
//     case VaccineType::Booster:
//       log10_boost = log10_mean_neut_Pfizer_dose_3;
//       break;
//     default:
//       throw std::logic_error(
//           "Unrecognised vaccation in boostNeutsVaccination. \n");
//   }
//   assignNewNeutValue(log10_boost, sd_log10_neut_titres, person, t);
// }

    return 0;
}