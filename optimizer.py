from keyboard import Keyboard, Key
import random

class Optimizer():
    def __init__(self,analyzer) -> None:
        self.analyzer = analyzer
        self.startKB = analyzer.keyboard
        self.bestKB = {"effort":self.startKB.copy(),
            "collsions":self.startKB.copy(),
            "alternating":self.startKB.copy(),
            "leftRight":self.startKB.copy()}
        self.bestMetrics = {"effort": 100.0,"collisions":1.0,"alternating":0.0,"leftRight":2.0}
        self.newKB = None    
    
    def createNewKB(self):
        missingKeys = []
        self.newKB = Keyboard()
        for k in self.bestKB["effort"].keys:
            for kb in self.bestKB.values:
                if not k in kb.keys:
                    missingKeys.append(k)
                    break
            else:
                self.newKB.addKey(k)
        # TODO: add the missing keys

        # change two random keys
        first = random.randint(0,len(self.newKB.keys)-1)
        second = random.randint(0,len(self.newKB.keys)-1)
        while second == first:
            second = random.randint(0,len(self.newKB.keys)-1)

        values_temp = self.newKB.keys[first].values
        self.newKB.keys[first].values = self.newKB.keys[second].values
        self.newKB.keys[second].values = values_temp

    def optimize(self, iterations:int):
        self.analyzer.testAll()
