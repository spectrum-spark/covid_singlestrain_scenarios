/**
 * @file main_initial-and-main_winterwave.cpp
 * @author your name (you@domain.com)
 * @brief generate initial conditions for the start of the actual 'winter wave', and then run the actual winter wave itself all in one go
 * @version 0.1
 * @date 2022-03-22
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
#include "abm/vax_infection_scenario_read.h"
#include "nlohmann/json.hpp"

#include <chrono>

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
    if (argc != 6)
    { // TODO: change this in once I know the number of input parameters needed
        std::cout << "ERROR did not load enough values" << std::endl;
        return 1;
    }

    // Neut parameters read in here.
    std::string neut_parameters_filename(argv[1]);
    nlohmann::json neuts_json = load_json(neut_parameters_filename);

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
    // age_band, num_people, max_vaccine_number, infection yes/no, dose in third round (number 0, 1, or even 2?)
    // gives age band, number of people in this particular group, 0, 1 or 2 vaccines--if 2 vaccines, the 1st dose is given at the very beginning, and the 2nd dose is given later (all boosters will be given in the 'main/actual' simulation, and whether or not this group gets infected during this 'pre' simulation)

    // Will be used to construct individuals--generating the ages given the age band
    std::vector<std::uniform_real_distribution<double>> generate_age =
        read_age_generation(vaccination_infection_scenario_foldername + "/dim_age_band.csv",
                            100.0);

    // Create residents.

    std::vector<double> age_brackets = sim_params_json["age_brackets"];

    // generates for each individual, vaccination dates and infection dates according to input values about total number of vaccinations and infections
    std::vector<Individual> residents =
        read_individuals_from_input(vaccination_infection_scenario_foldername + "/" +
                                        vaccination_infection_scenario_name + ".csv",
                                    generate_age, age_brackets, neuts_json);
    std::cout << "We made " << residents.size() << " Individuals\n";

    
    

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

    // loop per person instead of by time step, because the people don't affect each other.
    // update neuts according to vaccination dates and infection dates
    // using boostNeutsVaccination for each vaccination
    // and boostNeutsInfection for each infection
    // decay is built into these functions already

    for (int i = 0; i < residents.size(); ++i)
    {
        Individual &person = residents[i];
        Individual::VaccineHistory &vaccinations = residents[i].vaccinations;
        size_t infected_or_not = residents[i].number_infections;
        double time_of_past_infection = residents[i].time_past_infection;

        // need to check if anyone is getting a third dose, to ignore that until the start of the main simulation.

        if (vaccinations.size() == 0)
        {
            // i.e. unvaccinated
            if (infected_or_not)
            { // i.e., unvaccinated and infected
                VaccineType vaccination = VaccineType::Unvaccinated;
                residents[i].covid.vaccine_at_exposure = vaccination;
                covid.boostNeutsInfection(residents[i], time_of_past_infection);
            }
        }
        else if (vaccinations[0].first >= 212)
        { // i.e. first dose only in April/later, meaning that they were unvaxed for the initial phase
            if (infected_or_not)
            { // i.e., unvaccinated and infected
                VaccineType vaccination = VaccineType::Unvaccinated;
                residents[i].covid.vaccine_at_exposure = vaccination;
                covid.boostNeutsInfection(residents[i], time_of_past_infection);
            }
        }
        else
        {
            // vaccinated
            //  first dose
            double time_dose = vaccinations[0].first;
            VaccineType v = vaccinations[0].second;
            // std::cout << vaccinations[0].first << "," << vaccinations[0].second << "\n";
            covid.boostNeutsVaccination_no_switch(residents[i], time_dose, vaccinations[0].second);

            // if they have a first dose, they definitely have a second dose
            double time_dose_2 = vaccinations[1].first;
            VaccineType v2 = vaccinations[1].second;

            // if they also get infected
            if (infected_or_not)
            {
                if (time_of_past_infection < time_dose_2)
                {
                    // unlikely but just in case, then infection needs to happen first before the second dose
                    residents[i].covid.vaccine_at_exposure = v;

                    covid.boostNeutsInfection(residents[i], time_of_past_infection);
                    covid.boostNeutsVaccination_no_switch(residents[i], time_dose_2, v2);
                    residents[i].isVaccinated = true;
                }
                else
                {
                    covid.boostNeutsVaccination_no_switch(residents[i], time_dose_2, v2);
                    residents[i].isVaccinated = true;
                    residents[i].covid.vaccine_at_exposure = v2;
                    covid.boostNeutsInfection(residents[i], time_of_past_infection);
                }
            }
            else // not infected
            {
                covid.boostNeutsVaccination_no_switch(residents[i], time_dose_2, v2);
                residents[i].isVaccinated = true;
            }
        }
    }

    ////////////////////////////////////////////////
    // main simulation to now start!

    // Vaccinate people!
    std::vector<VaccinationSchedule> winter_first_doses;
    std::vector<VaccinationSchedule> winter_second_doses;
    std::vector<VaccinationSchedule> booster_doses;

    // Assign First doses to those getting their first dose 
    for (int i = 0; i < residents.size(); ++i)
    {
        Individual &person = residents[i];
        Individual::VaccineHistory &vaccinations = residents[i].vaccinations;
        if (vaccinations.size() == 0)
        {
            continue;
        }
        else if (vaccinations[0].first >= 212)
        {
            double time_dose = vaccinations[0].first;
            VaccineType v = vaccinations[0].second;
            winter_first_doses.push_back(VaccinationSchedule(vaccinations[0].first, i, vaccinations[0].second));
        }
    }


    // Assign booster doses to those getting their booster dose 
    for (int i = 0; i < residents.size(); ++i)
    {
        Individual &person = residents[i];
        Individual::VaccineHistory &vaccinations = residents[i].vaccinations;
        if (vaccinations.size() == 3)
        {
            double time_dose = vaccinations[2].first;
            VaccineType v = vaccinations[2].second;
            booster_doses.push_back(VaccinationSchedule(vaccinations[2].first, i, vaccinations[2].second));
        }
    }


    double t =212.0;
    double t_end = sim_params_json["t_end"];
    double seed_exposure = sim_params_json["seed_exposure"];
    bool catch_exposure = false;
    //double vaccination_dt = 7.0;
    double vaccination_dt = 1.0;
    double covid_dt = pow(2.0, -2.0);

    
  // Assemble the age_matrix (this is a list of people that are in each age bracket).
  std::vector<std::vector<int>> age_matrix(num_brackets);
  assemble_age_matrix(residents,age_matrix); // Nobody moves from the age matrix so only have to do it once.

    // Create memory that tracks who is exposed, E_ref, and who is infected, I_ref. gen_res is used to sample from the list of residents uniformly.
    std::vector<size_t> E_ref; E_ref.reserve(10000); // Magic number reserving memory.
    std::vector<size_t> I_ref; I_ref.reserve(10000); // Magic number of reserved.


  while(t < t_end) {
    std::cout << "Time is " << t << " and exposed = " << E_ref.size() << " with " << I_ref.size() << " infections \n";
    std::cout << winter_first_doses.size() << " " << winter_second_doses.size() << " " << booster_doses.size() << "\n";
    // Loop  through all first_doses (efficiency is not great oh well)
    auto first_it = std::remove_if(winter_first_doses.begin(), winter_first_doses.end(),[&](auto& x)->bool{
      // Function for first doses. 
      if(x.t<=t) {
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);
        
        Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;

        if(vaccinations.size()>1){
        winter_second_doses.push_back(VaccinationSchedule(vaccinations[1].first, x.person, vaccinations[1].second));
        }
        return true;
      } else {
        return false; 
      }

    });
    winter_first_doses.erase(first_it,winter_first_doses.end());

    // Loop through all second doses (efficiency is not great oh well)
    auto second_it = std::remove_if(winter_second_doses.begin(), winter_second_doses.end(),[&](auto& x)->bool{
      // Function for second doses
      if(x.t <= t) {
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);
        residents[x.person].isVaccinated = true;

        Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;
        // Will they get a booster!
        if(vaccinations.size()>2) {
          booster_doses.push_back(VaccinationSchedule(vaccinations[2].first, x.person, vaccinations[2].second));
        }
        return true; 
      } else {
        return false;
      }
    });
    winter_second_doses.erase(second_it,winter_second_doses.end());

    // Loop through all booster doses (efficiency is not great oh well)
    auto booster_it = std::remove_if(booster_doses.begin(), booster_doses.end(),[&](auto & x)->bool{
      if(x.t <= t) {
        //Booster dose. 
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);

        return true; 
      } else {
        return false;
      }
    });
    booster_doses.erase(booster_it,booster_doses.end());

    if(t >= seed_exposure && !(catch_exposure)) {
      catch_exposure = true; // Assign true so this will not trigger. 
      // Use cluster ref to track the infections phylogenetic tree.
      std::uniform_int_distribution<size_t> gen_res(0,residents.size()-1); 
      int cluster_ref = 0; 
      int initial_infections = 0; // Count initial infections.
      int total_initial_infected = sim_params_json["initial_infections"]; 
      while(initial_infections < total_initial_infected){
        int exposed_resident = gen_res(generator); // Randomly sample from all the population.
        if(residents[exposed_resident].covid.infection_status!='E'){
            covid.seed_exposure(residents[exposed_resident],t); // Random resident has become infected
            residents[exposed_resident].covid.cluster_number = cluster_ref;
            ++initial_infections;
            E_ref.push_back(exposed_resident); // Start tracking them.
        }
      }
    }



    std::vector<size_t> newly_symptomatic; newly_symptomatic.reserve(1000);

    // Simulate the disease model here.
    t = covid.covid_ascm(residents,age_matrix,t,t+vaccination_dt,covid_dt,E_ref,I_ref,newly_symptomatic);
    
  }

    ////////////////////////////////////////////////

    std::string output_filename =
        directory + "/sim_number_" + std::to_string(sim_number) + ".csv";
    // Write output to file.
    std::ofstream output_file(output_filename);
    if (output_file.is_open())
    {
        output_file << "age, vaccine, symptomatic, time_symptoms, log10_neuts, "
                       "secondary_infections, time_isolated, infection_number \n";
        output_file << covid; // So sneaky - will put a new line at the end.

        output_file.close();
    }

    auto end = std::chrono::steady_clock::now();
    std::cout << "Elapsed time in seconds: "
              << std::chrono::duration_cast<std::chrono::seconds>(end - start).count()
              << " sec";

    return 0;
}
