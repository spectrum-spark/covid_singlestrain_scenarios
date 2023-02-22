

# Class for individuals that keeps track of their vaccination date(s) and infection date if relevant

class Individual:
    def __init__(self, age_band, max_vax,infected,next_vax_eligibility_date=10000):
        self.age_band = age_band
        self.max_vax = max_vax
        self.doses_received = 0
        self.next_vax_eligibility_date = next_vax_eligibility_date
        self.infected = infected # true or false
        self.infected_day = -1
        self.vaccination_days = [] # days on which this individual gets vaccinated 
