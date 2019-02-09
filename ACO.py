# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:36:48 2018
@author: Victor O. Costa
Implementation of the Ant Colony for Continuous Domains method from Socha, 2008.
"""

import numpy as np
from scipy.stats import norm
import Functions
class ACO:
    """ Class containing the Ant Colony Optimization for Continuous Domains """

    def __init__(self):
        """ Constructor """
        self.verbosity = True
        
        # Initial algorithm parameters
        self.max_iter = 100                             
        self.pop_size = 5                               
        self.k = 50                                    
        self.q = 0.1                                   
        self.xi = 0.85                                  
        
        # Initial (NULL) problem definition
        self.num_var = 2                                
        self.var_ranges = [[0, 1],
                           [0, 1]]                      
        self.cost_function = None                       
        
        # Optimization results
        self.SA = None                                  
        self.best_solution = None                       
    # end def
            
            
    def variables(self, nvar, ranges):
        
        if len(ranges) != nvar:
            print "Error, number of variables and ranges does not match"
        else:
            self.num_var = nvar
            self.var_ranges = ranges
            self.SA = np.zeros((self.k, self.num_var))
    # end def
            
            
    def cost(self, costf):
        
        self.cost_function = costf
    # end def
    
    
    def parameters(self, max_iter, pop_size, k, q, xi):
        """ Sets the parameters of the algorithm """
        self.max_iter = max_iter
        self.pop_size = pop_size
        self.k = k
        self.q = q
        self.xi = xi
    # end def
    
    
    def verbosity(self, status):
        """ If status is True, will print partial results during the search """
        if type(status) is bool:
            self.verbosity = status
        else:
            print "Error, received verbosity parameter is not boolean"
    # end def
    
    
    def _biased_selection(self, probabilities):
        """ Returns an index based on a set of probabilities (also known as roulette wheel selection in GA) """
        r = np.random.uniform(0, sum(probabilities))
        for i, f in enumerate(probabilities):
            r -= f
            if r <= 0:
                return i
    # end def
         
         
    def optimize(self):
        """ Initializes the archive and enter the main loop, until it reaches maximum number of iterations """
        
        if self.num_var == 0:
            print "Error, first set the number of variables and their boundaries"
        elif self.cost_function == None:
            print "Error, first define the cost function to be used"
        else:
            
            if self.verbosity:   print "Initialization to the achrive"
            # Initialize the archive by random sampling, respecting each variable's constraints
            pop = np.zeros((self.pop_size, self.num_var))
            w = np.zeros(self.k)
            
            for i in xrange(self.k):
                for j in xrange(self.num_var): 
                    self.SA[i, j] = np.random.uniform(self.var_ranges[j][0], self.var_ranges[j][1])        # Initialize solution archive randomly
                self.SA[i, -1] = self.cost_function(self.SA[i, 0:self.num_var])                            # Get initial cost for each solution
            self.SA = self.SA[self.SA[:, -1].argsort()]                                                    # Sort solution archive (best solutions first
            
            x = np.linspace(1,self.k,self.k) 
            w = norm.pdf(x,1,self.q*self.k)                                 # Weights as a gaussian function of rank with mean 1, std qk
            p = w/sum(w)                                                    # Probabilities of selecting solutions as search guides
            
            if self.verbosity:   print "Algo for main loop"
            
            # Algorithm runs until it reaches maximum number of iterations
            for iteration in xrange(self.max_iter):
                if self.verbosity:
                    print "[%d]" % iteration
                    print self.SA[0, :]
                
                Mi = self.SA[:, 0:self.num_var]                                                                     # Matrix of means
                for ant in xrange(self.pop_size):                                                                   # For each ant in the population
                    l = self._biased_selection(p)                                                                   # Select solution of the SA to sample from based on probabilities p
                    
                    for var in xrange(self.num_var):                                                                # Calculate the standard deviation of all variables from solution l
                        sigma_sum = 0
                        for i in xrange(self.k):
                            sigma_sum += abs(self.SA[i, var] - self.SA[l, var])
                        sigma = self.xi * (sigma_sum/(self.k - 1))
                         
                        pop[ant, var] = np.random.normal(Mi[l, var], sigma)                                         # Sample from normal distribution with mean Mi and st. dev. sigma
                        
                        # Deals with search space violation using the random position strategy
                        if pop[ant, var] < self.var_ranges[var][0] or pop[ant, var] > self.var_ranges[var][1]:                   
                            pop[ant, var] = np.random.uniform(self.var_ranges[var][0], self.var_ranges[var][1])
                            
                    pop[ant, -1] = self.cost_function(pop[ant, 0:self.num_var])                                     # Evaluate cost of new solution
                
                self.SA = np.append(self.SA, pop, axis = 0)                                                         # Append new solutions to the Archive
                self.SA = self.SA[self.SA[:, -1].argsort()]                                                         # Sort solution archive according to the fitness of each solution
                self.SA = self.SA[0:self.k, :]                                                                      # Remove worst solutions
            
            self.best_solution = self.SA[0, :]
            #sol=Functions.Sphere(self.best_solution)
            #print "cost"
            #print sol
            return self.best_solution  
    # end def
    
# end class 