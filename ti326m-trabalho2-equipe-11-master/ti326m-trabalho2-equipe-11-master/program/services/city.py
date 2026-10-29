import math
class City:
    def __init__(self, id, x, y,pickpupDelivery=None, pair=None):
        self.id = id
        self.x = x
        self.y = y
        self.pickupDelivery = pickpupDelivery #0 for pickup, 1 for delivery
        self.pair = pair #id of the pair city (pickup or delivery)
    
    def calculateDistance(self, otherCity):
        return round(math.sqrt((self.x - otherCity.x) ** 2 + (self.y - otherCity.y) ** 2), 2)