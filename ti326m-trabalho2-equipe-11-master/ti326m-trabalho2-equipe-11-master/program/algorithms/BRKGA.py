import random
from core.algorithm import Algorithm
from core.solution import Solution
import time
class BRKGA(Algorithm):
    def __init__(self, termination, problem, p, pe, pm, rhoe, verbose=False):
        """
        p: Tamanho da população
        pe: Número de indivíduos na elite
        pm: Número de mutantes (imigrantes) por geração
        rhoe: Probabilidade de herdar a chave do pai elite no crossover
        """
        super().__init__(termination, problem, verbose)
        self.p = p
        self.pe = pe
        self.pm = pm
        self.rhoe = rhoe
        self.population = []
        self.best_solution = None

    def initialize(self):
        """Gera a população inicial com chaves aleatórias."""
        self.population = []
        self.startTime = time.time()  # Marca o início do tempo de execução
        self.nIteration = 0
        self.termination.reset()
        #self.termination.update_progress(self)  # Atualiza o progresso inicial (0%)
        # O tamanho do cromossomo é n_total - 1 (pois o depósito '1' é fixo no início)
        n_chaves = self.problem.size - 1 
        
        for _ in range(self.p):
            keys = [random.random() for _ in range(n_chaves)]
            cost = self._decode_and_evaluate(keys)
            self.population.append(Solution(keys, cost))
        
        self._sort_population()
        self.best_solution = self.population[0].copy()

    def advance(self):
        """Executa uma geração do BRKGA."""
        n_chaves = self.problem.size - 1
        next_population = []

        # 1. Elitismo: Copia os melhores indivíduos
        for i in range(self.pe):
            next_population.append(self.population[i].copy())

        # 2. Mutantes: Insere novos indivíduos aleatórios
        for _ in range(self.pm):
            keys = [random.random() for _ in range(n_chaves)]
            cost = self._decode_and_evaluate(keys)
            next_population.append(Solution(keys, cost))

        # 3. Crossover Enviesado
        n_crossover = self.p - self.pe - self.pm
        for _ in range(n_crossover):
            parent_elite = random.choice(self.population[:self.pe])
            parent_any = random.choice(self.population)
            
            child_keys = []
            for j in range(n_chaves):
                if random.random() < self.rhoe:
                    child_keys.append(parent_elite.value[j])
                else:
                    child_keys.append(parent_any.value[j])
            
            cost = self._decode_and_evaluate(child_keys)
            next_population.append(Solution(child_keys, cost))

        self.population = next_population
        self._sort_population()

        if self.population[0].cost < self.best_solution.cost:
            self.best_solution = self.population[0].copy()

    def _decode_and_evaluate(self, keys):
        n_total = self.problem.size
        
        # 1. Mapeia cada chave ao seu respectivo nó (clientes de 1 até n_total-1)
        # O gene keys[0] SEMPRE pertence ao nó 1, keys[1] ao nó 2, etc.
        chaves_nos = {}
        for i in range(n_total - 1):
            no_cliente = i + 1 
            chaves_nos[no_cliente] = keys[i]
            
        # 2. Força a Restrição de Precedência matematicamente
        for no_cliente in range(1, n_total):
            coleta, entrega = self.problem.pickupDeliveries[no_cliente]
            
            # Se eu estou olhando para uma coleta...
            if no_cliente == coleta:
                # E se a chave da entrega for menor ou igual a da coleta (o que geraria erro)...
                if chaves_nos[entrega] <= chaves_nos[coleta]:
                    # Eu empurro o valor da chave da entrega para ficar logo após a coleta!
                    chaves_nos[entrega] = chaves_nos[coleta] + 0.000001
                    
        # 3. Agora simplesmente ordenamos os nós baseados nas chaves ajustadas
        clientes_ordenados = sorted(chaves_nos.keys(), key=lambda n: chaves_nos[n])
        
        # 4. Adiciona o depósito (0) no início e avalia
        tour = [0] + clientes_ordenados
        return self.problem.evaluate(tour)

    def _sort_population(self):
        """Ordena a população do menor custo para o maior."""
        self.population.sort(key=lambda sol: sol.cost)