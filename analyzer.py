from keyboard import Keyboard
import io

class Analyzer():
    def __init__(self,corpus:str,keyboard:Keyboard) -> None:
        self.corpus = corpus
        self.keyboard = keyboard
        self.options = {"noSpace":False}
        self.alternatingHands = 0
        self.sameFinger = 0
 
    @property
    def totalPressed(self):
        return self.keyboard.totalPressed()
    
    @property
    def totalEffort(self):
        return self.keyboard.totalEffort()

    def testAll(self):
        self.alternatingHands = 0
        self.sameFinger = 0

        with io.open(self.corpus,"r",encoding="utf-8") as f:
            text = f.read()
            prevS=text[0]
            prevFinger, prevHand = self.keyboard.press(prevS)

            for s in text[1:]:
                if self.options["noSpace"] and s == " ":
                    continue

                finger, hand = self.keyboard.press(s)

                # Calculate alternating hands
                if prevHand != hand:
                    self.alternatingHands += 1
                elif prevFinger == finger and prevS != s:
                    # same finger on same hand, but not a double on the same key
                    self.sameFinger +=1

                prevFinger = finger
                prevHand = hand
                prevS = s
        self.keyboard.calcPressedPercent()
      
