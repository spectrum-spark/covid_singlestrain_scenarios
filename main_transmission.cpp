#include <iostream>
#include <sstream>
#include <fstream>
#include <sys/stat.h>
#include <sys/types.h>
#include "abm/quantium_read.h"
#include "abm/abmrandom.h"
#include "abm/ibm_simulation.h"
#include "nlohmann/json.hpp"

void assemble_age_matrix(const std::vector<Individual> & residents, std::vector<std::vector<int>> & age_matrix){

    // Assign residents to their age matrix.
    for(int i = 0; i < (int) residents.size(); i++){
        int bracket = residents[i].age_bracket;
        age_matrix[bracket].push_back(i);
    }
}


size_t bin_data(double& x, const std::vector<double>& upper_bounds){
  if(x < 0) std::cout << x << std::endl;
  if(x > 1) std::cout << x << std::endl;

  for(size_t bin=0; bin < upper_bounds.size(); ++bin) {
    if(x < upper_bounds[bin]){
      return bin;
    }
  }
  return -1;
}

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
  double vaccination_dt = 7.0;
  double covid_dt = pow(2.0,-4.0);

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
  // std::vector<double>bin_upperbound;
  // double upper_bound = 0;
  // while(upper_bound <= 1.0) {
  //   bin_upperbound.push_back(upper_bound);
  //   upper_bound+=pow(2,-10);  
  // }
  // size_t number_bins = bin_upperbound.size();
  
  size_t number_bins = residents.size();
  
  std::vector<double> tout;
  // This will bin the individuals into VE.
  // std::vector<std::vector<double>> population_protectionInfection(0,std::vector<double>(number_bins,0.0));
  // std::vector<std::vector<double>> population_protectionSymptoms(0,std::vector<double>(number_bins,0.0));
  // std::vector<std::vector<double>> population_protectionOnwards(0,std::vector<double>(number_bins,0.0));

  // std::vector<std::vector<double>> population_OverallReduction(0,std::vector<double>(number_bins,0.0));

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

  // Assemble the age_matrix (this is a list of people that are in each age bracket).
  std::vector<std::vector<int>> age_matrix(num_brackets);
  assemble_age_matrix(residents,age_matrix); // Nobody moves from the age matrix so only have to do it once.

    // Create memory that tracks who is exposed, E_ref, and who is infected, I_ref. gen_res is used to sample from the list of residents uniformly.
    std::vector<size_t> E_ref; E_ref.reserve(10000); // Magic number reserving memory.
    std::vector<size_t> I_ref; I_ref.reserve(10000); // Magic number of reserved.

    // // Use cluster ref to track the infections phylogenetic tree.
    // std::uniform_int_distribution<size_t> gen_res(0,residents.size()-1); 
    // int cluster_ref = 0; 
    // int initial_infections = 0; // Count initial infections.
    // int total_initial_infected = inputs["initial_infections"]; 
    // while(initial_infections < total_initial_infected){
    //     int exposed_resident = gen_res(generator); // Randomly sample from all the population.
    //     if(residents[exposed_resident].vaccine_status.get_type()==vaccine_type::none){
    //         if(residents[exposed_resident].covid.infection_status!='E'){
    //             covid.seed_exposure(residents[exposed_resident],t); // Random resident has become infected
    //             residents[exposed_resident].covid.cluster_number = cluster_ref;
    //             ++initial_infections;
    //             E_ref.push_back(exposed_resident); // Start tracking them.
    //         }
    //     }
    // }


  while(t <= t_end) {
    std::cout << "Time is " << t << " \n";
    std::cout << first_doses.size() << " " << second_doses.size() << " " << booster_doses.size() << "\n";
    // Loop  through all first_doses (efficiency is not great oh well)
    auto first_it = std::remove_if(first_doses.begin(), first_doses.end(),[&](auto& x)->bool{
      // Function for first doses. 
      if(x.t<=t) {
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

    std::vector<size_t> newly_symptomatic; newly_symptomatic.reserve(1000);

    // Simulate the disease model here. 
    t = covid.covid_ascm(residents,age_matrix,t,t+vaccination_dt,covid_dt,E_ref,I_ref,newly_symptomatic);
  }
  


  std::string output_filename = directory  + "/sim_number_" + std::to_string(sim_number) + ".csv";
  // Write output to file.
  std::ofstream output_age_file(output_filename);
  if(output_age_file.is_open()){  
  output_age_file.close();
  }

  return 0; 
}