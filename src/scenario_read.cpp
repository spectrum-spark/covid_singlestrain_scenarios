#include <fstream>
#include <iostream>
#include <sstream>
#include <cassert>
#include "abm/abmrandom.h"
#include "abm/scenario_read.h" //TODO: write the .h file for this
// and then link it in the main_generate_initial_conditions file

// vaccination infection scenario should have:
// age_band, num_people, max_vaccine_number, infection yes/no
// gives age band, number of people in this particular group, 0, 1 or 2 vaccines--if 2 vaccines, the 1st dose is given at the very beginning, and the 2nd dose is given later (all boosters will be given in the 'main/actual' simulaiton, and whether or not this group gets infected during this 'pre' simulation)

// assumption: that all primary doses (1 and 2) are AZ
static void create_individuals_assigned(std::stringstream &individual_group, std::vector<Individual> &residents, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params)
{
    // See what the string looks like. Push it back into the residents.

    // Im not psyched about this function, I havent checked that vaccine_booster is empty and that booster time is empty, its just assumed that it works. It's fine for now, but I wouldnt want anyone to run this function without their own quality checks on the input data like I have done.
    std::string string_value;
    std::stringstream string_value_stream;

    size_t age_band_id;
    size_t num_people;
    size_t max_vaccine_number;
    size_t infection;

    // size_t vaccine = 0;
    // size_t booster_vaccine = 0;
    // double time_dose_1;
    // double time_dose_2;
    // double time_booster;

    // Assign values: age band
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> age_band_id;
    }

    if (age_band_id > generate_age.size())
    {
        throw std::logic_error("Age band reference is past the length of ages.");
    }

    // Assign values: number of people
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        num_people = 0;
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> num_people;
    }

    // Assign values: max vaccine number
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        max_vaccine_number = 0;
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> max_vaccine_number;
    }

    // Assign values: infection
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        infection = 0;
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> infection;
    }

    // Loop through and create the individuals.
    // Assign people the time of vaccine in a vector for the constructor.

    double mean = (181.0 + 122.0) / 2.0;
    double norm_sd = (181.0 - 122.0) / 4.0;
    std::normal_distribution<double> distribution(mean, norm_sd);

    for (size_t i = 0; i < num_people; ++i)
    {
        // Create an individual!
        double age = generate_age[age_band_id - 1](generator);
        // std::cout << i << ", " << age << std::endl;
        // generate times of vaccination and infection for each person

        std::vector<std::pair<double, VaccineType>> Time_and_Vaccine;
        if (max_vaccine_number > 0)
        {
            // first dose assigned on the first day, effectively
            double time_dose_1 = 0.0;
            VaccineType dose = VaccineType::AZ1;
            // dose = VaccineType::Pfizer1;
            // dose = VaccineType::Moderna1;
            Time_and_Vaccine.push_back(std::make_pair(time_dose_1, dose));

            VaccineType dose2 = VaccineType::AZ2;
            // dose = VaccineType::Pfizer2;
            // dose = VaccineType::Moderna2;
            double time_dose = -(90.0 / 101.0) * age + 90.0;
            // basic function to assign time is:
            // t = -(90/101)*age + 90 , so that older people get their 2nd doses first.
            // and people aged 0 get their 2nd doses at ~3 months

            Time_and_Vaccine.push_back(std::make_pair(time_dose, dose2));
        }

        // if this person got infected
        double time_infected;
        if (infection > 0)
        {
            time_infected = distribution(generator);
            // std::cout << "time infected: " << time_infected  << std::endl;
        }
        else
        {
            time_infected = -1.0; // aka never
        }

        residents.push_back(Individual(age, age_brackets, Time_and_Vaccine, ve_params, infection, time_infected));
    }
}

std::vector<Individual> read_individuals_assignment(std::string vaccination_infection_filename, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params)
{

    std::vector<Individual> residents; // This will contain all residents.

    // Open the file, get the line Pass into create_individuals.
    std::cout << "Opening vaccination-infection schedule from: " + vaccination_infection_filename << std::endl;

    std::ifstream vaccination_infection_read(vaccination_infection_filename);

    if (vaccination_infection_read.is_open())
    {

        std::string line;
        std::getline(vaccination_infection_read, line); // Get the title line (dont do anything)
                                                        // std::cout << line << std::endl;
        while (std::getline(vaccination_infection_read, line))
        {
            // Read until end of file.
            // std::cout << line << std::endl;
            std::stringstream individuals_stream(line);
            create_individuals_assigned(individuals_stream, residents, generate_age, age_brackets, ve_params); // Create a group at a time.
        }
    }
    else
    {

        throw std::logic_error("The vaccination-infections file " + vaccination_infection_filename + " was not opened (found?).");
    }

    vaccination_infection_read.close(); // Close file.
    return residents;                   // Hopefully a move constructor haha!s
}

// assumption: that all primary doses (1 and 2) are AZ
static void create_individuals_given_data(std::stringstream &individual_group, std::vector<Individual> &residents, std::vector<double> &age_brackets, nlohmann::json &ve_params)
{
    // See what the string looks like. Push it back into the residents.

    // Im not psyched about this function, I havent checked that vaccine_booster is empty and that booster time is empty, its just assumed that it works. It's fine for now, but I wouldnt want anyone to run this function without their own quality checks on the input data like I have done.
    std::string string_value;
    std::stringstream string_value_stream;

    double age;
    size_t age_band_id;
    double log10_neuts;
    size_t max_vaccine_number;
    double time_if_vaccinated; // the last time vaccination occured
    size_t infection;
    double time_if_infected;

    // Assign values: age
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> age;
    }

    // Assign values: age band
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> age_band_id;
    }

    // Assign values: log10_neuts
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> log10_neuts;
    }

    // Assign values: max vaccine number
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> max_vaccine_number;
    }

    // Assign values: time_if_vaccinated
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_if_vaccinated;
    }

    // Assign values: infection
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        infection = 0;
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> infection;
    }

    // Assign values: time_if_infected
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_if_infected;
    }

    // Loop through and create the individuals, populating their data

   

    std::vector<std::pair<double, VaccineType>> Time_and_Vaccine;
    if (max_vaccine_number > 0)
    {
        // first dose assigned on the first day, effectively
        double time_dose_1 = 0.0;
        VaccineType dose = VaccineType::AZ1;
        // dose = VaccineType::Pfizer1;
        // dose = VaccineType::Moderna1;
        Time_and_Vaccine.push_back(std::make_pair(time_dose_1, dose));

        VaccineType dose2 = VaccineType::AZ2;
        // dose = VaccineType::Pfizer2;
        // dose = VaccineType::Moderna2;
        double time_dose = time_if_vaccinated;
        // basic function to assign time is:
        // t = -(90/101)*age + 90 , so that older people get their 2nd doses first.
        // and people aged 0 get their 2nd doses at ~3 months

        Time_and_Vaccine.push_back(std::make_pair(time_dose, dose2));
    }

    // if this person got infected
    double time_infected;
    if (infection > 0)
    {
        time_infected = time_if_infected;
        // std::cout << "time infected: " << time_infected  << std::endl;
    }
    else
    {
        time_infected = -1.0; // aka never
    }

    bool isvaxxed = false;
    if (max_vaccine_number>0){
        isvaxxed = true;
    }

    bool nocovid = true;
    if(infection>0){
        nocovid = false;
    }



    residents.push_back(Individual(age, age_brackets, Time_and_Vaccine, ve_params, infection, time_infected,log10_neuts,nocovid,isvaxxed));
}

std::vector<Individual> read_individuals_data(std::string neuts_vaccination_infection_filename, std::vector<double> &age_brackets, nlohmann::json &ve_params)
{

    std::vector<Individual> residents; // This will contain all residents.

    // Open the file, get the line Pass into create_individuals.
    std::cout << "Opening vaccination-infection schedule from: " + neuts_vaccination_infection_filename << std::endl;

    std::ifstream neuts_vaccination_infection_read(neuts_vaccination_infection_filename);

    if (neuts_vaccination_infection_read.is_open())
    {

        // age,age_bracket,log10_neuts,max_vaccine, time_if_vaccinated,infected,time_if_infected
        std::string line;
        std::getline(neuts_vaccination_infection_read, line); // Get the title line (dont do anything)
                                                              // std::cout << line << std::endl;
        while (std::getline(neuts_vaccination_infection_read, line))
        {
            // Read until end of file.
            // std::cout << line << std::endl;
            std::stringstream individuals_stream(line);
            create_individuals_given_data(individuals_stream, residents, age_brackets, ve_params); // Create a group at a time.
        }
    }
    else
    {

        throw std::logic_error("The vaccination-infections file " + neuts_vaccination_infection_filename + " was not opened (found?).");
    }

    neuts_vaccination_infection_read.close(); // Close file.
    return residents;                         // Hopefully a move constructor haha!s
}
