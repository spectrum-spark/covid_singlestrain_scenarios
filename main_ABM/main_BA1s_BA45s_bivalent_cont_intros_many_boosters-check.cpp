/**
 * @file main_continuous_simulation.cpp
 * @author your name (you@domain.com)
 * @brief fixed TP simulation from beginning to end
 * @version 0.1
 * @date 2022-05-14
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
#include "abm/ibm_simulation_4th_doses.h"
#include "abm/quantium_read.h"
#include "abm/vax_infection_scenario_read_many_boosters.h"
#include <math.h>

#include <chrono>
#include <thread>

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
  auto start = std::chrono::steady_clock::now();

  // Read in parameters.
  if (argc == 1)
  {
    std::cout << "ERROR: Parameter file not loaded!" << std::endl;
    return 1;
  }
  if (argc != 7)
  {
    std::cout << "ERROR did not load enough values" << std::endl;
    return 1;
  }

  // Neut parameters read in here.
  std::string neut_parameters_filename(argv[1]);
  nlohmann::json neuts_json = load_json(neut_parameters_filename);

  std::string new_strain_params_filename(argv[2]);
  nlohmann::json new_strain_neuts_json = load_json(new_strain_params_filename);

  // Load simulation parameters.
  std::string sim_params_filename(argv[3]);
  nlohmann::json sim_params_json = load_json(sim_params_filename);

  // Sim number
  int sim_number = 0;
  std::istringstream iss(argv[4]);
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
      argv[5]);                                             // Reads in scenario name.
  std::string vaccination_infection_scenario_name(argv[6]); // Reads in scenario name.

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
  std::ifstream ttiq_read("no_ttiq_distribution.csv");
  std::vector<double> ttiq_days, no_ttiq;
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
          no_ttiq.push_back(value);
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
  std::cout << "TTIQ days, no ttiq \n";
  for (int i = 0; i < ttiq_days.size(); ++i)
  {
    std::cout << ttiq_days[i] << ", " << no_ttiq[i]
              << "\n";
  }
#endif

  // Error check.
  if (ttiq_days.size() != no_ttiq.size())
  {
    throw std::logic_error("Dimension mismatch in ttiq distributions! \n");
  }

  // Will be used to construct individuals--generating the ages given the age band
  std::vector<std::uniform_real_distribution<double>> generate_age =
      read_age_generation(vaccination_infection_scenario_foldername + "/dim_age_band.csv", 100.0); // from quantium_read.cpp

  // Create residents.

  std::vector<double> age_brackets = sim_params_json["age_brackets"];

  // reads in, for each individual, their vaccination dates and (potential) infection date [unused] according to input values
  std::vector<Individual> residents =
      read_individuals_from_input_many_boosters(vaccination_infection_scenario_foldername + "/" +
                                      vaccination_infection_scenario_name + ".csv",
                                  generate_age, age_brackets, neuts_json);
  std::cout << "We made " << residents.size() << " Individuals\n";

  // TIMING
  double t = 0.0;
  double t_end = sim_params_json["t_end"];

  
  double vaccination_dt = 1.0; // because we have daily vaccinations instead of weekly assignments
  double covid_dt = pow(2.0, -2.0);

  double start_exposure_time = sim_params_json["start_exposure"];
  int regular_exposure_infections = sim_params_json["regular_exposure_infections"];
  double seed_every_x_days = sim_params_json["seed_every_x_days"];
  double latest_exposure_day = 0.0;

  // Bivalent details
  double bivalent_start_time = sim_params_json["bivalent_start_time"];
  double log10_mean_neut_bivalent_booster = neuts_json["log10_mean_neut_bivalent_booster"];


  // New strain details
  // int new_strain_wave_start = sim_params_json["new_strain_wave_start"]; // not needed
  double new_strain_wave_start_day =sim_params_json["new_strain_wave_start_day"];

  double new_strain_ratio = new_strain_neuts_json["R0_ratio"];
  double new_strain_immune_escape = new_strain_neuts_json["log10_omicron_neut_fold"];
  double OG_log10_omicron_neut_fold = neuts_json["log10_omicron_neut_fold"];
  double relative_omicron_log10_immune_escape = new_strain_immune_escape - OG_log10_omicron_neut_fold; // THis is relative omicron escape. In the json it is relative delta escape. It is assumed that it is further away from delta. Not back towards.

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
  std::vector<double> alpha = getJsonValue<std::vector<double>>(
      sim_params_json, "relative_infectiousness");
  std::vector<double> q =
      getJsonValue<std::vector<double>>(sim_params_json, "prob_symptoms");
  std::vector<double> xi =
      getJsonValue<std::vector<double>>(sim_params_json, "susceptibility");

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

  // Count residents in each age bracket for Historical Reasons?
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

  double TP = getJsonValue<double>(sim_params_json, "baseline_TP") * getJsonValue<double>(neuts_json, "R0_ratio");

  double mobility_restrictions =
      getJsonValue<double>(sim_params_json, "mobility_restrictions");

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

  if (ttiq_type == "no_ttiq")
  {
    w = std::vector<double>(no_ttiq.begin(), no_ttiq.end());
  }
  else
  {
    throw std::logic_error(
        "Unrecognised TTIQ_type, must be no_ttiq, try a (CASE "
        "SENSITIVE)\n");
  }

  // Calculate TP and load disease model.
  double start_restrictions =
      getJsonValue<double>(sim_params_json, "start_restrictions");
  double finish_restrictions =
      getJsonValue<double>(sim_params_json, "finish_restrictions");
  auto mobility_function = [=](double &t)
  {
    if (t < start_restrictions || t > finish_restrictions)
    {
      return 1.0;
    }
    else
    {
      return mobility_restrictions;
    }
  };

  disease_model covid(beta, q, xi, contact_matrix, b, w, neuts_json, mobility_function);
  covid.set_bivalent_booster(log10_mean_neut_bivalent_booster);

  //     double BA2_time = sim_params_json["BA2_time"];
  //   double BA2_ratio =sim_params_json["BA2_ratio"];

  //   for (auto& x : beta) {
  //     x = BA2_ratio * x;
  //   }

  // New strain emergence.
  // in Eamon's version, the BA2 code was run (aka uncommented) and so the ratio was relative to BA2; for us, different? aka more hypothetical? (though that was transmissibility, more so than immune escape?)
  for (auto &x : beta)
  {
    x = new_strain_ratio * x;
  }

  disease_model new_covid(beta, q, xi, contact_matrix, b, w, new_strain_neuts_json,
                          mobility_function, neuts_json["log10_omicron_neut_fold"]);
  new_covid.set_bivalent_booster(log10_mean_neut_bivalent_booster);

  // Vaccinate people!
  std::vector<VaccinationSchedule> first_doses;
  std::vector<VaccinationSchedule> second_doses;
  std::vector<VaccinationSchedule> booster_doses;
  std::vector<VaccinationSchedule> second_booster_doses;
  std::vector<VaccinationSchedule> third_booster_doses;
  std::vector<VaccinationSchedule> fourth_booster_doses;

  // Assign First doses.
  for (int i = 0; i < residents.size(); ++i)
  {
    Individual &person = residents[i];
    Individual::VaccineHistory &vaccinations = residents[i].vaccinations;
    if (vaccinations.size() == 0)
    {
      continue;
    }
    else
    {
      double time_dose = vaccinations[0].first;
      VaccineType v = vaccinations[0].second;
      first_doses.push_back(VaccinationSchedule(vaccinations[0].first, i,
                                                vaccinations[0].second));
    }
  }

  // Assemble the age_matrix (this is a list of people that are in each age
  // bracket).
  std::vector<std::vector<int>> age_matrix(num_brackets);
  assemble_age_matrix(residents,
                      age_matrix); // Nobody moves from the age matrix so only
                                   // have to do it once.

  // Create memory that tracks who is exposed, E_ref, and who is infected,
  // I_ref. gen_res is used to sample from the list of residents uniformly.
  std::vector<size_t> E_ref;
  E_ref.reserve(10000); // Magic number reserving memory.
  std::vector<size_t> I_ref;
  I_ref.reserve(10000); // Magic number of reserved.






  

  // BA1 WAVE(S) /////////////////////////////////////////

  while (t < new_strain_wave_start_day)
  {
    std::cout << "Time is " << t << " and exposed = " << E_ref.size()
              << " with " << I_ref.size() << " infections \n";

    std::cout << first_doses.size() << " " << second_doses.size() << " "
              << booster_doses.size() << " " << second_booster_doses.size()
              << "\n";

    // Loop  through all first_doses (efficiency is not great oh well)
    auto first_it = std::remove_if(
        first_doses.begin(), first_doses.end(), [&](auto &x) -> bool
        {
          // Function for first doses.
          if (x.t <= t) {
            covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);

            Individual::VaccineHistory& vaccinations =
                residents[x.person].vaccinations;

            if (vaccinations.size() > 1) {
              second_doses.push_back(VaccinationSchedule(
                  vaccinations[1].first, x.person, vaccinations[1].second));
            }
            return true;
          } else {
            return false;
          } });
    first_doses.erase(first_it, first_doses.end());

    // Loop through all second doses (efficiency is not great oh well)
    auto second_it = std::remove_if(
        second_doses.begin(), second_doses.end(), [&](auto &x) -> bool
        {
          // Function for second doses
          if (x.t <= t) {
            covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            residents[x.person].isVaccinated = true;

            Individual::VaccineHistory& vaccinations =
                residents[x.person].vaccinations;
            // Will they get a booster!
            if (vaccinations.size() > 2) {
              booster_doses.push_back(VaccinationSchedule(
                  vaccinations[2].first, x.person, vaccinations[2].second));
            }
            return true;
          } else {
            return false;
          } });
    second_doses.erase(second_it, second_doses.end());

    // Loop through all booster doses (efficiency is not great oh well)
    auto booster_it = std::remove_if(
        booster_doses.begin(), booster_doses.end(), [&](auto &x) -> bool
        {
          if (x.t <= t) {
            // Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
            // Will they get a booster!
            if (vaccinations.size() > 3) {
              second_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[3].first, x.person, vaccinations[3].second));
            }

            return true;
          } else {
            return false;
          } });
    booster_doses.erase(booster_it, booster_doses.end());

    // Loop through all second booster doses (efficiency is not great oh well)
    auto second_booster_it = std::remove_if(
        second_booster_doses.begin(), second_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // Second Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
            // Will they get another booster!
            if (vaccinations.size() > 4) {
              third_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[4].first, x.person, vaccinations[4].second));
            }

            return true;
          }
          else
          {
            return false;
          }
        });
    second_booster_doses.erase(second_booster_it, second_booster_doses.end());

    // Loop through all third booster doses (efficiency is not great oh well)
    auto third_booster_it = std::remove_if(
        third_booster_doses.begin(), third_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // third Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
            // Will they get another booster again!
            if (vaccinations.size() > 5) {
              fourth_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[5].first, x.person, vaccinations[5].second));
            }

            return true;
          }
          else
          {
            return false;
          }
        });
    third_booster_doses.erase(third_booster_it,third_booster_doses.end());

    // Loop through all fourth booster doses (efficiency is not great oh well)
    auto fourth_booster_it = std::remove_if(
        fourth_booster_doses.begin(), fourth_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // fourth Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }


            return true;
          }
          else
          {
            return false;
          }
        });
    fourth_booster_doses.erase(fourth_booster_it,fourth_booster_doses.end());


    double t_old = t;
    double t_vaccine = t_old + vaccination_dt;
    while (t < t_vaccine)
    {
      double daily_dt = 1.0;
      if (t + daily_dt > t_vaccine)
      {
        daily_dt = t_vaccine - t;
      }
      
      if (t >= start_exposure_time && t>=latest_exposure_day+seed_every_x_days)
      {
        // Use cluster ref to track the infections phylogenetic tree.
        std::uniform_int_distribution<size_t> gen_res(0, residents.size() - 1);
        int initial_infections = 0; // Count initial infections.
        while (initial_infections < regular_exposure_infections)
        {
          int exposed_resident =
              gen_res(generator); // Randomly sample from all the population.
          if (residents[exposed_resident].covid.infection_status != 'E' && residents[exposed_resident].covid.infection_status != 'I')
          {
            covid.seed_exposure(residents[exposed_resident],
                                t); // Random resident has become exposed
            residents[exposed_resident].covid.cluster_number = 0;
            ++initial_infections;
            E_ref.push_back(exposed_resident); // Start tracking them.
          }
        }

        latest_exposure_day = t;

      }

      std::vector<size_t> newly_symptomatic;
      newly_symptomatic.reserve(1000);

      // Simulate the disease model here.
      t = covid.covid_ascm(residents, age_matrix, t, t + daily_dt, covid_dt, E_ref, I_ref, newly_symptomatic);
    }
  }



  // BA4/5 WAVE(S) ////////////////////////////////////////////////////////////////////////////

// What happens if there is a new strain that appears?
  // If new strain has appeared than we want to use that strain. What happens.
  // We can have increased, beta... We can go through all of
  // the neuts of the individuals? So much needs to happen. So lets just do it
  // here.

  // We are throwing out all exposed and infected individuals as we cant handle
  // multiple strains.
  auto all_it =
      std::remove_if(E_ref.begin(), E_ref.end(), [&](auto &id) -> bool
                     {
        // Recover the individuals
        covid.recover_individual(residents[id]);
        return true; });
  E_ref.erase(all_it, E_ref.end());

  all_it = std::remove_if(I_ref.begin(), I_ref.end(), [&](auto &id) -> bool
                          {
    // Recover the individuals
    covid.recover_individual(residents[id]);
    return true; });
  I_ref.erase(all_it, I_ref.end());

  // Throw an assert here to ensure that noone was left behind.
  assert(E_ref.size() == 0 && I_ref.size() == 0);

  // Neuts have switched from being omicron neuts to not omicron neuts!
  for (auto &person : residents)
  {
    // Reduce their immunity by the factor passed in.
    person.log10_neutralising_antibodies += relative_omicron_log10_immune_escape;
    // Determine if this needs to be changed, ie what if they're at
    // std::numeric_limits<double>::lowest()
    if (!person.isCovidNaive)
    {
      // This person has had omicron, we need to store this so that we can use
      // it in the disease model. Its gross. HACK.
      person.isCovidNaive = true;
      person.priorStrain = true; // Yes they have had the prior strain.
    }
    // They are not familiar with the new strain of covid.
  }

  while (t < t_end)
  {
    // New strain nonsense.
    std::cout << "Time is " << t << " and exposed = " << E_ref.size()
              << " with " << I_ref.size() << " infections \n";

    std::cout << first_doses.size() << " " << second_doses.size() << " "
              << booster_doses.size() << " " << second_booster_doses.size()
              << "\n";

    // Loop  through all first_doses (efficiency is not great oh well)
    auto first_it = std::remove_if(
        first_doses.begin(), first_doses.end(), [&](auto &x) -> bool
        {
          // Function for first doses.
          if (x.t <= t) {
            new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);

            Individual::VaccineHistory& vaccinations =
                residents[x.person].vaccinations;

            if (vaccinations.size() > 1) {
              second_doses.push_back(VaccinationSchedule(
                  vaccinations[1].first, x.person, vaccinations[1].second));
            }
            return true;
          } else {
            return false;
          } });
    first_doses.erase(first_it, first_doses.end());

    // Loop through all second doses (efficiency is not great oh well)
    auto second_it = std::remove_if(
        second_doses.begin(), second_doses.end(), [&](auto &x) -> bool
        {
          // Function for second doses
          if (x.t <= t) {
            new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            residents[x.person].isVaccinated = true;

            Individual::VaccineHistory& vaccinations =
                residents[x.person].vaccinations;
            // Will they get a booster!
            if (vaccinations.size() > 2) {
              booster_doses.push_back(VaccinationSchedule(
                  vaccinations[2].first, x.person, vaccinations[2].second));
            }
            return true;
          } else {
            return false;
          } });
    second_doses.erase(second_it, second_doses.end());

    // Loop through all booster doses (efficiency is not great oh well)
    auto booster_it = std::remove_if(
        booster_doses.begin(), booster_doses.end(), [&](auto &x) -> bool
        {
          if (x.t <= t) {
            // Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                new_covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations =
                residents[x.person].vaccinations;
            // Will they get a booster!
            if (vaccinations.size() > 3) {
              second_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[3].first, x.person, vaccinations[3].second));
            }

            return true;
          } else {
            return false;
          } });
    booster_doses.erase(booster_it, booster_doses.end());

    // Loop through all second booster doses (efficiency is not great oh well)
    auto second_booster_it = std::remove_if(
        second_booster_doses.begin(), second_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // Second Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                new_covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
            // Will they get another booster!
            if (vaccinations.size() > 4) {
              third_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[4].first, x.person, vaccinations[4].second));
            }

            return true;
          }
          else
          {
            return false;
          }
        });
    second_booster_doses.erase(second_booster_it, second_booster_doses.end());

    // Loop through all third booster doses (efficiency is not great oh well)
    auto third_booster_it = std::remove_if(
        third_booster_doses.begin(), third_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // third Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                new_covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
            // Will they get another booster again!
            if (vaccinations.size() > 5) {
              fourth_booster_doses.push_back(VaccinationSchedule(
                  vaccinations[5].first, x.person, vaccinations[5].second));
            }

            return true;
          }
          else
          {
            return false;
          }
        });
    third_booster_doses.erase(third_booster_it,third_booster_doses.end());

    // Loop through all fourth booster doses (efficiency is not great oh well)
    auto fourth_booster_it = std::remove_if(
        fourth_booster_doses.begin(), fourth_booster_doses.end(),
        [&](auto &x) -> bool
        {
          if (x.t <= t)
          {
            // fourth Booster dose.
            if (t>= bivalent_start_time){
                VaccineType bivalent = VaccineType::BivalentBooster;
                new_covid.boostNeutsVaccination(residents[x.person], t, bivalent);
            }
            else{
                new_covid.boostNeutsVaccination(residents[x.person], t, x.vaccine);
            }

            return true;
          }
          else
          {
            return false;
          }
        });
    fourth_booster_doses.erase(fourth_booster_it,fourth_booster_doses.end());

    double t_old = t;
    double t_vaccine = t_old + vaccination_dt;
    while (t < t_vaccine)
    {
      double daily_dt = 1.0;
      if (t + daily_dt > t_vaccine)
      {
        daily_dt = t_vaccine - t;
      }

      if (t >= new_strain_wave_start_day && t>=latest_exposure_day+seed_every_x_days)
      {
        // Use cluster ref to track the infections phylogenetic tree.
        std::uniform_int_distribution<size_t> gen_res(0, residents.size() - 1);
        int initial_infections = 0; // Count initial infections.
        while (initial_infections < regular_exposure_infections)
        {
          int exposed_resident =
              gen_res(generator); // Randomly sample from all the population.
          if (residents[exposed_resident].covid.infection_status != 'E' && residents[exposed_resident].covid.infection_status != 'I')
          {
            covid.seed_exposure(residents[exposed_resident],
                                t); // Random resident has become exposed
            residents[exposed_resident].covid.cluster_number = 1;
            ++initial_infections;
            E_ref.push_back(exposed_resident); // Start tracking them.
          }
        }
        latest_exposure_day = t;
      }



      std::vector<size_t> newly_symptomatic;
      newly_symptomatic.reserve(1000);

      // Simulate the disease model here.

      t = new_covid.covid_ascm(residents, age_matrix, t, t + vaccination_dt,
                               covid_dt, E_ref, I_ref, newly_symptomatic);
    }
  }


  // simulations done, now output!

  auto end = std::chrono::steady_clock::now();
  std::cout << "Elapsed time in seconds: "
            << std::chrono::duration_cast<std::chrono::seconds>(end - start).count()
            << " sec" << std::endl;

  std::string output_filename = directory + "/sim_number_" + std::to_string(sim_number) + ".csv";
  // Write output to file.
  std::ofstream output_file(output_filename);

  if (output_file.is_open())
  {
    output_file << "age, vaccine, symptomatic, time_symptoms, log10_neuts, secondary_infections, time_isolated, infection_number, cluster \n";

    output_file << covid;
    output_file << new_covid;

    output_file.close();
  }
  else
  {
    std::cout << "Unable to open output file for some reason????";
  }

  // // Writing each individual's data out to file
  // std::string individuals_output_filename = directory + "/sim_number_" + std::to_string(sim_number) + "_individuals.csv";
  // std::ofstream individuals_output_file(individuals_output_filename);

  // if (individuals_output_file.is_open())
  // {
  //   individuals_output_file << "age, age bracket, dose times, infection times, symptom onset times \n";

  //   for (int i = 0; i < residents.size(); ++i)
  //   {
  //     Individual &person = residents[i];
  //     Individual::VaccineHistory &vaccinations = person.vaccinations;

  //     individuals_output_file << person.age << ", " << person.age_bracket << ",";
  //     for (int v = 0; v < vaccinations.size(); ++v)
  //     {
  //       if (v > 0)
  //       {
  //         individuals_output_file << ";"; // using ; to be different from the csv comma
  //       }
  //       individuals_output_file << vaccinations[v].first;
  //     }

  //     individuals_output_file << ",";

  //     for (int inft = 0; inft < person.infection_dates.size(); ++inft)
  //     {
  //       if (inft > 0)
  //       {
  //         individuals_output_file << ";";
  //       }
  //       individuals_output_file << person.infection_dates[inft];
  //     }

  //     individuals_output_file << ",";

  //     for (int inft = 0; inft < person.symptom_onset_dates.size(); ++inft)
  //     {
  //       if (inft > 0)
  //       {
  //         individuals_output_file << ";";
  //       }
  //       individuals_output_file << person.symptom_onset_dates[inft];
  //     }

  //     individuals_output_file << "\n";
  //   }

  //   individuals_output_file.close();
  // }
  // else
  // {
  //   std::cout << "Unable to open the individuals' output file for some reason????";
  // }

  return 0;
}
