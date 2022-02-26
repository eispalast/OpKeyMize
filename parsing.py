from keyboard import Key, Symbol, Keyboard
import xml.etree.ElementTree as ET

def parseLayout(layoutName="qwertz",pathToLayouts="layouts.xml",keyboardFile="keyboards.xml"):
    symbols = []
    symdict = {}
    layouts = ET.parse(pathToLayouts).getroot().findall("layout")
    layout = None
    for l in layouts:
        if layoutName == l.attrib["name"]:
            layout = l
            break
    if layout is None:
        raise Exception("No such layout")
    kb = parseBoard(layout.attrib["keyboard"],pathToKeyboards=keyboardFile)
    kb.layoutName = layoutName
    for layer in layout.findall("layer"):
        layerName=layer.attrib["layer_name"]
        layerEffort = layer.attrib["effort"]
        try:
            layerShiftKeyString = layer.attrib["layer_shift_key"]
            layerShiftKey = kb.getKey(int(layerShiftKeyString))
        except:
            layerShiftKey = None 
        for symbol in layer.findall("symbol"):
            #print(symbol.attrib["value"])
            key = kb.getKey(int(symbol.attrib["key"]))
            sym = Symbol()
            sym.layerEffort = layerEffort
            sym.layerName= layerName
            sym.layerShiftKey = layerShiftKey
            sym.parse(symbol)
            if key is not None:
                key.symbols.append(sym)
                sym.key = key
                symbols.append(sym)
                symdict[sym.value]=sym
                if sym.value == "spac":
                    symdict[" "]=sym
                elif sym.value == "ret":
                    symdict["\n"]=sym
    kb.symbols = symbols
    kb.symboldict = symdict
    return kb

def parseBoard(keyboardName="laptop",pathToKeyboards="keyboards.xml"):
    keyboards = ET.parse(pathToKeyboards).getroot().findall('keyboard')
    keyboard = None
    for k in keyboards:
        if k.attrib["name"] == keyboardName:
            keyboard = k
            break
    if keyboard is None:
        raise Exception("No such keyboard")
    kb = Keyboard(keyboardName)
    for r in keyboard.findall("row"):
        for k in r.findall("key"):
            key = Key(row= int(r.attrib["position"]))
            key.parse(k)
            kb.addKey(key)
    return kb
            
