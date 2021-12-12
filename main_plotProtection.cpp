#include <iostream>
#include <sstream>
#include <fstream>
#include <sys/stat.h>
#include <sys/types.h>
#include "abm/quantium_read.h"
#include "abm/abmrandom.h"
#include "abm/ibm_simulation.h"
#include "nlohmann/json.hpp"

nlohmann::json load_json(std::string filename) {
  std::ifstream json_stream(filename);
  if(!json_stream.is_open()){
    throw std::logic_error("Json is not found. \n FILENAME : " + filename + "\n");
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

class VaccinationSchedule {
  private:
  public:
  VaccinationSchedule(double& t_in,int& person_in,VaccineType & vaccine_in):t(t_in), person(person_in),vaccine(vaccine_in) {};
  double t; /**< Time */
  int person; /**< Who */
  VaccineType vaccine; /**< Vaccination */

};

int main(int argc, char *argv[]){
  // Read in parameters. 
  if(argc == 1){
    std::cout << "ERROR: Parameter file not loaded!" << std::endl;
    return 1;
  }
  if(argc!=6){
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
  int sim_number=0;
  std::istringstream iss(argv[3]);
  if(iss >> sim_number)
  {
      std::cout << "Sim number " << sim_number << std::endl;
  }else{
      throw std::logic_error("Sim number failed to convert\n");
  }

  // Vaccination scenario. 
  std::string vaccination_scenario_foldername(argv[4]); // Reads in scenario name.
  std::string vaccination_scenario_name(argv[5]); // Reads in scenario name.

  // Create output directory 

  // Create the folder for outputs of the scenario. 
  std::string folder = vaccination_scenario_name + (std::string) sim_params_json["folder_suffix"];
  std::string directory = (std::string) sim_params_json["output_directory"] + folder;
  #ifdef _WIN32
        int top_folder = mkdir(((std::string) sim_params_json["output_directory"]).c_str());
        int main_folder = mkdir(directory.c_str()); // Create folder.
    #else
        int top_folder = mkdir(((std::string) sim_params_json["output_directory"]).c_str(), 0777);
        int main_folder = mkdir(directory.c_str(),0777); // Create folder.
    #endif
    (void) main_folder; // Unused variable;

  // Write json output to file for comparison later comparison. 
  // std::string output_json_for_save = directory  + "/secondary_infections" + file_suffix + "_input.json";

  // std::ofstream json_output(output_json_for_save);
  // if(json_output.is_open()){
  //     json_output << parameters_json;
  //     json_output.close();
  // };

  // Will be used to construct individuals. 
  std::vector<std::uniform_real_distribution<double>> generate_age = read_age_generation(vaccination_scenario_foldername + "/dim_age_band.csv",100.0);

  // Create residents.  
  std::vector<double> age_brackets = sim_params_json["age_brackets"];
  std::vector<Individual> residents = read_individuals(vaccination_scenario_foldername + "/" + vaccination_scenario_name + ".csv",generate_age, age_brackets);
  std::cout << "We made " << residents.size() << " Individuals\n";
  

  // Assign neutralising antibodies to all residents. 
  double t = 0.0;
  double t_end = sim_params_json["t_end"];
  double dt = 7.0;

  // Contact matrix filename. 
  std::string contact_matrix_filename = sim_params_json["contact_matrix"];
  size_t num_brackets = age_brackets.size(); // Number of brackets. 

  // Contact matrix - read in. 
  std::vector<std::vector<double>> contact_matrix(num_brackets,std::vector<double>(num_brackets,0.0));
  std::ifstream matrix_read(contact_matrix_filename);
  if(matrix_read.is_open()){
    std::string line;
    double value;
    for(int i = 0; i < num_brackets; i++){
      std::getline(matrix_read,line); // Read the line. 
      std::stringstream stream_line(line);
      std::string row_val;
      for(int j = 0; j < num_brackets; j++){
        std::getline(stream_line,row_val,','); // Row val is the corresponding double we are after. 
        std::stringstream stream_row(row_val);
        stream_row >> value;
        contact_matrix[i][j] = value; 
      }
    }
    matrix_read.close();
  } else {
    throw std::logic_error("The contact matrix file " + contact_matrix_filename + " was not found.");
  }

  std::cout << std::endl;

#ifdef DUMP_INPUT
  std::cout << "Contact matrix " << std::endl;
  for(int i = 0; i < contact_matrix.size(); i++){
    for(int j = 0;j < contact_matrix[i].size(); j++){
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
  if(alpha.size()!=contact_matrix.size()) {
    throw std::logic_error("Difference in size between beta and contact_matrix. \n");
  }
  if(q.size()!=contact_matrix.size()) {
    throw std::logic_error("Difference in size between q and contact_matrix. \n");
  }
  if(xi.size()!=contact_matrix.size()) {
    throw std::logic_error("Difference in size between xi and contact_matrix. \n");
  }

  // Count residents in each age bracket - set up vaccination?
  std::vector<int> age_bracket_count(num_brackets,0);
  for(auto &x : residents){
    ++age_bracket_count[x.age_bracket];
  }

  std::vector<double> population_pi(num_brackets,0.0);
  std::cout << "Population proportion" << std::endl;
  for(int i = 0; i < num_brackets; ++i) {
    population_pi[i] = static_cast<double>(age_bracket_count[i])/residents.size();
    std::cout << population_pi[i] << std::endl;
  }
  std::cout << std::endl;

  // Calculate beta from TP.
  double tau_S = 1.0; // Symptomatic. 
  double tau_A = 0.5; // Asymptomatic.
  double sum_expression = 0.0;
  for(int k = 0; k < (int) num_brackets;k++){
    double xi_k = xi[k];
    double internal_sum = 0.0;
    for(int i = 0; i < (int) num_brackets; i++){
        double lambda_ik = contact_matrix[i][k];
        internal_sum += alpha[i]*lambda_ik*((tau_S - tau_A)*q[i] + tau_A)*population_pi[i];
    };
    sum_expression += internal_sum*xi_k;
  };

  // This is fun. 
  double TP = sim_params_json["TP"];
  double beta_scale = TP/(sum_expression*((5.1-2.5) + 1.5)); // This is hardcoded, be careful if anything changes. 
  std::vector<double> beta = alpha;
  std::cout << "beta " << std::endl;
  for(auto& x:beta){ // Scale so that it is the appropriate size. 
    x = beta_scale*x;
    std::cout << x << std::endl;
  }
  std::cout << std::endl;

  // TTIQ response. 
  std::vector<double> b{1.0,2.0};
  std::vector<double> w{1.0};

  // Calculate TP and load disease model. 
  disease_model covid(beta, q, xi, contact_matrix, b, w);

  // Output informations. 
  std::vector<double> tout;
  // std::vector<double> population_mean_protectionInfection;
  // std::vector<double> population_mean_protectionSymptoms;
  // std::vector<double> population_mean_protectionOnwards;
  std::vector<std::vector<double>> ageProtectionInfection(0,std::vector<double>(num_brackets,0.0));
  std::vector<std::vector<double>> ageProtectionSymptoms(0,std::vector<double>(num_brackets,0.0));
  std::vector<std::vector<double>> ageProtectionOnwards(0,std::vector<double>(num_brackets,0.0));
  std::vector<std::vector<double>> ageOverallReduction(0,std::vector<double>(num_brackets,0.0));


  // Vaccinate people! 
  std::vector<VaccinationSchedule> first_doses;
  std::vector<VaccinationSchedule> second_doses;
  std::vector<VaccinationSchedule> booster_doses;

  // Assign First doses. 
  for(int i = 0; i < residents.size(); ++i) {
    Individual & person = residents[i];
    Individual::VaccineHistory& vaccinations = residents[i].vaccinations;
    if(vaccinations.size()==0){
      continue; 
    } else {
    double time_dose = vaccinations[0].first;
    VaccineType v = vaccinations[0].second;
    first_doses.push_back(VaccinationSchedule(vaccinations[0].first, i, vaccinations[0].second));
    }
  }


  while(t <= t_end) {
    std::cout << "Time is " << t << " \n";
    std::cout << first_doses.size() << " " << second_doses.size() << " " << booster_doses.size() << "\n";
    // Loop  through all first_doses (efficiency is not great oh well)
    auto first_it = std::remove_if(first_doses.begin(), first_doses.end(),[&](auto& x)->bool{
      // Function for first doses. 
      if(x.t<=t) {
        // std::cout << x.t <<", " << x.person <<", " <<x.vaccine <<std::endl;
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);
        
        Individual::VaccineHistory& vaccinations = residents[x.person].vaccinations;

        if(vaccinations.size()>1){
        second_doses.push_back(VaccinationSchedule(vaccinations[1].first, x.person, vaccinations[1].second));
        }

        return true;
      } else {
        return false; 
      }

    });
    first_doses.erase(first_it,first_doses.end());

    // Loop through all second doses (efficiency is not great oh well)
    auto second_it = std::remove_if(second_doses.begin(), second_doses.end(),[&](auto& x)->bool{
      // Function for second doses
      if(x.t <= t) {
        // std::cout << x.t <<", " << x.person <<", " <<x.vaccine <<std::endl;
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);

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
    second_doses.erase(second_it,second_doses.end());


#ifndef DISABLE_BOOSTERS
    // Loop through all booster doses (efficiency is not great oh well)
    auto booster_it = std::remove_if(booster_doses.begin(), booster_doses.end(),[&](auto & x)->bool{
      if(x.t <= t) {
        //Booster dose. 
        // std::cout << x.t <<", " << x.person <<", " <<x.vaccine <<std::endl;
        covid.boostNeutsVaccination(residents[x.person],t,x.vaccine);

        return true; 
      } else {
        return false;
      }
    });
    booster_doses.erase(booster_it,booster_doses.end());
#endif

    // How do the neutralising antibodies decay. 
    double population_pInfect = 0.0;
    double population_pSymptoms = 0.0;
    double population_pOnwards = 0.0;
    std::vector<double> age_pInfect(num_brackets,0.0);
    std::vector<double> age_pSymptom(num_brackets,0.0);
    std::vector<double> age_pOnward(num_brackets,0.0);
    std::vector<double> age_Overall(num_brackets,0.0);
    
    for(int i = 0; i < residents.size(); i++) {
      int age_bracket = residents[i].age_bracket;
      double Infect = covid.getProtectionInfection(residents[i],t);
      double Symptom = covid.getProtectionSymptoms(residents[i],t);
      double Onwards = covid.getProtectionOnwards(residents[i],t);
      population_pInfect += Infect;
      population_pSymptoms += Symptom;
      population_pOnwards += Onwards;
      age_pInfect[age_bracket]+= Infect;
      age_pSymptom[age_bracket]+= Symptom;
      age_pOnward[age_bracket]+=Onwards;
      age_Overall[age_bracket]+= 1.0 - (1.0 - Infect)*(1.0 - Onwards);
      

    }

    for(int i = 0; i < num_brackets; ++i) {
      age_pInfect[i] = age_pInfect[i]/age_bracket_count[i];
      age_pSymptom[i] = age_pSymptom[i]/age_bracket_count[i];
      age_pOnward[i] = age_pOnward[i]/age_bracket_count[i];
      age_Overall[i] = age_Overall[i]/age_bracket_count[i];
    }

    tout.push_back(t);
    // population_mean_protectionInfection.push_back(population_pInfect/residents.size());
    // population_mean_protectionSymptoms.push_back(population_pSymptoms/residents.size());
    // population_mean_protectionOnwards.push_back(population_pOnwards/residents.size());

    ageProtectionInfection.push_back(age_pInfect);
    ageProtectionSymptoms.push_back(age_pSymptom);
    ageProtectionOnwards.push_back(age_pOnward);
    ageOverallReduction.push_back(age_Overall);

    t+=dt;
  }
  
  // Write output to file.
  // std::ofstream output_file("PopulationAverageNoBooster.csv");
  // if(output_file.is_open()){
  //   output_file << "Time, Protection, Type of immunity \n";
  //   for(int i =0; i < population_mean_protectionInfection.size(); ++i) {

  //       output_file << tout[i] << ", " << population_mean_protectionInfection[i] << ", " << "Acquisition\n";
  //       output_file << tout[i] << ", " << population_mean_protectionSymptoms[i] << ", " << "Symptoms\n";
  //       output_file << tout[i] << ", " << population_mean_protectionOnwards[i] << ", " << "Onwards transmission\n";
  //   }
  
  // output_file.close();
  // }

  std::string output_filename = directory  + "/sim_number_" + std::to_string(sim_number) + ".csv";
  // Write output to file.
  std::ofstream output_age_file(output_filename);
  if(output_age_file.is_open()){
    output_age_file << "Time, Age, Protection, Type of immunity, Sim \n";
    for(int i =0; i < ageProtectionInfection.size(); ++i) {
      for(int j = 0; j < ageProtectionInfection[i].size(); ++j) {
        output_age_file << tout[i] << ", " << j << ", " << ageProtectionInfection[i][j] << ", " << "Acquisition, " << sim_number << "\n";
        output_age_file << tout[i] << ", " << j << ", " << ageProtectionSymptoms[i][j] << ", " << "Symptoms, " << sim_number << "\n";
        output_age_file << tout[i] << ", " << j << ", " << ageProtectionOnwards[i][j] << ", " << "Onwards transmission, " << sim_number << "\n";
        output_age_file << tout[i] << ", " << j << ", " << ageOverallReduction[i][j] << ", " << "Overall reduction, " << sim_number << "\n";

      }
    }
  
  output_age_file.close();
  }

  return 0; 
}