#include "abm/individual.h"
#include "abm/abmrandom.h"

// Take an age and sort it.
static int age_sort(double &age, std::vector<double> &age_brackets)
{
  // Return the age bracket of the individual.
  // Agesort needs a minus one for the final one because referenced from zero!
  for (int i = 0; i < (int)age_brackets.size() - 1; i++)
  {
    if (age < age_brackets[i + 1])
    {
      return i;
    }
  }
  return (int)(age_brackets.size() - 1);
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

Individual::Individual(double &age_in, std::vector<double> &age_brackets_in, std::vector<std::pair<double, VaccineType>> &vaccination_in, nlohmann::json &ve_params)
    : covid('S'),
      age(age_in),
      age_bracket(age_sort(age_in, age_brackets_in)),
      secondary_infections(0),
      log10_neutralising_antibodies(std::numeric_limits<double>::lowest()),
      old_log10_neutralising_antibodies(std::numeric_limits<double>::lowest()),
      time_last_boost(0.0),
      decay_rate(ve_params["neut_decay"]),
      time_isolated(std::nan("7")),
      isCovidNaive(true),
      isVaccinated(false),
      vaccinations(vaccination_in),
      number_infections(0)
{}

Individual::Individual(double &age_in, std::vector<double> &age_brackets_in, std::vector<std::pair<double, VaccineType>> &vaccination_in, nlohmann::json &ve_params, size_t &num_infections, double &time_of_past_infection)
    : covid('S'),
      age(age_in),
      age_bracket(age_sort(age_in, age_brackets_in)),
      secondary_infections(0),
      log10_neutralising_antibodies(std::numeric_limits<double>::lowest()),
      old_log10_neutralising_antibodies(std::numeric_limits<double>::lowest()),
      time_last_boost(0.0),
      decay_rate(ve_params["neut_decay"]),
      time_isolated(std::nan("7")),
      isCovidNaive(true),
      isVaccinated(false),
      vaccinations(vaccination_in),
      number_infections(num_infections),
      time_past_infection(time_of_past_infection)
{}


Individual::Individual(double &age_in, std::vector<double> &age_brackets_in, std::vector<std::pair<double, VaccineType>> &vaccination_in, nlohmann::json &ve_params, size_t &num_infections, double &time_of_past_infection, double &log10_neuts, bool &nocovid, bool &isvaxxed)
    : covid('S'),
      age(age_in),
      age_bracket(age_sort(age_in, age_brackets_in)),
      secondary_infections(0),
      log10_neutralising_antibodies(log10_neuts),
      old_log10_neutralising_antibodies(log10_neuts),
      time_last_boost(0.0),
      decay_rate(ve_params["neut_decay"]),
      time_isolated(std::nan("7")),
      isCovidNaive(nocovid),
      isVaccinated(isvaxxed),
      vaccinations(vaccination_in),
      number_infections(num_infections),
      time_past_infection(time_of_past_infection)
{}


std::ostream &operator<<(std::ostream &os, const Individual &person)
{
  os << person.age << ", " << person.age_bracket << ", " << person.covid.infection_status << ", " << person.log10_neutralising_antibodies << ", " << person.old_log10_neutralising_antibodies << ", " << person.time_last_boost;
  return os;
}

std::ostream &operator<<(std::ostream &os, const Disease &covid)
{
  os << covid.log10_neuts_at_exposure << ", " << covid.asymptomatic << ", " << covid.time_of_symptom_onset;
  return os;
}

std::ostream &operator<<(std::ostream &os, const VaccineType &vaccine)
{
  std::string output;
  switch (vaccine)
  {
  case VaccineType::AZ1:
    output = "AZ dose 1";
    break;
  case VaccineType::AZ2:
    output = "AZ dose 2";
    break;
  case VaccineType::Pfizer1:
    output = "Pfizer dose 1";
    break;
  case VaccineType::Pfizer2:
    output = "Pfizer dose 2";
    break;
  case VaccineType::Moderna1:
    output = "Moderna dose 1";
    break;
  case VaccineType::Moderna2:
    output = "Moderna dose 2";
    break;
  case VaccineType::Booster:
    output = "mRNA booster";
    break;
    case VaccineType::Unvaccinated :
    output = "Unvaccinated";
    break;
    default:
    throw std::logic_error("Unrecognised VaccineType. \n");
  }
  os << output;
  return os;
}