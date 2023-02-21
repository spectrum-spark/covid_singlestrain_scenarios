#include <fstream>
#include <iostream>
#include <sstream>
#include <cassert>
#include "abm/abmrandom.h"
#include "abm/vax_infection_scenario_read.h" 

// vaccination infection scenario should have:
// age_band, num_people, max_vaccine_number, time dose 1, time dose 2, time dose 3, infection yes/no, time of infection
// gives age band, number of people in this particular group, 0, 1 or 2 vaccines--if 2 vaccines, the 1st dose is given at the very beginning, and the 2nd dose is given later (all boosters will be given in the 'main/actual' simulaiton, and whether or not this group gets infected during this 'pre' simulation)



// assumption: that all primary doses (1 and 2) are AZ and all booster doses are mRNA (Pfizer)
static void create_individuals_from_input(std::stringstream &individual_group, std::vector<Individual> &residents, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params)
{
    // See what the string looks like. Push it back into the residents.

    // Im not psyched about this function, I havent checked that vaccine_booster is empty and that booster time is empty, its just assumed that it works. It's fine for now, but I wouldnt want anyone to run this function without their own quality checks on the input data like I have done.

    std::string string_value;
    std::stringstream string_value_stream;

    size_t age_band_id;
    size_t num_people; // probably just one
    size_t max_vaccine_number;
    double time_dose_1;
    double time_dose_2;
    double time_booster_1;
    double time_booster_2;
    size_t infection;
    double infection_day;

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


  // Assign values: first dose day
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        time_dose_1 = -1.0; //shouldn't actually be empty though, should have filler values
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_dose_1;
    }

 // Assign values: second dose day
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        time_dose_2 = -1.0; //shouldn't actually be empty though, should have filler values
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_dose_2;
    }

 // Assign values: third (first booster) dose day
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        time_booster_1 = -1.0; //shouldn't actually be empty though, should have filler values
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_booster_1;
    }
 // Assign values: fourth (second booster) dose day
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        time_booster_2 = -1.0; //shouldn't actually be empty though, should have filler values
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> time_booster_2;
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


    // Assign values: infection day
    std::getline(individual_group, string_value, ',');
    if (string_value.empty())
    {
        // What do we do for empty stuff.
        infection_day = -1.0;
    }
    else
    {
        string_value_stream = std::stringstream(string_value);
        string_value_stream >> infection_day;
    }




    // Loop through and create the individuals.
    // Assign people the time of vaccine in a vector for the constructor.

    for (size_t i = 0; i < num_people; ++i)
    {
        // Create an individual!
        double age = generate_age[age_band_id - 1](generator);
        // std::cout << i << ", " << age << std::endl;
        // generate times of vaccination and infection for each person

        std::vector<std::pair<double, VaccineType>> Time_and_Vaccine;
        if (max_vaccine_number > 0)
        {
            // first dose
            VaccineType dose = VaccineType::AZ1;
            // dose = VaccineType::Pfizer1;
            // dose = VaccineType::Moderna1;
            Time_and_Vaccine.push_back(std::make_pair(time_dose_1, dose));
        }
        if (max_vaccine_number>1){
 VaccineType dose2 = VaccineType::AZ2;
            // dose = VaccineType::Pfizer2;
            // dose = VaccineType::Moderna2;
            Time_and_Vaccine.push_back(std::make_pair(time_dose_2, dose2));
        }
        if (max_vaccine_number>2){

            VaccineType dose3 = VaccineType::Booster;
            Time_and_Vaccine.push_back(std::make_pair(time_booster_1, dose3));
        }
        if (max_vaccine_number>3){

            VaccineType dose4 = VaccineType::Booster;
            Time_and_Vaccine.push_back(std::make_pair(time_booster_2, dose4));
        }

        
        residents.push_back(Individual(age, age_brackets, Time_and_Vaccine, ve_params, infection, infection_day));
    }
}

std::vector<Individual> read_individuals_from_input(std::string vaccination_infection_filename, std::vector<std::uniform_real_distribution<double>> &generate_age, std::vector<double> &age_brackets, nlohmann::json &ve_params)
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
            create_individuals_from_input(individuals_stream, residents, generate_age, age_brackets, ve_params); // Create a group at a time.
        }
    }
    else
    {

        throw std::logic_error("The vaccination-infections file " + vaccination_infection_filename + " was not opened (found?).");
    }

    vaccination_infection_read.close(); // Close file.
    return residents;                   // Hopefully a move constructor haha!s
}
