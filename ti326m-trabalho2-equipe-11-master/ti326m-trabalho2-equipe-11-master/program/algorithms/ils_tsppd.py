from random import random
import random
from algorithms.ils import IteratedLocalSearch
from core.solution import Solution

"""
Class with the functions that are specific to ILS for the TSP
"""
class IteratedLocalSearchForTSPPD(IteratedLocalSearch):

  def _get_initial_solution(self):
    n_cities = self.problem.size
    
    tour = [0] 
    unvisited = set(range(1, n_cities)) # ignore the first one
    
    deliveries = set() # all deliveries
    if self.problem.pickupDeliveries:
      for city, (pickup, delivery) in self.problem.pickupDeliveries.items():
        deliveries.add(delivery)
        
    while unvisited:
      valid_candidates = []
      
      for city in unvisited:
        if city not in deliveries:
          valid_candidates.append(city)
        else:
          pickup, delivery = self.problem.pickupDeliveries[city]
          if pickup in tour:
            valid_candidates.append(city)
      
      # now, the valid_candidates set only has nodes that can be the next
      next_city = random.choice(valid_candidates)
      tour.append(next_city)
      unvisited.remove(next_city)
        
    initial_solution = Solution(value=tour)
    initial_solution.cost = self.problem.evaluate(tour)
    
    return initial_solution

  
  def __get_neighbors_by_relocate(self):

    route = self.current_solution.value
    current_cost = self.current_solution.cost

    n = len(route)

    for i in range(1, n):

      for j in range(1, n):

          if i == j or i + 1 == j:
            continue

          self.nIteration += 1

          if not self.problem.is_valid_relocate(route, i, j):
            continue

          new_cost = self.problem.relocate_delta_cost(
              route,
              current_cost,
              i,
              j
          )

          # cria rota REAL exatamente igual ao delta
          new_route = route[:]

          city = new_route.pop(i)

          if j > i:
            j -= 1

          new_route.insert(j, city)

          # DEBUG
          real_cost = self.problem.evaluate(new_route)

          assert abs(real_cost - new_cost) < 1e-6, (
              f"\nDELTA ERROR\n"
              f"i={i}, j={j}\n"
              f"Incremental={new_cost}\n"
              f"Real={real_cost}\n"
              f"Current={current_cost}\n"
              f"Old route={route}\n"
              f"New route={new_route}"
          )

          if real_cost < current_cost:

            neighbor = self.current_solution.copy()
            neighbor.value = new_route
            neighbor.cost = real_cost

            return neighbor

    return self.current_solution


  def _get_neighbors(self):
    return self.__get_neighbors_by_relocate()
    #return self.__get_neighbors_by_2opt()
  

  def _perturb(self):

    route = self.current_solution.value[:]

    pairs = list(set(
        tuple(v)
        for v in self.problem.pickupDeliveries.values()
    ))

    if not pairs:
        return self.current_solution

    n_pairs = len(pairs)

    k = max(2, int(n_pairs * 0.25))

    selected_pairs = random.sample(
        pairs,
        min(k, n_pairs)
    )

    removed = []

    for pickup, delivery in selected_pairs:

        if pickup in route:
            route.remove(pickup)

        if delivery in route:
            route.remove(delivery)

        removed.append((pickup, delivery))

    for pickup, delivery in removed:

        insert_pickup = random.randint(
            1,
            len(route)
        )

        route.insert(insert_pickup, pickup)

        insert_delivery = random.randint(
            insert_pickup + 1,
            len(route)
        )

        route.insert(insert_delivery, delivery)

    perturbed = self.current_solution.copy()

    perturbed.value = route
    perturbed.cost = self.problem.evaluate(route)

    self.nIteration += 1

    return perturbed
  