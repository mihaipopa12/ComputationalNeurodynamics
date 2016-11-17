import numpy as np
import random
from IzNetwork import *
from pylab import plot, show, savefig
import matplotlib.pyplot as plt

class ModularNetwork(object):
    def __init__(self, NExcitatoryModules, NExcitatory, NInhibitory, p):
        self._NExcitatoryModules = NExcitatoryModules
        self._NExcitatory = NExcitatory
        self._NInhibitory = NInhibitory
        self._NTotal = NExcitatory + NInhibitory
        self._p = p

    def setParameters(self):
        a = [0.02] * (self._NExcitatory + self._NInhibitory)
        b = [0.2] * self._NExcitatory + [0.25] * self._NInhibitory
        c = [-65] * (self._NExcitatory + self._NInhibitory)
        d = [8] * self._NExcitatory + [2] * self._NInhibitory
        self._network.setParameters(np.asarray(a), np.asarray(b), np.asarray(c), np.asarray(d))

    def generateEdges(self):
        # Initialise the adjacency matrix
        self._edges = np.zeros((self._NTotal, self._NTotal))
        # Build the initial inter excitatory connections
        perModule = self._NExcitatory / self._NExcitatoryModules 
        for i in range(self._NExcitatoryModules):
            j = 0
            while (j < 1000):
                x = random.randint(i * perModule, (i + 1) * perModule - 1)
                y = random.randint(i * perModule, (i + 1) * perModule - 1)
                if self._edges[x][y] == 0 and x != y:
                    j += 1
                    if random.random() < self._p:
                        while True:
                            module = random.sample(range(0, i) + range(i + 1, self._NExcitatoryModules), 1)[0]
                            z = module * perModule + random.randint(0, perModule - 1)
                            if module == i or z == x:
                                continue
                            if self._edges[x][z] == 0:
                                self._edges[x][z] = 1 
                                break
                    else: 
                        self._edges[x][y] = 1
        # Build connection from excitatory to inhibitory
        for i in range(self._NExcitatory, self._NTotal):
            randomModule = random.randint(0, self._NExcitatoryModules - 1)
            excitatories = random.sample(range(randomModule * perModule, (randomModule + 1) * perModule), 4)
            for excitatory in excitatories:
                self._edges[excitatory][i] = 1
        # Connect inhibitory with everyone else
        for i in range(self._NExcitatory, self._NTotal):
            for j in range(self._NTotal):
                if i != j:
                    self._edges[i][j] = 1
              
    def isExcitatory(self, i):
        return i < self._NExcitatory

    def _getWeight(self, i, j):
        if self.isExcitatory(i) and self.isExcitatory(j):
            return 1.0 * 17
        if self.isExcitatory(i):
            return random.random() * 50
        if not self.isExcitatory(j):
            return -random.random()
        return -random.random() * 2
        if self.isExcitatory(i) and self.isExcitatory(j):
            return 1
        if self.isExcitatory(i):
            return random.random()
        return -random.random()
        # if self.isExcitatory(i) and self.isExcitatory(j):
        #     return 1
        # if self.isExcitatory(i):
        #     return random.random()
        # return -random.random()

    def setWeights(self):
        self._weights = np.zeros((self._NTotal, self._NTotal))
        for i in range(self._NTotal):
            for j in range(self._NTotal):
                if self._edges[i][j] != 0:
                    self._weights[i][j] = self._getWeight(i, j)
        self._network.setWeights(self._weights)
    
    def setDelays(self):
        delays = np.zeros((self._NTotal, self._NTotal), dtype=int)
        for i in range(self._NTotal):
            for j in range(self._NTotal):
                if self.isExcitatory(i) and self.isExcitatory(j):
                    delays[i][j] = random.randint(1, 20)
                else:
                    delays[i][j] = 1
        self._network.setDelays(delays)


    def prepare(self):
        self._network = IzNetwork(self._NTotal, 20)
        self.setParameters()
        self.generateEdges()
        self.setWeights()
        self.setDelays()

    def plotA(self):
        for x in range(self._NTotal):
            for y in range(self._NTotal):
                if self._edges[x][y] != 0:
                    plot(x, y, '.')
        savefig("a.png")

    def generatePoissonCurrent(self):
        current = np.zeros(self._NTotal)
        samples = np.random.poisson(0.01, self._NTotal)
        for i in range(self._NTotal):
            if samples[i] > 0:
                current[i] = 15
        return current
        
    def plotB(self):
        fireEvents = []
        for time in range(1000):
            self._network.setCurrent(self.generatePoissonCurrent())
            for neuron in self._network.update():
                plot(time, neuron, '.')
        savefig("b.png")

def main():
    network = ModularNetwork(8, 800, 200, 0)
    network.prepare()
    # network.plotA()
    # network.plotB()
    # network.plotC()

if __name__ == "__main__":
    main()
