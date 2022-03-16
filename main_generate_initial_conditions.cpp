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
#include "abm/scenario_read.h"
#include "nlohmann/json.hpp"

void assemble_age_matrix(const std::vector<Individual> &residents,
                         std::vector<std::vector<int>> &age_matrix)
{
    // Assign residents to their age matrix.
    for (int i = 0; i < (int)residents.size(); i++)
    {
        int bracket = residents[i].age_bracket;
        age_matrix[bracket].push_back(i);
    }
}

size_t bin_data(double &x, const std::vector<double> &upper_bounds)
{
    if (x < 0)
        std::cout << x << std::endl;
    if (x > 1)
        std::cout << x << std::endl;

    for (size_t bin = 0; bin < upper_bounds.size(); ++bin)
    {
        if (x < upper_bounds[bin])
        {
            return bin;
        }
    }
    return -1;
}

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

class VaccinationSchedule
{
private:
public:
    VaccinationSchedule(double &t_in, int &person_in, VaccineType &vaccine_in)
        : t(t_in), person(person_in), vaccine(vaccine_in){};
    double t;            /**< Time */
    int person;          /**< Who */
    VaccineType vaccine; /**< Vaccination */
};

int main(int argc, char *argv[])
{
    // Read in parameters.
    if (argc == 1)
    {
        std::cout << "ERROR: Parameter file not loaded!" << std::endl;
        return 1;
    }
    if (argc != 6)
    { // TODO: change this in once I know the number of input parameters needed
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

    // Load simulation parameters.
    std::string sim_params_filename(argv[2]);
    nlohmann::json sim_params_json = load_json(sim_params_filename);

    // Sim number
    int sim_number = 0;
    std::istringstream iss(argv[3]);
    if (iss >> sim_number)
    {
        std::cout << "Sim number " << sim_number << std::endl;
    }
    else
    {
        throw std::logic_error("Sim number failed to convert\n");
    }

    // Vaccination and infection scenario.
    std::string vaccination_infection_scenario_foldername(
        argv[4]);                                             // Reads in scenario name.
    std::string vaccination_infection_scenario_name(argv[5]); // Reads in scenario name.

    // Create output directory

    // Create the folder for outputs of the scenario.
    std::string folder =
        vaccination_infection_scenario_name + (std::string)sim_params_json["folder_suffix"];
    std::string directory =
        (std::string)sim_params_json["output_directory"] + folder;
#ifdef _WIN32
    int top_folder =
        mkdir(((std::string)sim_params_json["output_directory"]).c_str());
    int main_folder = mkdir(directory.c_str()); // Create folder.
#else
    int top_folder =
        mkdir(((std::string)sim_params_json["output_directory"]).c_str(), 0777);
    int main_folder = mkdir(directory.c_str(), 0777); // Create folder.
#endif
    (void)main_folder; // Unused variable;

    // Write json output to file for comparison later comparison.
    std::string output_json_for_save = directory + "_inputs.json";

    std::ofstream json_output(output_json_for_save);
    if (json_output.is_open())
    {
        json_output << sim_params_json << std::endl
                    << neuts_json;
        json_output.close();
    };

    // Load the TTIQ distributions.
    std::ifstream ttiq_read("ttiq_distributions.csv");
    std::vector<double> ttiq_days, partial, optimal;
    if (ttiq_read.is_open())
    {
        std::string line;
        double value;
        std::getline(ttiq_read, line); // Get first line.
        // Do nothing this is a title.
        // Second line onwards.
        while (std::getline(ttiq_read, line))
        {
            std::stringstream stream_line(line);
            std::string row_val;
            // std::vector<double> row;
            for (int col_number = 0; col_number < 3; col_number++)
            {
                std::getline(stream_line, row_val,
                             ','); // Row val is the corresponding double we are after.
                std::stringstream stream_row(row_val);
                stream_row >> value;
                if (col_number == 0)
                {
                    ttiq_days.push_back(value);
                }
                if (col_number == 1)
                {
                    partial.push_back(value);
                }
                if (col_number == 2)
                {
                    optimal.push_back(value);
                }
            }
        }
        ttiq_read.close();
    }
    else
    {
        throw std::logic_error("The ttiq distributions file was not found.");
    }

#ifdef DUMP_INPUT
    std::cout << "TTIQ days, partial, optimal \n";
    for (int i = 0; i < ttiq_days.size(); ++i)
    {
        std::cout << ttiq_days[i] << ", " << partial[i] << ", " << optimal[i]
                  << "\n";
    }
#endif

    // Error check.
    if (ttiq_days.size() != partial.size() ||
        ttiq_days.size() != optimal.size())
    {
        throw std::logic_error("Dimension mismatch in ttiq distributions! \n");
    }

    // vaccination infection scenario should have:
    // age_band, num_people, max_vaccine_number, infection yes/no
    // gives age band, number of people in this particular group, 0, 1 or 2 vaccines--if 2 vaccines, the 1st dose is given at the very beginning, and the 2nd dose is given later (all boosters will be given in the 'main/actual' simulaiton, and whether or not this group gets infected during this 'pre' simulation)

    // Will be used to construct individuals.
    std::vector<std::uniform_real_distribution<double>> generate_age =
        read_age_generation(vaccination_infection_scenario_foldername + "/dim_age_band.csv",
                            100.0);

    // Create residents. 

    std::vector<double> age_brackets = sim_params_json["age_brackets"];

    // generates for each individual, vaccination dates and infection dates according to input values about total number of vaccinations and infections
    std::vector<Individual> residents =
        read_individuals_assignment(vaccination_infection_scenario_foldername + "/" +
                             vaccination_infection_scenario_name + ".csv",
                         generate_age, age_brackets, neuts_json);
    std::cout << "We made " << residents.size() << " Individuals\n";

    // Assign neutralising antibodies to all residents.
    double t = 0.0;
    double t_end = sim_params_json["t_end"];
    double seed_exposure = sim_params_json["seed_exposure"];
    bool catch_exposure = false;
    double vaccination_dt = 7.0;
    double covid_dt = pow(2.0, -2.0);

    // construct mostly empty disease model object and then use its to apply the effect of vaccination and infection and thus modify the neuts:

    // Contact matrix filename.
    std::string contact_matrix_filename = sim_params_json["contact_matrix"];
    size_t num_brackets = age_brackets.size(); // Number of brackets.

    // Contact matrix - read in.
    std::vector<std::vector<double>> contact_matrix(
        num_brackets, std::vector<double>(num_brackets, 0.0));
    std::ifstream matrix_read(contact_matrix_filename);
    if (matrix_read.is_open())
    {
        std::string line;
        double value;
        for (int i = 0; i < num_brackets; i++)
        {
            std::getline(matrix_read, line); // Read the line.
            std::stringstream stream_line(line);
            std::string row_val;
            for (int j = 0; j < num_brackets; j++)
            {
                std::getline(stream_line, row_val,
                             ','); // Row val is the corresponding double we are after.
                std::stringstream stream_row(row_val);
                stream_row >> value;
                contact_matrix[i][j] = value;
            }
        }
        matrix_read.close();
    }
    else
    {
        throw std::logic_error("The contact matrix file " +
                               contact_matrix_filename + " was not found.");
    }

    std::cout << std::endl;

#ifdef DUMP_INPUT
    std::cout << "Contact matrix " << std::endl;
    for (int i = 0; i < contact_matrix.size(); i++)
    {
        for (int j = 0; j < contact_matrix[i].size(); j++)
        {
            std::cout << contact_matrix[i][j] << ", ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
#endif

    // Disease parameters.
    std::vector<double> alpha = sim_params_json["relative_infectiousness"];
    std::vector<double> q = sim_params_json["prob_symptoms"];
    std::vector<double> xi = sim_params_json["susceptibility"];

    // Check the sizes of beta q and xi against eachother and the contact matrix.
    if (alpha.size() != contact_matrix.size())
    {
        throw std::logic_error(
            "Difference in size between beta and contact_matrix. \n");
    }
    if (q.size() != contact_matrix.size())
    {
        throw std::logic_error(
            "Difference in size between q and contact_matrix. \n");
    }
    if (xi.size() != contact_matrix.size())
    {
        throw std::logic_error(
            "Difference in size between xi and contact_matrix. \n");
    }

    // Count residents in each age bracket - set up vaccination?
    std::vector<int> age_bracket_count(num_brackets, 0);
    for (auto &x : residents)
    {
        ++age_bracket_count[x.age_bracket];
    }

    std::vector<double> population_pi(num_brackets, 0.0);
    std::cout << "Population proportion" << std::endl;
    for (int i = 0; i < num_brackets; ++i)
    {
        population_pi[i] =
            static_cast<double>(age_bracket_count[i]) / residents.size();
        std::cout << population_pi[i] << std::endl;
    }
    std::cout << std::endl;

    // Calculate beta from TP.
    double tau_S = 1.0; // Symptomatic.
    double tau_A = 0.5; // Asymptomatic.
    double sum_expression = 0.0;
    for (int k = 0; k < (int)num_brackets; k++)
    {
        double xi_k = xi[k];
        double internal_sum = 0.0;
        for (int i = 0; i < (int)num_brackets; i++)
        {
            double lambda_ik = contact_matrix[i][k];
            internal_sum += alpha[i] * lambda_ik * ((tau_S - tau_A) * q[i] + tau_A) *
                            population_pi[i];
        };
        sum_expression += internal_sum * xi_k;
    };

    double TP = sim_params_json["TP"];

    double beta_scale =
        TP / (sum_expression *
              ((5.1 - 2.5) +
               1.5)); // This is hardcoded, be careful if anything changes.

    std::vector<double> beta = alpha;
    std::cout << "beta " << std::endl;

    for (auto &x : beta)
    {
        // Scale so that it is the appropriate size.
        x = beta_scale * x;
        std::cout << x << std::endl;
    }
    std::cout << std::endl;

    // TTIQ response.
    std::vector<double> b(ttiq_days.begin(), ttiq_days.end());
    std::vector<double> w;
    std::string ttiq_type = sim_params_json["ttiq"];

    if (ttiq_type == "partial")
    {
        w = std::vector<double>(partial.begin(), partial.end());
    }
    else if (ttiq_type == "optimal")
    {
        w = std::vector<double>(optimal.begin(), optimal.end());
    }
    else
    {
        throw std::logic_error(
            "Unrecognised TTIQ_type, please choose either partial or optimal (CASE "
            "SENSITIVE)\n");
    }

    // Calculate TP and load disease model.
    disease_model covid(beta, q, xi, contact_matrix, b, w, neuts_json);

    // initial neuts prior vaccination and infection
    // I can loop per person instead of by time step, because the people don't affect each other.



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

    // and then print out all the neuts values and vaccination history and infection history per person

    std::string output_filename =
        directory + "/sim_number_" + std::to_string(sim_number) + ".csv";
    // Write output to file.
    std::ofstream output_file(output_filename);
    if (output_file.is_open())
    {
        output_file << "age, vaccine, symptomatic, time_symptoms, log10_neuts, "
                       "secondary_infections, time_isolated, infection_number \n";
        output_file << covid; // So sneaky - will put a new line at the end.
        output_file << covid_christmas;
        output_file << covid_restrictions; // Infections from medium covid times.

        output_file.close();
    }

    return 0;
}