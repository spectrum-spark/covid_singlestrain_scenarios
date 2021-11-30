#include <fstream> 
#include <iostream>
#include <sstream>
#include "abm/abmrandom.h"
#include "abm/quantium_read.h"

std::vector<std::uniform_real_distribution<double>> read_age_generation(std::string dim_age_filename, double max_age) {
  // std::string dim_age_filename = "booster-uptake-draft-data-model/dim_age_band.csv";
  std::vector<std::uniform_real_distribution<double>> generate_age; 
  std::cout << "Opening age bands from: " + dim_age_filename << std::endl;

  std::ifstream ageband_read(dim_age_filename);
  std::vector<double> lower_age_band;

  if(ageband_read.is_open()){

    std::string line; 
    std::getline(ageband_read,line); // Get the title line.
    
    // Check that the file satisfies what we know. 
    {// Restrict the lifetime of titleline and num columns. 
      std::stringstream titleline(line);
      size_t num_columns = 0; 
      // Split at comma for column names. 
      while(std::getline(titleline,line,',')) { 
        ++num_columns;
        // Check if they match. 
        if(num_columns==1) {
          assert(line.compare("age_band_id")==0);
        } else if(num_columns==2) {
          assert(line.compare("age_band")==0);
        } else {
          throw std::logic_error("Too many columns in " + dim_age_filename);
        }
      }
    } // Finish checking that the file matches the criteria. 

    while(std::getline(ageband_read,line)){
      double lower_bound;

      std::stringstream stream_line(line);
      std::string column; 

      // Split at comma for first column. 
      std::getline(stream_line,column,',');

      // Get second column 
      std::getline(stream_line,column,',');
      std::stringstream ageband_stream(column); // Bounds of age. 

      
      std::getline(ageband_stream,column,'-');
      std::stringstream value_stream(column);
      value_stream >> lower_bound;
      lower_age_band.push_back(lower_bound);
    }
  } else {
    throw std::logic_error("The age band file " + dim_age_filename + " was not opened (found?).");
  }

  ageband_read.close(); // Close file.

  // Max age must be above the max age already known.
  if(max_age <= lower_age_band.back()){
    max_age = lower_age_band.back() + 10.0;
    std::cout << "Max age updated to be " << max_age << std::endl;
  }

  lower_age_band.push_back(max_age); // Add max age. 

  // Create the distributions for each age band. 
  for(size_t i = 0; i < lower_age_band.size()-1;++i){
    generate_age.push_back(std::uniform_real_distribution(lower_age_band[i],lower_age_band[i+1]));
  }

 return generate_age;

}

static void create_individuals(std::stringstream& individual_group, std::vector<Individual>& residents, std::vector<std::uniform_real_distribution<double>>& generate_age){
  // See what the string looks like. Push it back into the residents. 
  std::string string_value; 
  std::stringstream string_value_stream;

  size_t age_band_id; 
  size_t vaccine;
  size_t booster_vaccine;
  double time_dose_1;
  double time_dose_2;
  double time_booster; 
  size_t num_people;

  // Assign values
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> age_band_id;
  } 

  // Assign values vaccine
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> vaccine;
  } 

  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> booster_vaccine;
  } 

  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
    time_dose_1 = std::numeric_limits<double>::max();
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> time_dose_1;
  } 

  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
    time_dose_2 = std::numeric_limits<double>::max();
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> time_dose_2;
  } 
  
  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
    time_booster = std::numeric_limits<double>::max();
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> time_booster;
  } 
  
  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff. 
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> num_people;
  } 

  std::cout << age_band_id <<", "<< vaccine <<", "<< booster_vaccine <<", "<< time_dose_1 <<", "<< time_dose_2 <<", "<< time_booster <<", "<< num_people << std::endl;

  if(age_band_id > generate_age.size()){
    throw std::logic_error("Age band reference is past the length of ages.");
  }
  // Loop through and create the individuals. 
  for(size_t i = 0; i < num_people;++i){
    // Create an individual! 
    std::cout << i << ", " << generate_age[age_band_id-1](generator) << std::endl;
    
  }

}


std::vector<Individual> read_individuals(std::string vaccinations_filename, std::vector<std::uniform_real_distribution<double>>& generate_age) {

  std::vector<Individual> residents; // This will contain all residents. 

  // Open the file, get the line Pass into create_individuals. 
  std::cout << "Opening vaccination schedule from: " + vaccinations_filename << std::endl;

  std::ifstream vaccinations_read(vaccinations_filename);

  if(vaccinations_read.is_open()){

    std::string line; 
    std::getline(vaccinations_read,line); // Get the title line (dont do anything)

    while(std::getline(vaccinations_read,line)){
      // Read until end of file.
      std::stringstream individuals_stream(line);
      create_individuals(individuals_stream, residents, generate_age); // Create a group at a time. 
    }
  
  } else {

    throw std::logic_error("The vaccination file " + vaccinations_filename + " was not opened (found?).");

  }
  vaccinations_read.close(); // Close file.
  return residents; // Hopefully a move constructor haha!s
}