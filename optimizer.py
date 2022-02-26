from keyboard import Keyboard, Key
from analyzer import Analyzer
import random

class Optimizer():
    def __init__(self,analyzer:Analyzer) -> None:
        self.analyzer = analyzer
        self.startKB = analyzer.keyboard.copy()
        self.bestKB = {"effort":self.startKB.copy(),
            "collsions":self.startKB.copy(),
            "alternating":self.startKB.copy(),
            "leftRight":self.startKB.copy()}
        self.bestMetrics = {"effort": 100.0,"collisions":1.0,"alternating":0.0,"leftRight":2.0}
        self.newKB = None    
        self.prevChanged = []
    
    def swapKeyVals(self,key1,key2):
        values_temp = key1.symbols
        key1.symbols = key2.symbols
        key2.symbols = values_temp

        for s in key1.symbols:
            s.key = key1
        for s in key2.symbols:
            s.key = key2

    def createNewKB(self):
        # self.prevChanged = []
        self.newKB = Keyboard("optimized")
        for k in self.bestKB["effort"].keys:
            for kb in self.bestKB.values():
                if not k in kb.keys:
                    # add to previously changed keys so they don't get swapped in this round
                    self.prevChanged.append(k.id)
                self.newKB.addKey(k.copy())
        
        # change two random keys
        first = random.randint(0,len(self.newKB.keys)-1)
        while first in self.prevChanged:
            first = random.randint(0,len(self.newKB.keys)-1)
        second = random.randint(0,len(self.newKB.keys)-1)
        while second == first or second in self.prevChanged:
            second = random.randint(0,len(self.newKB.keys)-1)
        self.swapKeyVals(self.newKB.keys[first],self.newKB.keys[second])
        
    def optimize(self, iterations:int):
        self.analyzer.testAll()
        for i in range(iterations):
            print(f"optiround: {i}")
            better = False
            if self.analyzer.totalEffort < self.bestMetrics["effort"]:
                self.bestMetrics["effort"] = self.analyzer.totalEffort
                self.bestKB["effort"] = self.analyzer.keyboard.copy()
                better = True
            
            if self.analyzer.collisions/self.analyzer.totalPressed < self.bestMetrics["collisions"]:
                self.bestMetrics["collisions"] = self.analyzer.collisions/self.analyzer.totalPressed
                self.bestKB["collisions"] = self.analyzer.keyboard.copy()
                better = True
                        
            if self.analyzer.alternatingHands > self.bestMetrics["alternating"]:
                self.bestMetrics["alternating"] = self.analyzer.alternatingHands
                self.bestKB["alternating"] = self.analyzer.keyboard.copy()
                better = True
            try:
                leftRightRatio = float(self.analyzer.leftHand)/float(self.analyzer.rightHand)
            except:
                leftRightRatio = 2.0
            if abs(1.0-leftRightRatio) < self.bestMetrics["leftRight"]:
                self.bestMetrics["leftRight"] = abs(1.0-leftRightRatio)
                self.bestKB["leftRight"] = self.analyzer.keyboard.copy()
                better = True
            
            if better:
                print("found better layout")
                print(self.analyzer.keyboard.layoutString(layers=["base"]))
                self.analyzer.printResults()
            else:
                self.analyzer.keyboard = self.bestKB["effort"].copy()
            
            self.createNewKB()
            self.analyzer.keyboard = self.newKB
            self.analyzer.testAll()
