from parsing import parseLayout
from keyboard import Keyboard, Key, Symbol
import sys 
import getopt
import io
from gui import App, KeyboardView

DEBUGGING = False
GUI = True
SHOW_LAYERS = ["base"]
def printHelp():
    print("Hilfe")

def parseInputs(argv):
    layoutName = "qwertz"
    layoutFile= "layouts.xml"
    keyboardFile = "keyboards.xml"
    corpus = "corpus.txt"
    try:
        opts, args = getopt.getopt(argv,"hdgl:K:L:c:s:",["layout=","keyboardfile=","layoutfile=","corpus=","showlayers="])
    except:
        print("Usage: fail: python optiKey.py -l <layoutname>")
        print("For more help, type python optiKey.py -h")
        sys.exit()
        
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt == "-d":
            global DEBUGGING 
            DEBUGGING = True
        elif opt == "-g":
            global GUI
            GUI = True
        elif opt in ("-l", "--layout"):
            layoutName = arg
        elif opt in ("-L", "--layoutfile"):
            layoutFile = arg
        elif opt in ("-K", "--keyboardfile"):
            keyboardFile = arg
        elif opt in ("-c", "--corpus"):
            corpus = arg
        elif opt in ("-s", "--showlayers"):
            global SHOW_LAYERS
            SHOW_LAYERS = arg.split(",")
    return layoutName, layoutFile, keyboardFile, corpus


def main(argv):
    layoutName, layoutFile, keyboardFile, corpus = parseInputs(argv)
    keyboard = parseLayout(layoutName,layoutFile,keyboardFile)
    alternatingHands = 0
    sameFinger = 0

    with io.open(corpus,"r",encoding="utf-8") as f:
        text = f.read()
        prevS=text[0]
        prevFinger, prevHand = keyboard.press(prevS)

        for s in text[1:]:
            finger, hand = keyboard.press(s)

            # Calculate alternating hands
            if prevHand != hand:
                alternatingHands += 1
            elif prevFinger == finger and prevS != s:
                # same finger on same hand, but not a double on the same key
                sameFinger +=1
            
            prevFinger = finger
            prevHand = hand
            prevS = s
    keyboard.calcPressedPercent()
    if DEBUGGING:
        print(keyboard.layoutString(layers=SHOW_LAYERS))
        print(keyboardFile, layoutFile, layoutName)
    
    print("total effort: ",keyboard.totalEffort())
    print("total presses: ", keyboard.totalPressed())
    print("alternating hands: ", alternatingHands/keyboard.totalPressed())
    print("same finger: ", sameFinger/keyboard.totalPressed())
    left, right =keyboard.leftRightHandPercent()
    print(f"Left hand: {left}%.   Right hand: {right}%.")
    if GUI:
        app = App()
        kbView = KeyboardView(app)
        allRows=keyboard.getAllRows()
        for id, row in enumerate(keyboard.getAllRows()):
            kbView.addRow(position=id,keys=row)
        kbView.showLabels(["id","effort"])
        app.mainloop()

if __name__ == "__main__":
    main(sys.argv[1:])