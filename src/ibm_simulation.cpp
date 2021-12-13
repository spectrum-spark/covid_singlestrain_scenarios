#include <algorithm>
#include "abm/nbinrnd.h"
#include "abm/abmrandom.h"
#include "abm/ibm_simulation.h"

// Constructor for disease model, vector betas
disease_model::disease_model(std::vector<double> beta_C_in, std::vector<double> q_in, std::vector<double> xi_in, std::vector<std::vector<double>> contact_matrix_in, std::vector<double> b,std::vector<double> w)
    : beta_C(beta_C_in),
      q(q_in),
      xi(xi_in),
      k(exp(1.201998516)),
      c50_acquisition(-0.567888054),
      c50_symptoms(-0.619448181),
      c50_transmission(0.077153705),
      sd_log10_neut_titres(0.4647092),
      log10_mean_neut_infection(0.0),
      log10_mean_neut_AZ_dose_1(-0.642536778),
      log10_mean_neut_AZ_dose_2(-0.193159173),
      log10_mean_neut_Pfizer_dose_1(-0.331614187),
      log10_mean_neut_Pfizer_dose_2(0.225736770),
      log10_mean_neut_Pfizer_dose_3(1.128683850)
       {

    double scale_e = 4.817559;
    double scale_S = 1.013935;
    double scale_r = 1.000000;
    double mu = 1.5;
    
    contact_matrix = contact_matrix_in; // Could move into initialiser list. 

    gen_tau_E = std::gamma_distribution<double>(scale_e,2.5/scale_e); //1.7911264 0.8504219 0.5444788
    gen_tau_R = std::gamma_distribution<double>(scale_r,mu/scale_r); //6.069358 2.189083 1.691274, 3.817559 1.013935 1.000000
    
    gen_tau_S = std::gamma_distribution<double>(scale_S,(5.1-2.5)/scale_S);
    gen_tau_isolation = std::piecewise_constant_distribution<double>(b.begin(),b.end(),w.begin()); // When are they isolated.

    // Should do a bunch of checks on the beta q xi and contact matrix for sizes. 
};


// // Constructor for disease model, scalar beta's
// disease_model::disease_model(double beta_C_in, std::vector<std::vector<double>> contact_matrix_in,std::vector<double> b,std::vector<double> w)
//     : beta_C(beta_C_in),
//       k(3.0977), // logistic slope exp(1.130661), from Slack
//       c50_acquisition(-0.691),
//       c50_symptoms(-0.697),
//       c50_transmission(0.118) {

//     double scale_e = 4.817559;
//     double scale_S = 1.013935;
//     double scale_r = 1.000000;
//     double mu = 1.5;
    
//     contact_matrix = contact_matrix_in; 
//     gen_tau_E = std::gamma_distribution<double>(scale_e,2.5/scale_e); //1.7911264 0.8504219 0.5444788
//     gen_tau_R = std::gamma_distribution<double>(scale_r,mu/scale_r); //6.069358 2.189083 1.691274, 3.817559 1.013935 1.000000
    
//     gen_tau_S = std::gamma_distribution<double>(scale_S,(5.1-2.5)/scale_S);
//     gen_tau_isolation = std::piecewise_constant_distribution<double>(b.begin(),b.end(),w.begin()); // When are they isolated.

// };

//  Covid model Age stratified Individual contacts. (ASCM - age stratified
//  contact model)
double disease_model::covid_ascm(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double t1, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic){
//  Evaluates a covid model based on Individual contacts from t0 to t1 with
//  timestep of dt. Returns the current time value.

  // Error check the size of the age_ref vs the contact matrix. Throw error if
  // not the same size.
  if(contact_matrix.size()!=age_ref.size()){
      throw std::logic_error("The contact matrix and age reference matrix are not the same size. Check the dimensions of your stratification!");
  }

  if(t0 >= t1){
      throw std::logic_error("Incorrect time specified. t_0 is larger than (or equal to) t_1 in disease_model::covid_ascm.");
  }
    
  double t = t0;
  // Timestep until the next step would be equal or pass the end time.
  while(t < t1){
      if(t+dt > t1){
          //  Complete the last time step, ensuring that it finishes exactly
          //  at tend.
          dt = t1 - t;
      }
      // Run one step of the simulation.
      t = covid_one_step_ascm(residents, age_ref, t, dt, E, I, newly_symptomatic);
      
  }
// Return the time value, should always be tend.
  return t;
}

 
bool disease_model::distribution_infected_update(Individual& person, size_t& ind_number, std::vector<size_t>& newly_symptomatic, double& t){
    
    // This function is in charge of determining the updates of infected
    // individuals.
    bool symptom_latch = person.covid.check_symptoms; // Define a symptom latch to control that individuals develop symptoms once.
    bool develop_symptoms = (symptom_latch)&&(t > person.covid.time_of_symptom_onset)&&(!person.covid.asymptomatic); // Will they develop symptoms.
    bool recovery = (t > person.covid.time_of_recovery);
    
    if(recovery){
        recover_individual(person); // Do not require t in this function as we can assign time of recovery at point of infection.
    }else if(develop_symptoms){
        // Determine if they become symptomatic (also severity?) // Can be
        // determined at infection time.
        newly_symptomatic.push_back(ind_number); // The individuals that have developed symptoms today.
        person.covid.check_symptoms = false; // Activate latch for this Individual.
    } // I am giving precedence to recovering here. If you recover before you develop symptoms, because dt is too large, thats what happens (super unlikely but).

    return recovery;
}


bool disease_model::distribution_exposed_update(Individual& person, size_t& ind_number, std::vector<size_t>& newly_infected, double& t){
  // This function returns true if you move from exposed to infected.
  bool infected = (t > person.covid.time_of_infection);
  if(infected){
    infect_individual(person);
    newly_infected.push_back(ind_number); // Must pass in Individual number here.
  }
  return infected;
}

void disease_model::infection_ascm(double t, Individual&infected_individual, std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double dt, std::vector<size_t>& newly_exposed){
   
  // This function will alter the infection status of any contacts that are infected
  int individual_bracket = infected_individual.age_bracket; // Infected individuals age bracket.
  int cluster_number = infected_individual.covid.cluster_number;
  bool isolated = (t >= infected_individual.time_isolated); // Are they isolated at this current time. I dont have to put in  check for the maximum time, because they will only be isolated for the time they are infectious and I dont check if they are isolated at the point of infection.


  if(std::isnan(infected_individual.time_isolated)){
      throw std::logic_error("Probability of infection is Nan.");
  }
  
  //  Community transmission. The person will contact people depending upon
  //  the contact matrix. For each component of the contact matrix we sample
  //  how many contacts they make from each age bracket.
  for(size_t age_strata = 0; age_strata < contact_matrix.size(); age_strata++){
        
#define NEGBIN
#ifdef NEGBIN

    // Update for negative binomial. 
    double r_daily = 0.050;
    double mu_contacts = static_cast<double>(contact_matrix[individual_bracket][age_strata]);
    double p = mu_contacts/(r_daily+mu_contacts);

    // Note that contact matrix is square so doesnt matter which dimension
    // has their size checked. 
    nbinrnd gen_num_contacts(r_daily*dt,p); // Define the Distribution from which we sample community contacts.
    size_t num_in_strata = age_ref[age_strata].size(); // Must be obtained from the reference to the age matrix.
#endif
#ifdef POISSON
    // Average number of contacts per day.
    double mu_contacts = contact_matrix[individual_bracket][age_strata];

    // Note that contact matrix is square so doesnt matter which dimension
    // has their size checked.
    std::poisson_distribution<int> gen_num_contacts(mu_contacts*dt); // Create the probability distributon for the number of contacts.

    // The dt scale is so that it makes sense.
    size_t num_in_strata = age_ref[age_strata].size(); // Must be obtained from the reference to the age matrix.
#endif

    if(num_in_strata == 0){
        continue;    // Skip strata as no-one is in it.
    }
    
    std::uniform_int_distribution<size_t> gen_reference(0,num_in_strata-1);
    int number_comm_contacts = gen_num_contacts(generator);
        
    for(int i = 0; i < number_comm_contacts; i++){
      int contact_ref = age_ref[age_strata][gen_reference(generator)];
      
      // This is where we can finish generating contacts, the rest of
      // the loop calculated whether they are infected. Should this be
      // split ?
      Individual& contact = residents[contact_ref]; // Define which community member was contacted.
      // Track all contacts (We can then implement how good contact
      // tracing is currently disabled)
      if(contact.covid.infection_status == 'S'){
        // Do they get infected.
        double r = genunf_std(generator);
        double prob_transmission = (!isolated)*infected_individual.covid.transmissibility*getSusceptibility(contact,t);

        // if(t < infected_individual.covid.time_of_symptom_onset){
        //   prob_transmission = prob_transmission*2.29;
        // }

        if(r < prob_transmission){   // This part doesnt need the dt, because the dt is taken into account earlier by limiting the number of contacts per timesteps.
          newly_exposed.push_back(contact_ref);
          expose_individual(contact,t);
          ++infected_individual.secondary_infections;
          contact.covid.cluster_number = cluster_number;
        }   
      }
    }
  }
};

double  disease_model::covid_one_step_ascm(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic){
    // The ordering of this function is important. Infected individuals, then
    // exposed. There is a shift in memory location for each true statement that
    // comes from std::remove_if. This is faster than creating a new vector
    // (checked with example).
    
    // Reserve memory for new infections... Small but should save from
    // reallocation costs which can be significant.
    std::vector<size_t> newly_exposed; newly_exposed.reserve(3000); // 3000 is a magic number... could try different values. Somehow relate to dt could be possible.
    std::vector<size_t> newly_infected; newly_infected.reserve(3000); // Could make dependent upon the number of exposed individuals.
    
    // Loop over all infected individuals, removing those that recover. This
    // will alter a vector newly_exposed to have the newly exposed individuals.
    auto recovered_it = std::remove_if(I.begin(),I.end(),[&](size_t& ind_ref)->bool{
      
      // Infected Individual
      Individual& person = residents[ind_ref];
      
      //Error check.
      if(person.covid.infection_status!='I'){
          throw std::logic_error("Individual in I vector does not match infection status.");
      }

      // Community infection model.
      infection_ascm(t0, person, residents, age_ref, dt, newly_exposed);
      
      return distribution_infected_update(person, ind_ref, newly_symptomatic, t0); // If infected, do they recover, this function must alter the Individual disease status.
    });
    
    // Loop over Exposed individuals. Note that this does not include
    // newly_exposed individuals.
    auto infected_it = std::remove_if(E.begin(),E.end(),[&](size_t& ind_ref)->bool{
        
      // Get person of interest.
      Individual& person = residents[ind_ref];
      
      //Error check.
      if(person.covid.infection_status!='E'){
          throw std::logic_error("Individual in E vector does not match infection status.");
      }
      
      bool infected = distribution_exposed_update(person,ind_ref,newly_infected, t0); // Distribution exposed update should now update individuals to be infected., this function must alter the Individual disease status.
      return infected;
    });
    
    // We have a vector of newly exposed individuals and an iterator,
    // recovered_it, that points to the location of recovered individuals.
    I.erase(recovered_it,I.end()); // Remove the recovered individuals from the vector of infections (could be done at the end).
    I.insert(I.end(),newly_infected.begin(),newly_infected.end()); // Adds the removed end of E to the end of I.
    
    // We cannot insert the remove_if values to the end of I as the value after
    // remove_if is unspecified.
    E.erase(infected_it,E.end()); // Remove the exposed individuals that are now infected.
    E.insert(E.end(),newly_exposed.begin(),newly_exposed.end()); // Insert the newly exposed individuals to the end of exposed individuals.
    
    // The probability of tranisitioning into a new compartment is now dependent
    // upon the order of the individuals in E and I. This should be better for
    // branch prediction. It is still stochastic so its not just perfect order,
    // but its better! (Very likely to be false at the end).

  return t0 + dt;
}

void disease_model::seed_exposure(Individual& resident, double& t){
    expose_individual(resident, t);
}

void disease_model::infect_individual(Individual& resident){
    resident.covid.infection_status = 'I';
}


void disease_model::recover_individual(Individual& resident){ 
    susceptible_individual(resident);
    //Write output of the infection here ? Where shall it get written. 
    // output.push_back(DiseaseOutput(resident));
}

void disease_model::susceptible_individual(Individual& resident){
    resident.covid.infection_status = 'S';
}

void disease_model::expose_individual(Individual& resident, double& t){
  
  resident.covid.infection_status = 'E';
  resident.covid.time_of_exposure = t;
  resident.covid.time_of_infection = resident.covid.time_of_exposure + gen_tau_E(generator);
  resident.covid.time_of_symptom_onset = resident.covid.time_of_infection + gen_tau_S(generator);
  resident.covid.time_of_recovery = resident.covid.time_of_symptom_onset + gen_tau_R(generator);
  resident.time_isolated = resident.covid.time_of_symptom_onset + gen_tau_isolation(generator); // This is hardcoded for now.

  // Determine if the Individual will be asymptomatic and the severity of the disease. 
  double r = genunf_std(generator);
  double prob_symptomatic = getProbabilitySymptomatic(resident, t);
  bool   asymptomatic = r > prob_symptomatic; // You are asymptomatic. 
  resident.covid.asymptomatic = asymptomatic;
  resident.covid.check_symptoms = true; // Set the symptom latch. 
  
  // Severity check (Currently in model of care).
  resident.covid.severe = false; // This is currently disabled.
  
  // Determine the transmissibility of the Individual. 
  assignTransmissibility(resident, t, asymptomatic); // This is 1 - VE_O and is constant throughout the infecton period) If theyre asymptomatic iy must be smaller!

  // Set Neut levels!  You have been exposed to covid your neutralising antibodies will now do a thing.
  boostNeutsInfection(resident,t); // What do the neuts go to (also assigns old Neutralising antibody levels)

  // Set statistics for tracking - required for log10 neuts.
  // Write log10 neuts for MOC. 
  resident.covid.log10_neuts_at_exposure = resident.old_log10_neutralising_antibodies; 

}


// This code is used to check the R0.
double disease_model::covid_ascm_R0(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double t1, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic){

//  Evaluates a covid model based on Individual contacts from t0 to t1 with
//  timestep of dt. Returns the current time value.

    // Error check the size of the age_ref vs the contact matrix. Throw error if
    // not the same size.
    if(contact_matrix.size()!=age_ref.size()){
        throw std::logic_error("The contact matrix and age reference matrix are not the same size. Check the dimensions of your stratification!");
    }

    if(t0 >= t1){
        throw std::logic_error("Incorrect time specified. t_0 is larger than (or equal to) t_1 in disease_model::covid_ascm.");
    }
    
double t = t0;
// Timestep until the next step would be equal or pass the end time.
    while(t < t1){
        if(t+dt > t1){
            //  Complete the last time step, ensuring that it finishes exactly
            //  at tend.
            dt = t1 - t;
        }
        // Run one step of the simulation.
        t = covid_one_step_ascm_R0(residents, age_ref, t, dt, E, I, newly_symptomatic);
        
    }
// Return the time value, should always be tend.
return t;
}

double  disease_model::covid_one_step_ascm_R0(std::vector<Individual>& residents, std::vector<std::vector<int>>& age_ref, double t0, double dt, std::vector<size_t>& E, std::vector<size_t>& I,std::vector<size_t>& newly_symptomatic){
    // E and I are all that is needed to generate incidence? (Do I want to add E
    // and I to the disease_model class?)

    // The ordering of this function is important. Infected individuals, then
    // exposed. There is a shift in memory location for each true statement that
    // comes from std::remove_if. This is faster than creating a new vector
    // (checked with example). Reserve memory for new infections... Small but
    // should save from reallocation costs which can be significant.
    std::vector<size_t> newly_exposed; newly_exposed.reserve(3000); // 3000 is a magic number... could try different values. Somehow relate to dt could be possible.
    std::vector<size_t> newly_infected; newly_infected.reserve(1); // Could make dependent upon the number of exposed individuals.
    
    // Loop over all infected individuals, removing those that recover. This
    // will alter a vector newly_exposed to have the newly exposed individuals.
    auto recovered_it = std::remove_if(I.begin(),I.end(),[&](size_t& ind_ref)->bool{
       
      // Infected Individual
      Individual& person = residents[ind_ref];
      
      //Error check.
      if(person.covid.infection_status!='I'){
          throw std::logic_error("Individual in I vector does not match infection status.");
      }
            
        
      // Community infection model.
      infection_ascm(t0, person, residents, age_ref, dt, newly_exposed);
      
      return distribution_infected_update(person, ind_ref, newly_symptomatic, t0); // If infected, do they recover, this function must alter the Individual disease status.
    });
    
    // Loop over Exposed individuals. Note that this does not include
    // newly_exposed individuals.
    auto infected_it = std::remove_if(E.begin(),E.end(),[&](size_t& ind_ref)->bool{
        
        // Get person of interest.
        Individual& person = residents[ind_ref];
        
            //Error check.
            if(person.covid.infection_status!='E'){
                throw std::logic_error("Individual in I vector does not match infection status.");
            }
        
        bool infected = distribution_exposed_update(person,ind_ref,newly_infected, t0); // Distribution exposed update should now update individuals to be infected., this function must alter the Individual disease status.
        
        return infected;
        
    });
    // We have a vector of newly exposed individuals and an iterator,
    // recovered_it, that points to the location of recovered individuals.
    I.erase(recovered_it,I.end()); // Remove the recovered individuals from the vector of infections (could be done at the end).
    I.insert(I.end(),newly_infected.begin(),newly_infected.end()); // Adds the removed end of E to the end of I.
    
    // We cannot insert the remove_if values to the end of I as the value after
    // remove_if is unspecified.
    E.erase(infected_it,E.end()); // Remove the exposed individuals that are now infected.
    // Do not add newly exposed individuals, we just want them to be exposed.
    return t0 + dt;
}

double disease_model::getSusceptibility(const Individual& person, double& t){
  return (1.0 - getProtectionInfection(person,t))*xi[person.age_bracket];
}

double disease_model::getProbabilitySymptomatic(const Individual& person, double& t){
  return (1.0 - getProtectionSymptoms(person,t))*q[person.age_bracket];
   // This should be an odds ratio. 
}

void disease_model::assignTransmissibility(Individual& person, double& t, bool& asymptomatic) {
  person.covid.transmissibility = (1.0 - 0.5*(asymptomatic))*(1.0 - getProtectionOnwards(person,t))*beta_C[person.age_bracket];
}

double disease_model::calculateNeuts(const Individual& person, double& t){
  return person.log10_neutralising_antibodies - person.decay_rate*(t-person.time_last_boost)/log(10.0); // We are working in log neuts so if exponential is in base e then k is log10(e)*k. 
}

// used multiple times. 
static void assignNewNeutValue(const double& log10_neuts,const double& sd_log10_neuts, Individual& person, double& t) {
  // Might include ucrrent neuts as inputs. 
  std::normal_distribution<double> sample_neuts(log10_neuts, sd_log10_neuts);
  double new_neuts = sample_neuts(generator);

  // If we really want, we can add a check for time here. 
  // if(person.time_last_boost + 14.0 >= t) {
  //   // They were boosted so recent! Theyre still on the way up!
  // }

  if(new_neuts >= person.old_log10_neutralising_antibodies){
    person.log10_neutralising_antibodies = new_neuts;
  } else {
    person.log10_neutralising_antibodies = person.old_log10_neutralising_antibodies;
  } 

  person.time_last_boost = t; 

}

void disease_model::boostNeutsInfection(Individual& person, double& t){
  person.old_log10_neutralising_antibodies = calculateNeuts(person, t); // Assign the old neuts here. 
  assignNewNeutValue(log10_mean_neut_infection,sd_log10_neut_titres,person,t);
}

void disease_model::boostNeutsVaccination(Individual& person, double& t, VaccineType& vaccine ){
  person.old_log10_neutralising_antibodies = calculateNeuts(person, t); 
  // We can do fold increase in neuts here depending upon the individuals previous exposure ( + log10(N) would be an N fold increase)
  double log10_boost; 

  switch(vaccine){
    case VaccineType::AZ1 :
      log10_boost = log10_mean_neut_AZ_dose_1;
      break;
    case VaccineType::AZ2 : 
      log10_boost = log10_mean_neut_AZ_dose_2;
      break;
    case VaccineType::Pfizer1 :
      log10_boost = log10_mean_neut_Pfizer_dose_1;
      break;
    case VaccineType::Pfizer2 :
      log10_boost = log10_mean_neut_Pfizer_dose_2;
      break;
    case VaccineType::Moderna1 :
      log10_boost = log10_mean_neut_Pfizer_dose_1;
      break;
    case VaccineType::Moderna2 :
      log10_boost = log10_mean_neut_Pfizer_dose_2;
      break;
    case VaccineType::Booster :
      log10_boost = log10_mean_neut_Pfizer_dose_3;
      break;
    default:
    throw std::logic_error("Unrecognised vaccation in boostNeutsVaccination. \n");
  }
  // std::cout << log10_boost << ", " << sd_log10_neut_titres << std::endl;
  assignNewNeutValue(log10_boost,sd_log10_neut_titres,person,t);
}

// used multiple times. 
static inline double prob_avoid_outcome(const double& log10_neuts, const double& k, const double& c50) {
  return 1.0/( 1.0 + exp(-k*(log10_neuts-c50)));
}

double disease_model::getProtectionInfection(const Individual& person, double& t) {
  double n = calculateNeuts(person, t);
  return prob_avoid_outcome(n, k, c50_acquisition);
}

double disease_model::getProtectionSymptoms(const Individual& person, double& t){
  double n = calculateNeuts(person, t);
  return prob_avoid_outcome(n, k, c50_symptoms);
}

double disease_model::getProtectionOnwards(const Individual& person, double& t) {
  double n = calculateNeuts(person, t);
  return prob_avoid_outcome(n, k, c50_transmission); 
}