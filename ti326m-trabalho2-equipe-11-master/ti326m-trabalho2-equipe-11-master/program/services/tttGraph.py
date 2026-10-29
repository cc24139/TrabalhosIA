import matplotlib.pyplot as plt
import random
import matplotlib.image as mpimg


class TTTGraph:
    def __init__(self,instances,algorithm,targetFunction,targetValue,nameAlgorit):
        self.instances = instances
        self.algorithm = algorithm
        self.targetFunction = targetFunction
        self.targetValue = targetValue
        self.nameAlgorit = nameAlgorit
        
    def plotTime(self, save = False,nameFile = None,helpFunc=None):
        instances = [instance for instance in self.instances if self.targetFunction(instance.value)]
        n = len(instances)
        if n==0:
            #case no instance meets the target function, we will consider all instances for the graph
            #value of target is the worst value of the instances that meet the target function
            instances = [instance for instance in self.instances if helpFunc(instance.value)]
            instances.sort(key=lambda x: x.value)
            self.targetValue = instances[-1].value
            n = len(instances)
        instances.sort(key=lambda x: x.time)
        probabilty = [(i)/n for i in range(1, n+1)]
        plt.title(f"Cumulative Probability for {self.nameAlgorit} \n Target Value: {self.targetValue}")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Cumulative Probability")
        plt.plot([instance.time for instance in instances], probabilty, marker='o',label=f'{self.nameAlgorit}')
        plt.grid()
        if save:
            plt.savefig(f"{self.nameAlgorit}_time.png" if nameFile is None else nameFile)
        plt.show()
        return True
    
    
    
    def comparitonTTTGraph(self,instancesOtherAlgortim,nameOtherAlgorit,otherTargFunc,save=False,nameFile=None):
        instances = [instance for instance in self.instances if self.targetFunction(instance.value)]
        instancesOtherAlgortim = [instance for instance in instancesOtherAlgortim if otherTargFunc(instance.value)]
        instances.sort(key=lambda x: x.time)
        instancesOtherAlgortim.sort(key=lambda x: x.time)
        n = len(instances)
        probabilty = [i/n for i in range(1, n+1)]
        plt.title(f"Cumulative Probability Comparison")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Cumulative Probability")
        plt.plot([instance.time for instance in instances], probabilty, marker='o',label=f'{self.nameAlgorit}')
        plt.plot([instance.time for instance in instancesOtherAlgortim], probabilty, marker='o',label=f'{nameOtherAlgorit}')
        plt.grid()
        plt.legend()
        plt.show()
        if save:
            plt.savefig(f"Comparison_{self.nameAlgorit}_{nameOtherAlgorit}.png" if nameFile is None else nameFile)
    
class Instancie:
    def __init__(self, name, nIterations, time,value):
        self.name = name
        self.nIterations = nIterations
        self.time = time
        self.value = value
        

    
