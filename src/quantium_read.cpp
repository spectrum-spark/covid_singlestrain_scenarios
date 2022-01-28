#include <fstream> 
#include <iostream>
#include <sstream>
#include <cassert>
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
    // {// Restrict the lifetime of titleline and num columns. 
    //   std::stringstream titleline(line);
    //   size_t num_columns = 0; 
    //   // Split at comma for column names. 
    //   while(std::getline(titleline,line,',')) { 
    //     ++num_columns;
    //     // Check if they match. 
    //     if(num_columns==1) {
    //       assert(line.compare("age_band_id")==0);
    //     } else if(num_columns==2) {
    //       std::cout << line << std::endl;
    //       assert(line.compare("age_band")==0);
    //     } else {
    //       throw std::logic_error("Too many columns in " + dim_age_filename);
    //     }
    //   }
    // } // Finish checking that the file matches the criteria. 

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

  std::cout << "Lower age bands " << std::endl;
  for(auto x: lower_age_band){
    std::cout << x << ", ";
  }
  std::cout << max_age << std::endl;


  lower_age_band.push_back(max_age); // Add max age. 

  // Create the distributions for each age band. 
  for(size_t i = 0; i < lower_age_band.size()-1;++i){
    generate_age.push_back(std::uniform_real_distribution(lower_age_band[i],lower_age_band[i+1]));
  }

 return generate_age;

}

static void create_individuals(std::stringstream& individual_group, std::vector<Individual>& residents, std::vector<std::uniform_real_distribution<double>>& generate_age, std::vector<double> & age_brackets, nlohmann::json& ve_params){
  // See what the string looks like. Push it back into the residents. 

  //Im not psyched about this function, I havent checked that vaccine_booster is empty and that booster time is empty, its just assumed that it works. It's fine for now, but I wouldnt want anyone to run this function without their own quality checks on the input data like I have done. 
  std::string string_value; 
  std::stringstream string_value_stream;

  size_t age_band_id; 
  size_t vaccine = 0;
  size_t booster_vaccine = 0;
  double time_dose_1;
  double time_dose_2;
  double time_booster; 
  size_t num_people;


      std::cout << individual_group.str() << std::endl;

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

  // std::vector<double> Time_doses;
  std::vector<std::pair<double, VaccineType>> Time_and_Vaccine;
  std::string time_dose_1_string;
  std::getline(individual_group,time_dose_1_string,',');

  if(!time_dose_1_string.empty()) {
 
    // Get the value. 
    string_value_stream = std::stringstream(time_dose_1_string);
    string_value_stream >> time_dose_1;
    time_dose_1 = time_dose_1*(7.0);
    VaccineType dose;
    if(vaccine==2){
      dose = VaccineType::AZ1;
    } else if(vaccine==1 | vaccine==5) {
      dose = VaccineType::Pfizer1;
    } else if(vaccine==3) {
      dose = VaccineType::Moderna1;
    } else {

      throw std::logic_error("Unrecognised vaccine \n");
    }
    // Time_doses.push_back(time_dose_1);
    // Time_and_Vaccine.push_back(std::make_pair(time_dose_1,vaccine));
    Time_and_Vaccine.push_back(std::make_pair(time_dose_1,dose));

  }

  // Assign values. 
  std::string time_dose_2_string;
  std::getline(individual_group,time_dose_2_string,',');
  if(!time_dose_2_string.empty()){
    assert(Time_and_Vaccine.size()==1); // If you are getting second dose, you have to have had first. 
    string_value_stream = std::stringstream(time_dose_2_string);
    string_value_stream >> time_dose_2;
    time_dose_2 = time_dose_2*(7.0);
    VaccineType dose;
    if(vaccine==2){
      dose = VaccineType::AZ2;
    } else if(vaccine==1| vaccine==5) {
      dose = VaccineType::Pfizer2;
    } else if(vaccine==3) {
      dose = VaccineType::Moderna2;
    } else {
      throw std::logic_error("Unrecognised vaccine \n");
    }
    Time_and_Vaccine.push_back(std::make_pair(time_dose_2,dose));
  } 
  
  // Assign values. 
  std::string time_booster_string;
  std::getline(individual_group,time_booster_string,',');
  if(!time_booster_string.empty()){
    assert(Time_and_Vaccine.size()==2);
    string_value_stream = std::stringstream(time_booster_string);
    string_value_stream >> time_booster;
    time_booster = time_booster*(7.0);
    // Time_doses.push_back(time_booster);
    VaccineType dose;
    if(booster_vaccine == 4){
      dose = VaccineType::Booster;
    } else {
      // std::cout << time_booster_string << std::endl; 
      throw std::logic_error("Unrecognised vaccine \n");
    }

    Time_and_Vaccine.push_back(std::make_pair(time_booster,dose));
  } 
  
  // Assign values. 
  std::getline(individual_group,string_value,',');
  if(string_value.empty()){
    // What do we do for empty stuff.
    num_people = 0; 
  } else {
    string_value_stream = std::stringstream(string_value);
    string_value_stream >> num_people;
  } 
  
  if(age_band_id > generate_age.size()){
    throw std::logic_error("Age band reference is past the length of ages.");
  }
  // Loop through and create the individuals. 
  // Assign people the time of vaccine in a vector for the constructor. 
  
  for(size_t i = 0; i < num_people;++i){
    // Create an individual! 
    double age = generate_age[age_band_id-1](generator);
    // std::cout << i << ", " << age << std::endl;
    residents.push_back(Individual(age,age_brackets, Time_and_Vaccine, ve_params));
  }
}


std::vector<Individual> read_individuals(std::string vaccinations_filename, std::vector<std::uniform_real_distribution<double>>& generate_age, std::vector<double>& age_brackets, nlohmann::json& ve_params) {

  std::vector<Individual> residents; // This will contain all residents. 

  // Open the file, get the line Pass into create_individuals. 
  std::cout << "Opening vaccination schedule from: " + vaccinations_filename << std::endl;

  std::ifstream vaccinations_read(vaccinations_filename);

  if(vaccinations_read.is_open()){

    std::string line; 
    std::getline(vaccinations_read,line); // Get the title line (dont do anything)
  // std::cout << line << std::endl;
    while(std::getline(vaccinations_read,line)){
      // Read until end of file.
      // std::cout << line << std::endl;
      std::stringstream individuals_stream(line);
      create_individuals(individuals_stream, residents, generate_age, age_brackets, ve_params); // Create a group at a time. 
    }
  
  } else {

    throw std::logic_error("The vaccination file " + vaccinations_filename + " was not opened (found?).");

  }

  vaccinations_read.close(); // Close file.
  return residents; // Hopefully a move constructor haha!s
}