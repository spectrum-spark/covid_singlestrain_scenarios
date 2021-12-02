#include "abm/individual.h"
#include "abm/abmrandom.h"

// Take an age and sort it. 
static int age_sort(double& age, std::vector<double>& age_brackets){
  // Return the age bracket of the individual.
  // Agesort needs a minus one for the final one because referenced from zero!
  for(int i = 0; i < (int) age_brackets.size()-1; i++){
    if(age < age_brackets[i+1]){
        return i;
    }
  }

  return (int) (age_brackets.size()-1);
  
}

//  Define constructor for the disease class (removed the trivial constructor)
Disease::Disease(char status)
    : infection_status(status),
      asymptomatic(false),
      severe(false),
      transmissibility(std::nan("1")),
      time_of_exposure(std::nan("2")),
      time_of_symptom_onset(std::nan("3")),
      time_of_infection(std::nan("4")),
      time_of_recovery(std::nan("5")),
      log10_neuts_at_exposure(std::nan("6")),
      check_symptoms(true),
      cluster_number(-1) {}

Individual::Individual(double& age_in, std::vector<double>& age_brackets_in,std::vector<std::pair<double,size_t>>& Vaccinations) 
    : covid('S'),
      age(age_in),
      age_bracket(age_sort(age_in,age_brackets_in)),
      secondary_infections(0),
      log10_neutralising_antibodies(std::numeric_limits<double>::min()),
      old_log10_neutralising_antibodies(0.0),
      time_last_boost(0.0),
      decay_rate(0.0),
      time_isolated(std::nan("7")),
      isCovidNaive(true),
      isVaccinated(false) {}

std::ostream& operator<<(std::ostream& os, const Individual & person) {
  os << person.age <<", " << person.age_bracket <<", " << person.covid.infection_status;
  return os;
}
