from iniconfig import ParseError
from keyboard import Key, Symbol, Keyboard
import xml.etree.ElementTree as ET

def parseLayout(layoutName="qwertz",pathToLayouts="layouts.xml"):
    symbols = []
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

    for layer in layout.findall("layer"):
        layerName=layer.attrib["layer_name"]
        print(f"Found Layer: {layerName}")
        layerEffort = layer.attrib["effort"]
        print("effort: ",layerEffort)
        for symbol in layer.findall("symbol"):
            #print(symbol.attrib["value"])
            key = kb.getKey(int(symbol.attrib["key"]))
            sym = Symbol()
            sym.layerEffort = layerEffort
            sym.layerName= layerName
            sym.parse(symbol)
            if key != None:
                key.symbols.append(sym)
                sym.key = key
    kb.symbols = symbols
    return kb

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
            key = Key(row= int(r.attrib["position"]))
            key.parse(k)
            kb.addKey(key)
    return kb
            
def main():
    kb = parseLayout("qwertz")
    print(kb.layoutString("shift"))
    

if __name__ == "__main__":
    main()