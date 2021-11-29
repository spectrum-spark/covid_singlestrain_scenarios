#include <fstream> 
#include <iostream>
#include <sstream>
#include <vector> 
#include "abm/abmrandom.h"

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
  ageband_read.close();
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

//   for(size_t i = 0; i < generate_age.size(); ++i){
//     for(size_t j = 0; j < 10; ++j){
//       std::cout << generate_age[i](generator) << ", ";
//     }
//     std::cout << std::endl;
//   }

//   return 0; 
// }