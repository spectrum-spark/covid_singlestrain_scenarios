#include "abm/individual.h"
#include "abm/abmrandom.h"

//  Define constructor for the disease class (removed the trivial constructor)
Disease::Disease(char status):infection_status(status),asymptomatic(false),severe(false),transmissibility(std::nan("1")),time_of_exposure(std::nan("2")),time_of_symptom_onset(std::nan("3")),time_of_infection(std::nan("4")),time_of_recovery(std::nan("5")),log10_neuts_at_exposure(std::nan("6")),check_symptoms(true),cluster_number(-1){
  // Set all values in the disease class. 
  
}

Individual::Individual(double& age_in, int& age_bracket_in):covid('S'),age(age_in),age_bracket(age_bracket_in),secondary_infections(0),log10_neutralising_antibodies(0.0),old_log10_neutralising_antibodies(0.0),time_last_boost(0.0),decay_rate(0.0),time_isolated(std::nan("7")),isCovidNaive(true),isVaccinated(false) {}

// // // Individual constructor - modified for the vaccination_parameters class.
// // individual::individual(double age, int age_bracket_in, int home_id, int community_id, vaccine_parameters & Vaccination):age_bracket(age_bracket_in),age(age),home_id(home_id),community_id(community_id),covid(disease('S')),vaccine_status(vaccine(Vaccination,age_bracket_in)){
// //     current_community =     community_id;   // Assign to home community
// //     current_home      =     home_id;        // Assign to household.
// // }

// // void individual::update_age(const double &dt){
// //     age += dt/365.0;  //  Age is in years and dt is in days.
// // //    time_since_last_test += dt;
// // }

// double generate_age(int bracket, const std::vector<double> &age_brackets){
//    // This function has hardcoded the oldest is the age bracket + 10. 
//    // Uniformly samples age between the two brackets. 
//     double r = genunf_std(generator);
//     double diff;

//     if(bracket == (int) age_brackets.size()-1){
//         diff = 10; 
//     }else{
//         diff = age_brackets[bracket+1] - age_brackets[bracket];
//     }
    
//     return age_brackets[bracket] + r*diff;  
// }

// int age_sort(individual &person,std::vector<double> age_brackets){
//     // Return the age bracket of the individual. Ths function is hardcoded to be in groups of 10 years.
//     // Agesort needs a minus one for the final one because referenced from zero!
//     double age = person.age;
//     for(int i = 0; i < (int) age_brackets.size()-1; i++){
        
//         if(age < age_brackets[i+1]){
//             person.age_bracket = i;
//             return i;
//         }
//     };  
//     person.age_bracket = (int) age_brackets.size()-1;
//     return (int) (age_brackets.size()-1);
// }

// int age_sort(double age,std::vector<double> age_brackets){
//     // Return the age bracket of the individual. Ths function is hardcoded to be in groups of 10 years.
//     // Agesort needs a minus one for the final one because referenced from zero!
//     for(int i = 0; i < (int) age_brackets.size()-1; i++){
        
//         if(age < age_brackets[i+1]){
//             return i;
//         }


//     };

//     return (int) age_brackets.size()-1;
// }

// // Contact class. 
// trace_contact::trace_contact(int ind_number, double t):time(t),who(ind_number){}
// trace_contact::trace_contact(){}

// void trace_contact::update_time(double t){
//     time = t;
// }

// simulation_statistics::simulation_statistics(){};
// void simulation_statistics::set_infection_stats(vaccine_type vax, int number_doses, double time_latest){
//     vaccine_status = vax;
//     doses = number_doses;
//     time_of_last_dose = time_latest;
// }
