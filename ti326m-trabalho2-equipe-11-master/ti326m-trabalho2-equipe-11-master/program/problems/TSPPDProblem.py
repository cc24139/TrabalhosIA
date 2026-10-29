from core.problem import Problem
import math
from services.city import City

class TravelingSalesmanPickupAndDelivery(Problem):
    def __init__(self,distances,nCities,pickupDeliveries=None):
        self.distances = distances #Matrix of adjacency of the citys
        #dictionary of routes (a,b) where a is the pickup and b is the delivery, or vice versa, depending on the city type)
        #Example: routes[0] = [0,5] and routes[5] = [0,5] means that city 0 is a pickup and city 5 is a delivery, and they are paired
        self.pickupDeliveries = pickupDeliveries 
        self.nCities = nCities # number of cities
        
    def evaluate(self, tour):

        if not self.avaliation(tour):
            return float('inf')

        n = len(tour)

        return sum(
            self.distances[tour[i]][tour[(i + 1) % n]]
            for i in range(n)
        )
    
    def avaliation(self, tour):

        pos = {
            city: idx
            for idx, city in enumerate(tour)
        }

        checked = set()

        for city, (pickup, delivery) in self.pickupDeliveries.items():

            if (pickup, delivery) in checked:
                continue

            checked.add((pickup, delivery))

            if pos[pickup] > pos[delivery]:
                return False

        return True

    # to see if its a valid relocate
    def is_valid_relocate(self, route, i, j):
        city = route[i]

        if city == 0:
            return False

        pickup, delivery = self.pickupDeliveries[city]

        pos = {c: idx for idx, c in enumerate(route)}

        new_pos = j

        if city == pickup:
            return new_pos < pos[delivery]

        else:
            return pos[pickup] < new_pos


    # to calculate a cost change without calculating the whole thing
    def relocate_delta_cost(self, route, current_cost, i, j):

        n = len(route)

        # movimentos inúteis
        if i == j or i + 1 == j:
            return current_cost

        city = route[i]

        # vizinhos da remoção
        prev_i = route[i - 1]
        next_i = route[(i + 1) % n]

        delta = 0

        # REMOVE city
        delta -= self.distances[prev_i][city]
        delta -= self.distances[city][next_i]
        delta += self.distances[prev_i][next_i]

        # rota sem city
        temp = route[:]
        temp.pop(i)

        # ajusta posição de inserção
        if j > i:
            j -= 1

        # vizinhos da inserção
        prev_j = temp[j - 1]
        next_j = temp[j]

        # INSERT city
        delta -= self.distances[prev_j][next_j]
        delta += self.distances[prev_j][city]
        delta += self.distances[city][next_j]

        return current_cost + delta


    @property   
    def size(self):
        return self.nCities
    



