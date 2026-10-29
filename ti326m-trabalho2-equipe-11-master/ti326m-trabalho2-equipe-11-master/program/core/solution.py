class Solution:
    def __init__(self,value,cost = 0):
        self.value = value
        self.cost = cost
        
    @property
    def size(self):
        return len(self.value)
    
    def copy(self):
        return self.__class__(self.value.copy(), self.cost)