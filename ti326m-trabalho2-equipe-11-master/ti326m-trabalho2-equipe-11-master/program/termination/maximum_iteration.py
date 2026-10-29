from core.termination import Termination

class MaximumIteration(Termination):
    def __init__(self, max_generations):
        super().__init__() # Inicializa a classe base (forceTermination e percentage)
        self.max_generations = max_generations
        self.current_generation = 0
    
    def reset(self):
        self.current_generation = 0
        self.percentage = 0.0
        self.forceTermination = False
    
    def compute_progress(self, algorithm):
        self.current_generation += 1
        
        print(f"Geração {self.current_generation}/{self.max_generations} | Melhor Custo: {algorithm.best_solution.cost}")
        
        progresso = self.current_generation / self.max_generations
        
        return progresso