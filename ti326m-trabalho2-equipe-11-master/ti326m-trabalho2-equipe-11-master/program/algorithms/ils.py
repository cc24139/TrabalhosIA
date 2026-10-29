
from core.algorithm import Algorithm
from core.solution import Solution

import math
import random

class IteratedLocalSearch(Algorithm):

  def __init__(self, termination, problem, verbose=False):
    
    super().__init__(termination, problem, verbose)
    
    self.best_solution = None

    self._got_local_optimal_solution = False

  
  def initialize(self):
    self.nIteration = 0
    self.termination.reset()
    if self.verbose:
      print("Iterated Local Search(ILS) algorithm initialized.")
    self.intial_solution = self._get_initial_solution()
    self.current_solution = self.intial_solution.copy()
    self.best_solution = self.intial_solution.copy()
  

  def advance(self): 
    if self.verbose:
      print(f"{self.nIteration}nth iteration: ILS advancing")
    
    neighbor = self._get_neighbors()
    #print(f'N cost: {neighbor.cost}')
    #print(f'C cost: {self.current_solution.cost}')
    if neighbor.cost == self.current_solution.cost:
      if self.verbose:
        print("Pertub called")
      perturbed_solution = self._perturb()
      
      if perturbed_solution.cost != self.current_solution.cost:
        self.current_solution = perturbed_solution
      return

    self.current_solution = neighbor;
    if self.verbose:
      print(f"Current solution changed. New cost: {self.current_solution.cost}")

    if self.best_solution.cost > self.current_solution.cost:
      self.best_solution = self.current_solution
      if self.verbose:
        print("Best solution changed")


  def finalize(self):
    if self.verbose:
      print(f"Finalizing ILS algorithm. Iterations: {self.nIteration}")
    return super().finalize()


  def _get_initial_solution(self):
    
    initial_solution = Solution(
      value = random.sample(list(range(self.problem.size)), self.problem.size)
    )
    initial_solution.cost = self.problem.evaluate(initial_solution.value)

    return initial_solution
  

  def _get_neighbors(self, current_solution):
    pass
    i, j = random.sample(list(range(self.problem.size)), k=2)
    neighbors = current_solution.copy()
    neighbors.value[i], neighbors.value[j] = neighbors.value[j], neighbors.value[i]
    neighbors.cost = self.problem.evaluate(neighbors.value)
    return neighbors
  

  # method to get a solution away from the local optimal solution
  def _perturb(self, current_solution):
    pass
