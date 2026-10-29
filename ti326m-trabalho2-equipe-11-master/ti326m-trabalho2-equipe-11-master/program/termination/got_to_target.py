from core.termination import Termination

class GotToTarget(Termination):
    def __init__(self, target):
        super().__init__() # Inicializa a classe base (forceTermination e percentage)
        self.target = target
        self.progress = 0
        self.initial_distance = 0
    
    def __init__(self, target):

        super().__init__()

        self.target = target

    def reset(self):

        self.forceTermination = False
        self.percentage = 0.0

    def compute_progress(self, algorithm):

        best_cost = algorithm.best_solution.cost

        # chegou no target
        if best_cost <= self.target:
            self.forceTermination = True
            self.percentage = 1.0

            return 1.0


        # progresso meramente informativo
        progress = self.target / best_cost

        # evita valores absurdos
        progress = max(0.0, min(progress, 0.999999))

        print(
            f"Progress: {self.percentage * 100:.2f}% "
            f"| Best Cost: {algorithm.best_solution.cost:.2f}"
        )
        return progress
    