from parsing import parseLayout
from keyboard import Keyboard, Key, Symbol
import sys 
import getopt
import io
from gui import App, KeyboardView
from analyzer import Analyzer

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
    analyzer = Analyzer(corpus,keyboard)
    analyzer.options["noSpace"] = True
    analyzer.testAll()
    if DEBUGGING:
        print(keyboard.layoutString(layers=SHOW_LAYERS))
        print(keyboardFile, layoutFile, layoutName)
    
    analyzer.printResults()
    left, right =keyboard.leftRightHandPercent()
    print(f"Left hand: {left}%.   Right hand: {right}%.")
    if GUI:
        app = App(analyzer)
        app.mainloop()

if __name__ == "__main__":
    main(sys.argv[1:])