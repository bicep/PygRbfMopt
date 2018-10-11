import pygmo as pg
import os as os
import rbfopt as rbfopt
from collections import deque
from utils.pygmo_utils import calculate_weighted_objective


class Rbfmopt():

  # So the settings tell us how many function evaluations to do, and the problem is instantiated together with the
  # algorithm
  def __init__(self, settings, problem):
      #Augmented Tchebycheff stuff
      self.rho = 0.05
      # let's set this later
      self.seed = 33
      self.settings = settings
      self.max_fevals = self.settings.max_evaluations
      # The problem is straightaway a blackbox
      self.problem = problem

  def optimize(self):
    
    n = self.problem.get_n_obj()
    all_weights = deque(pg.decomposition_weights(n_f = self.problem.get_n_obj(), n_w = self.max_fevals, method = "low discrepancy", seed = self.seed).tolist())

    #Initialize the fitness list
    f_list = []

    #loop this part for cycles
    while(len(f_list) < self.max_fevals):

        # Update the weights
        current_weights = all_weights.popleft()
        # Set the updated weights for the problem as well
        self.problem.set_current_weights(current_weights)

        print('Weights: {}'.format(current_weights ))   
        
        #Set cycle number to refinement frequency to allow one refinement phase
        self.settings.max_cycles = self.settings.refinement_frequency

        #Calculate values from objectives with sobol weights
        if len(f_list) > 0:
            # If we have done this before, then we use the new current_weights to calculate the
            # weighted objectives of the past fitness values
            weighted_objs = [calculate_weighted_objective(current_weights, fitnessValue, self.rho) for fitnessValue in f_list]
            print('Weighted objectives: {}'.format(weighted_objs)) 
        
            alg = rbfopt.RbfoptAlgorithm(self.settings, self.problem, self.problem.get_x_list(), weighted_objs, False)
        else:
            alg = rbfopt.RbfoptAlgorithm(self.settings, self.problem)
            
        alg.optimize()

        #Replace the old f list with the new f list
        f_list = self.problem.get_f_list()
    
  def get_f_list(self):
    return self.problem.get_f_list()

  def get_x_list(self):
    return self.problem.get_x_list()
