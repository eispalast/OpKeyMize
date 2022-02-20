from audioop import add
import xml.etree.ElementTree as ET
class Key:
    def __init__(self,row:int) -> None:
        self.id         = 0
        self.position   = 0
        self.width      = 0.0
        self.hand       = ""
        self.finger     = ""
        self.effort     = 0.0
        self.pressed    = 0
        self.symbols    = []
        self.row        = row
    def parse(self, element):
        self.id         = int(element.find("id").text)
        self.position   = int(element.find("position").text)
        self.width      = float(element.find("width").text)
        self.hand       = element.find("hand").text
        self.finger     = element.find("finger").text
        self.effort     = float(element.find("effort").text)
    def layoutString(self, layer = "id"):
        s = "|"
        for i in range(int(self.width/0.25)):
            s += " "
        if layer == "id":
            s += f"{self.id:4}"
        else:
            try:
                s+= f"{list(filter(lambda x: x.layerName == layer, self.symbols))[0].value:4}"
            except:
                s+= "    "
        for i in range(int(self.width/0.25)):
            s += " "
        s += "|"
        return s

class Keyboard:
    def __init__(self,name) -> None:
        self.name = name
        self.keys = []
        self.symbols = []

    def addKey(self,key:Key):
        if not key in self.keys:
            self.keys.append(key)
    
    def layoutString(self,layer="id"):
        s = f"Keybord name: {self.name}\n"
        s += f"Layer: {layer}\n"
        s += "Keys: \n"
        minRow, maxRow = self.getMinMaxRow()
        for rowID in range(maxRow,minRow-1,-1):
            row = self.getRow(rowID)
            for k in row:
                s+=k.layoutString(layer=layer)
            s += "\n"
        return s
    def getMinMaxRow(self):
        keysSorted = list(sorted(self.keys, key=lambda x: x.row,reverse=True))
        return keysSorted[-1].row, keysSorted[0].row

    def getRow(self, rowID):
        return list(sorted(filter(lambda x: x.row == rowID,self.keys),key=lambda x: x.position))

    def getKey(self, keyID):
        try:
            return list(filter(lambda x: x.id==keyID, self.keys))[0]
        except:
            return None
    
    
class Symbol:
    def __init__(self) -> None:
        self.value = ""
        self.layerEffort = 1.0
        self.key = None
        self.additionalEffort = 1.0
        self.layerName = ""

    def parse(self, element):
        self.value = element.attrib["value"]
        try: 
            self.additionalEffort = element.attrib["additionalEffort"]
        except:
            self.additionalEffort = 1.0    