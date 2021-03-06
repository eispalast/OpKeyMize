from keyboard import Keyboard
import io

class Analyzer():
    def __init__(self,corpus:str,keyboard:Keyboard) -> None:
        self.corpus = corpus
        self.keyboard = keyboard
        self.options = {"noSpace":False}
        self.alternatingHands = 0
        self.collisions = 0
        self.leftHand = 0
        self.rightHand = 0
        
    def printResults(self):
        print("total effort: ",self.totalEffort)
        print("total presses: ", self.totalPressed)
        print("alternating hands: ", self.alternatingHands/self.totalPressed)
        print("collisions: ", self.collisions/self.totalPressed)

    @property
    def totalPressed(self):
        return self.keyboard.totalPressed()
    
    @property
    def totalEffort(self):
        return self.keyboard.totalEffort()

    def getLeftRightPercent(self):
        return self.keyboard.leftRightHandPercent()

    def testAll(self):
        self.keyboard.resetPresses()
        self.alternatingHands = 0
        self.collisions = 0
        self.leftHand = 0
        self.rightHand = 0

        with io.open(self.corpus,"r",encoding="utf-8") as f:
            text = f.read()
            prevS=text[0]
            self.keyboard.refreshSymbolDict()
            prevFinger, prevHand = self.keyboard.press(prevS)

            for s in text[1:]:
                if self.options["noSpace"] and s == " ":
                    continue

                finger, hand = self.keyboard.press(s)
                if hand == "r":
                    self.rightHand += 1
                else:
                    self.leftHand += 1

                # Calculate alternating hands
                if prevHand != hand:
                    self.alternatingHands += 1
                elif prevFinger == finger and prevS != s:
                    # same finger on same hand, but not a double on the same key
                    self.collisions +=1

                prevFinger = finger
                prevHand = hand
                prevS = s
        self.keyboard.calcPressedPercent()
      
