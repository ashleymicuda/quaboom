#!/usr/bin/env python

import unittest
# Code to import Person.py from parent directory
import os, sys
sys.path.append("../")
import Population

class TestPerson(unittest.TestCase):
    
    def setUp(self):       # Code that will be run before every test function is executed
        pass
    
    def tearDown(self):    # Code that will be run after every test function is executed
        pass
    
    def test_init(self):
        nPop, n0 = 1000, 20
        pop = Population.Population(nPop=nPop, n0=n0)
        
        # Make sure that there are n0 infected, 0 recovered, nPop-n0 susceptible
        self.assertEqual(pop.count_infected(), n0)
        self.assertEqual(pop.count_recovered(), 0)
        self.assertEqual(pop.count_susceptible(), nPop-n0)
        
        pass

    def test_globals(self): 
        
        # Make sure weights and options line up
        self.assertEqual(len(Population.AGE_OPTIONS), len(Population.AGE_WEIGHTS))
        self.assertEqual(len(Population.JOB_OPTIONS), len(Population.JOB_WEIGHTS))
        self.assertEqual(len(Population.HOUSE_OPTIONS), len(Population.HOUSE_WEIGHTS))
        self.assertEqual(len(Population.ISOLATION_OPTIONS), len(Population.ISOLATION_WEIGHTS))
        
        # Make sure probabilities sum to 1
        roundLevel = 6 # Decimal digits to round 
        self.assertEqual(round(sum(Population.AGE_WEIGHTS), roundLevel), 1)
        self.assertEqual(round(sum(Population.JOB_WEIGHTS), roundLevel), 1)
        self.assertEqual(round(sum(Population.HOUSE_WEIGHTS), roundLevel), 1)
        self.assertEqual(round(sum(Population.ISOLATION_WEIGHTS), roundLevel), 1)
        
if __name__ == '__main__':
    unittest.main()
    