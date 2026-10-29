instancesDir = "./program/instances/"
from  problems.TSPPDProblem import TravelingSalesmanPickupAndDelivery, City
from termination.maximum_iteration import MaximumIteration
from termination.got_to_target import GotToTarget
from services.tttGraph import TTTGraph, Instancie
import time
from algorithms.BRKGA import BRKGA
from algorithms.ils_tsppd import IteratedLocalSearchForTSPPD

cities = []
instanceNames = {
        0: ["pdtsp-n105", 6019],#6019
        1: ["pdtsp-n171", 10203],
        2: ["pdtsp-n213", 7314],
        3: ["pdtsp-n289", 14447],
        4: ["pdtsp-n317", 9901],
        5: ["pdtsp-n335", 16002],
        6: ["pdtsp-n401", 13399],
        7: ["pdtsp-n459", 12350],
        8: ["pdtsp-n547", 20126],
        9: ["pdtsp-n599", 21017],
    }
def readInstancies(pathInstance):
        arq = open(instancesDir + pathInstance, "r")
        distances = []
        routes = {}
        cities = [] 
        numLines = int(arq.readline())
        line = arq.readline()
        depoitCity = City(
            id = int(line[0:7].strip())-1,
            x = float(line[6:16].strip()),
            y = float(line[16:26].strip()),
            pair= int(line[0:7].strip())-1
        )
        cities.append(depoitCity)
        routes[depoitCity.id] = [depoitCity.id, depoitCity.id]
        while ((line := arq.readline()) != "-999"):
            print(line)
            atualCity = City(
                id = int(line[0:6].strip())-1,
                x = float(line[6:15].strip()),
                y = float(line[16:25].strip()),
                pickpupDelivery=int(line[26:32].strip()),
                pair=int(line[32:39].strip()) -1
            )
            cities.append(atualCity)
        for city in cities:
            distances.append([city.calculateDistance(otherCity) for otherCity in cities])
            if city.id == 0:
                 continue
            
            if city.pickupDelivery == 0:
                routes[city.id] = [city.id, city.pair]
            else:
                routes[city.id] = [city.pair, city.id]
        return TravelingSalesmanPickupAndDelivery(distances, numLines, routes)
    

# Além de um seletor para qual algoritmo e para qual instância, precisa também de um para 
# escolher o modo de término
def chooseInstance():
    option = -1
    while option < 0 or option > 10:
        print("Choose which instance you want")
        for key, value in instanceNames.items():
            print(f"{key+1} - {value[0]} with target value {value[1]}")
        print("0 - Go back")
        print("Any number between 1 and 10: an instance")
        option = int(input("Type your option: "))
    return option


def runBRKGA():
     #parametros BRKGA
    n_pop = 2000
    n_elite = int(n_pop * 0.20)
    n_mutant = int(n_pop * 0.10)
    rho_elite = 0.7
    instanciaNumber = chooseInstance()-1
    if(instanciaNumber == -1):
        return
    termino = MaximumIteration(200)
    print("Running BRKGA on instance: ", instanceNames[instanciaNumber][1]*1.45)
    problema = readInstancies(instanceNames[instanciaNumber][0])
    algorithm = BRKGA(
        termination=termino,
        problem=problema,
        p=n_pop,
        pe=n_elite,
        pm=n_mutant,
        rhoe=rho_elite,
        verbose=False
        )
    iteracoes = []
    for i in range(5):
            algorithm.run()
            finalTime = time.time() - algorithm.startTime
            iteracoes.append(Instancie(instanceNames[instanciaNumber][0], algorithm.nIteration, finalTime, algorithm.best_solution.cost))
            print(f"Iteration {i+1} - Time: {finalTime:.2f} seconds - Cost: {iteracoes[-1].value}")
    tttGraph = TTTGraph(iteracoes, algorithm, lambda x: x <= instanceNames[instanciaNumber][1]*1.45,instanceNames[instanciaNumber][1]*1.45,"BRKGA")
    iteracoes.sort(key=lambda x: x.value)
    helpFunc = lambda x: x <= iteracoes[-1].value
    tttGraph.plotTime(save=True,nameFile=f"BRKGA_{instanceNames[instanciaNumber][0]}_time.png",helpFunc=helpFunc)
   
        


def runILS(instanceNum, maxIteration):
    termination = MaximumIteration(maxIteration)
    problem = readInstancies(instanceNames[instanceNum][0])
    algorithm = IteratedLocalSearchForTSPPD(
        termination=termination,
        problem=problem,
        verbose=False
        )
    instances = []
    for i in range(5):
        algorithm.run()
        finalTime = time.time() - algorithm.startTime
        instances.append(Instancie(instanceNames[instanceNum][0], algorithm.nIteration, finalTime, algorithm.best_solution.cost))
    instances.sort(key=lambda x: x.value)
    helpFunc = lambda x: x <= instances[-1].value
    tttGraph = TTTGraph(instances, algorithm, lambda x: x <= instanceNames[instanceNum][1]*1.45, instanceNames[instanceNum][1]*1.45, "ILS")
    tttGraph.plotTime(save=True,nameFile=f"ILS_{instanceNames[instanceNum][0]}_time.png",helpFunc=helpFunc)
   
    


def prepareILS():
    instanceNumber = chooseInstance()
    if instanceNumber == 0:
        return
    runILS(instanceNumber-1, 1200)


def main():
    option = -1
    while option < 0 or option > 3:
        print("Option selector")
        print("0 - End program")
        print("1 - Run BRKGA")
        print("2 - Run ILS")
        print("3 - Compare Algorithms")
        option = int(input("Choose your option: "))
        match(option):
            case 0: print("Program exited.")
            case 1: runBRKGA()
            case 2: prepareILS()
            case 3: compareAlgorithms()
            case _: continue

def compareAlgorithms():
    numInstances = chooseInstance()-1
    #parameter BRKGA
    n_pop = 400
    n_elite = int(n_pop * 0.20)
    n_mutant = int(n_pop * 0.10)
    rho_elite = 0.7
    max_geracoes = 2000
    problem = readInstancies(instanceNames[numInstances][0])
    termino = MaximumIteration(max_geracoes)
    algorithmBRKGA = BRKGA(
        termination=termino,
        problem=problem,
        p=n_pop,
        pe=n_elite,
        pm=n_mutant,
        rhoe=rho_elite,
        verbose=False
        )
    algorithmILS = IteratedLocalSearchForTSPPD(
        termination=termino,problem=problem,verbose=False
    )
    instancesBRKGA = []
    instancesILS = []
    for i in range(5):
        algorithmBRKGA.run()
        finalTime = time.time() - algorithmBRKGA.startTime
        instancesBRKGA.append(Instancie(instanceNames[numInstances][0], algorithmBRKGA.nIteration, finalTime, algorithmBRKGA.best_solution.cost))
        algorithmILS.run()
        finalTime = time.time() - algorithmILS.startTime
        instancesILS.append(Instancie(instanceNames[numInstances][0], algorithmILS.nIteration, finalTime, algorithmILS.best_solution.cost))
        
    tttGraph = TTTGraph(instancesBRKGA, algorithmBRKGA, lambda x: x <= instanceNames[numInstances][1]*1.45, instanceNames[numInstances][1]*1.45, "BRKGA")
    tttGraph.comparitonTTTGraph(instancesILS, "ILS", lambda x: x <= instanceNames[numInstances][1]*1.45, save=True,nameFile=f"Comparison_{instanceNames[numInstances][0]}.png")
    gerarRelatorio(instancesBRKGA, f"Comparação_BRKGA_{instanceNames[numInstances][0]}")
    gerarRelatorio(instancesILS, f"Comparação_ILS_{instanceNames[numInstances][0]}")
    

    


if(__name__ == "__main__"):
    main()