from parsing import parseLayout
from keyboard import Keyboard, Key, Symbol
import sys 
import getopt
import io

DEBUGGING = False
SHOW_LAYERS = ["base"]
def printHelp():
    print("Hilfe")

def parseInputs(argv):
    layoutName = "qwertz"
    layoutFile= "layouts.xml"
    keyboardFile = "keyboards.xml"
    corpus = "corpus.txt"
    try:
        opts, args = getopt.getopt(argv,"hdl:K:L:c:s:",["layout=","keyboardfile=","layoutfile=","corpus=","showlayers="])
    except:
        print("Usage: python optiKey.py -l <layoutname>")
        print("For more help, type python optiKey.py -h")
        sys.exit()
        
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt == "-d":
            global DEBUGGING 
            DEBUGGING = True
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
    with io.open(corpus,"r",encoding="utf-8") as f:
        text = f.read()
        for s in text:
            keyboard.press(s)
    if DEBUGGING:
        print(keyboard.layoutString(layers=SHOW_LAYERS))
        print(keyboardFile, layoutFile, layoutName)
    print("total effort: ",keyboard.totalEffort())
    print("total presses: ", keyboard.totalPressed())
if __name__ == "__main__":
    main(sys.argv[1:])