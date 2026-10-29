#Classe que vai ajudar a controlar um algoritimo com varios criterios de paradas

class Termination:
    
    def __init__(self):
        self.forceTermination = False
        self.percentage = 0.0

    def has_Terminated(self):
        return self.forceTermination or self.percentage >= 1.0
    
    def reset(self):
        pass

    def update_progress(self, algorithm):
        if self.forceTermination:
            self.percentage = 1.0
        else:
            self.percentage = self.compute_progress(algorithm)
            #Throw Exception
            assert self.percentage >=0, "Invalid progress was set by the termination criteria"
            
        return self.percentage
    
    def has_terminated(self):
        return self.percentage >= 1.00
    
    def terminate(self):
        self.forceTermination = True
        
    def compute_progress(self,algorithm):
        pass