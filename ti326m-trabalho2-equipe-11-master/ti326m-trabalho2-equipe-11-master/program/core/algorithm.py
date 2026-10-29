import time
#Todo o algoritmo que a busca deve conter no minimo
#Classe base
class Algorithm:
    def __init__(self,termination,problem,verbose=False):
        #Criterio de parada da busca
        self.termination = termination
        #Problema a ser resolvido
        self.problem = problem
        #Nivel de detalhamento das informacoes
        self.verbose = verbose
        #Num atual de interacoes:
        self.nIteration = 0
        #Tempo que o algoritimo foi iniciado pela primeira vez
        self.startTime = None
        
    def run(self):
        self.initialize()
        self.startTime = time.time()
        while not self.termination.has_Terminated():
            self.advance()
            self.termination.update_progress(self);
        self.finalize()

    def initialize(self):
        pass
    
    def advance(self):
        pass
    
    def finalize(self):
        pass
    