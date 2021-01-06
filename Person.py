import numpy as np
import json

TIME_QUARANTINE = 14 #days people have to quarantine

# How long the infection will last
json_file = open('dataK.json')
disease_params = json.load(json_file)

# recovery
MIN_MILD= disease_params['recovery'][0]['MIN_MILD']
MAX_MILD= disease_params['recovery'][0]['MAX_MILD']
MIN_SEVERE= disease_params['recovery'][0]['MIN_SEVERE']
MAX_SEVERE= disease_params['recovery'][0]['MAX_SEVERE']
MIN_ICU= disease_params['recovery'][0]['MIN_ICU']
MAX_ICU= disease_params['recovery'][0]['MAX_ICU']
MIN_DIE= disease_params['recovery'][0]['MIN_DIE']
MAX_DIE= disease_params['recovery'][0]['MAX_DIE']


json_file.close()

class Person(object):

    # Initalize a person - Can set properties but only needed one is index
    def __init__(self, index, infected=False, recovered=False, dead=False, quarantined=False, quarantined_day=None, infected_day=None, 
                 recovered_day=None, death_day=None, others_infected=None, cure_days=None, 
                 recent_infections=None,age=None,job=None,house_index=0,isolation_tendencies=None,case_severity=None):

        self.infected = infected
        self.recovered = recovered
        self.dead = dead
        self.quarantined = quarantined
        self.quarantined_day = quarantined_day
        self.infected_day = infected_day
        self.recovered_day = recovered_day
        self.death_day = death_day
        self.others_infected = [] if others_infected is None else others_infected
        self.cure_days = cure_days
        self.recent_infections = recent_infections
        self.index = index
        self.age = age
        self.job = job
        self.household = house_index
        self.isolation_tendencies = isolation_tendencies
        self.case_severity = case_severity
    # Return True if infected, False if not
    def is_infected(self):
        return self.infected

    # Return True if recovered, False if not
    def is_recovered(self):
        return self.recovered
    
    #return True if dead, False if not
    def is_dead(self):
        return self.dead
    
    #return True if quarantined, False if not
    def is_quarantined(self):
        return self.quarantined
    
    def get_quarantine_day(self):
        return self.quarantined_day
    
    # Return index of person
    def get_index(self):
        return self.index

    # Return list of others infected
    def get_others_infected(self):
        return self.others_infected

    # Get list of recent infections (from the last time they infected people)
    def get_recent_infections(self):
        return self.recent_infections
    
    def get_case_severity(self):
        return self.case_severity

    # Method to infect a person
    def infect(self, day, cure_days=None):

        # Check that they are suseptable (maybe should have that as property?)
        if not self.recovered and not self.infected and not self.dead:
            self.infected = True
            self.infected_day = day
            # If cure days not specified then choose random number inbetween min and max
            if self.case_severity == 'Mild' or self.case_severity == None: # If severity not specified, choose Mild
                self.cure_days = np.random.randint(MIN_MILD, MAX_MILD) if cure_days is None else cure_days
            elif self.case_severity == 'Hospitalization':
                self.cure_days = np.random.randint(MIN_SEVERE, MAX_SEVERE) if cure_days is None else cure_days
            elif self.case_severity == 'ICU':
                self.cure_days = np.random.randint(MIN_ICU, MAX_ICU) if cure_days is None else cure_days
            elif self.case_severity == 'Death':
                self.cure_days = np.random.randint(MIN_DIE, MAX_DIE) if cure_days is None else cure_days

            return True

        return False

    # check if someone is quarantined, and if they can come out
    # (if they've quarantined for 14 days)
    def check_quarantine(self, day):
        if self.quarantined:
            days_since_quarantined = day - self.quarantined_day
            if days_since_quarantined >= TIME_QUARANTINE:
                self.quarantined = False
                
                return False
            return True
        
        else: # if not self quarantined
            # if they aren't in quarantine, check if they know they're infected
            ##   then put them into quarantine
            if self.case_severity != "Mild":
                # if their symtoms are not mild, quarantine if they're infected
                # assume people in the hospital aren't spreading it either
                self.quarantined_day = day
                self.quarantined = True
                
                return True
            return False
    
    # Method that checks if a person is past their cure time and will cure them
    # Returns True if they were cured, False if not
    def check_cured(self, day):

        if self.infected and not self.recovered:

            days_since_infected = day - self.infected_day
            # Checks cure timeline
            if days_since_infected >= self.cure_days:
                # Resets values to cure them
                self.infected = False
                self.recovered = True
                self.recovered_day = day

                return True
        return False
    
    def check_dead(self, day): # checking that case_severity==death outside of the loop

        if self.infected:

            days_since_infected = day - self.infected_day
            # Checks death timeline
            if days_since_infected >= self.cure_days:
                self.infected = False
                self.dead = True
                self.death_day = day

                return True
        return False

    # Method to infect a random subset of the susceptable population. Returns how many people infected
    def infect_others(self, pop_list, suscept_pop, day, num_to_infect=1):

        # If there are no susceptable people, return 0 infections
        if len(suscept_pop) == 0:
            return 0

        # Choose the random indices from the population to have infectious contacts with
        contact_options = list(range(len(pop_list)))
        contact_options.remove(self.index)       # Make it so that it can not select itself as a contact
        infect_indexs = np.random.choice(contact_options, num_to_infect, replace=False)
        self.recent_infections = []
        infectCount = 0
        for index in infect_indexs:
            # If the contact was not susceptable, nothing happens
            if index not in suscept_pop:
                continue

            # Get the id of the susceptable person being infected
            person_to_infect = pop_list[index]
            person_index = person_to_infect.get_index()

            # Infect that person
            person_to_infect.infect(day)

            # Update others infected list
            self.others_infected.append(person_index)
            # Update who was actually infected
            self.recent_infections.append(person_index)

        return len(self.recent_infections)


