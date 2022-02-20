from iniconfig import ParseError
from keyboard import Key, Symbol, Keyboard
import xml.etree.ElementTree as ET

def parseLayout(layoutName="qwertz",pathToLayouts="layouts.xml"):
    layouts = ET.parse(pathToLayouts).getroot().findall("layout")
    layout = None
    for l in layouts:
        if layoutName == l.attrib["name"]:
            layout = l
            break
    if layout == None:
        raise Exception("No such layout")
    print(layout,layout.attrib)
    kb = parseBoard(layout.attrib["keyboard"])

def parseBoard(keyboardName="laptop",pathToKeyboards="keyboards.xml"):
    keyboards = ET.parse(pathToKeyboards).getroot().findall('keyboard')
    keyboard = None
    for k in keyboards:
        if k.attrib["name"] == keyboardName:
            keyboard = k
            break
    if keyboard == None:
        raise Exception("No such keyboard")
    print(keyboard,keyboard.attrib)
    kb = Keyboard(keyboardName)
    for r in keyboard.findall("row"):
        for k in r.findall("key"):
            key = Key(row= r.attrib["position"])
            key.parse(k)
            
def main():
    parseLayout("qwertz")

if __name__ == "__main__":
    main()