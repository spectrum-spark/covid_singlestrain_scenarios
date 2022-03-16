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

//assumption: that all primary doses (1 and 2) are AZ
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


    // // std::vector<double> Time_doses;
    // std::vector<std::pair<double, VaccineType>> Time_and_Vaccine;
    // std::string time_dose_1_string;
    // std::getline(individual_group, time_dose_1_string, ',');

    // if (!time_dose_1_string.empty())
    // {

    //     // Get the value.
    //     string_value_stream = std::stringstream(time_dose_1_string);
    //     string_value_stream >> time_dose_1;
    //     time_dose_1 = time_dose_1 * (7.0);
    //     VaccineType dose;
    //     if (vaccine == 2)
    //     {
    //         dose = VaccineType::AZ1;
    //     }
    //     else if (vaccine == 1 | vaccine == 5)
    //     {
    //         dose = VaccineType::Pfizer1;
    //     }
    //     else if (vaccine == 3)
    //     {
    //         dose = VaccineType::Moderna1;
    //     }
    //     else
    //     {

    //         throw std::logic_error("Unrecognised vaccine \n");
    //     }
    //     // Time_doses.push_back(time_dose_1);
    //     // Time_and_Vaccine.push_back(std::make_pair(time_dose_1,vaccine));
    //     Time_and_Vaccine.push_back(std::make_pair(time_dose_1, dose));
    // }

    // // Assign values.
    // std::string time_dose_2_string;
    // std::getline(individual_group, time_dose_2_string, ',');
    // if (!time_dose_2_string.empty())
    // {
    //     assert(Time_and_Vaccine.size() == 1); // If you are getting second dose, you have to have had first.
    //     string_value_stream = std::stringstream(time_dose_2_string);
    //     string_value_stream >> time_dose_2;
    //     time_dose_2 = time_dose_2 * (7.0);
    //     VaccineType dose;
    //     if (vaccine == 2)
    //     {
    //         dose = VaccineType::AZ2;
    //     }
    //     else if (vaccine == 1 | vaccine == 5)
    //     {
    //         dose = VaccineType::Pfizer2;
    //     }
    //     else if (vaccine == 3)
    //     {
    //         dose = VaccineType::Moderna2;
    //     }
    //     else
    //     {
    //         throw std::logic_error("Unrecognised vaccine \n");
    //     }
    //     Time_and_Vaccine.push_back(std::make_pair(time_dose_2, dose));
    // }

    // // Assign values.
    // std::string time_booster_string;
    // std::getline(individual_group, time_booster_string, ',');
    // if (!time_booster_string.empty())
    // {
    //     assert(Time_and_Vaccine.size() == 2);
    //     string_value_stream = std::stringstream(time_booster_string);
    //     string_value_stream >> time_booster;
    //     time_booster = time_booster * (7.0);
    //     // Time_doses.push_back(time_booster);
    //     VaccineType dose;
    //     if (booster_vaccine == 1 | booster_vaccine == 2 | booster_vaccine == 3 | booster_vaccine == 4 | booster_vaccine == 5)
    //     {
    //         dose = VaccineType::Booster;
    //     }
    //     else
    //     {
    //         // std::cout << time_booster_string << std::endl;
    //         throw std::logic_error("Unrecognised vaccine \n");
    //     }

    //     Time_and_Vaccine.push_back(std::make_pair(time_booster, dose));
    // }

    
    // Loop through and create the individuals.
    // Assign people the time of vaccine in a vector for the constructor.

    for (size_t i = 0; i < num_people; ++i)
    {
        // Create an individual!
        double age = generate_age[age_band_id - 1](generator);
        // std::cout << i << ", " << age << std::endl;
        // todo: generate times of vaccination and infection for each person
        residents.push_back(Individual(age, age_brackets, Time_and_Vaccine, ve_params));
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
