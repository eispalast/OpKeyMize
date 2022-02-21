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
        self.pressedPerc= 0
        self.symbols    = []
        self.row        = row
    def parse(self, element):
        self.id         = int(element.find("id").text)
        self.position   = int(element.find("position").text)
        self.width      = float(element.find("width").text)
        self.hand       = element.find("hand").text
        self.finger     = element.find("finger").text
        self.effort     = float(element.find("effort").text)
    def layoutString(self, layer = "id",compact=False):
        s = "|"
        if not compact:
            for i in range(int(self.width/0.25)):
                if layer != "bottom":
                    s += " "
                else:
                    s += "_"
        if layer == "id":
            s += f"{self.id:4}"
        elif layer == "effort":
            s += f"{self.effort:4}"
        elif layer == "null":
            s+= "    "
        elif layer == "bottom":
            s+="____"
        elif layer == "pressed":
            s+= f"{self.pressed:4}"
        elif layer == "pressedPerc":
            s+= f"{(self.pressedPerc*100):4.1f}"
        else:
            try:
                s+= f"{list(filter(lambda x: x.layerName == layer, self.symbols))[0].value:4}"
            except:
                s+= "    "
        if not compact:
            for i in range(int(self.width/0.25)):
                if layer != "bottom":
                    s += " "
                else:
                    s += "_"
        return s


class Keyboard:
    def __init__(self,name) -> None:
        self.name = name
        self.keys = []
        self.symbols = []
        self.symboldict = {}
        self.layoutName = ""

    def addKey(self,key:Key):
        if not key in self.keys:
            self.keys.append(key)
    
    def layoutString(self,layers=["id"],compact=False):
        s = f"Keybord name: {self.name}\n"
        s += f"Layout name: {self.layoutName}\n"
        s += f"Layers: {layers}\n"
        s += "Keys: \n"
        layers = ["bottom","null","null"]+layers+["null","bottom"]
        minRow, maxRow = self.getMinMaxRow()
        for rowID in range(minRow,maxRow+1):
            row = self.getRow(rowID)
            for layer in layers:
                for k in row:
                    s+=k.layoutString(layer=layer,compact=compact)
                s += "|\n"
        return s
    def getMinMaxRow(self):
        keysSorted = list(sorted(self.keys, key=lambda x: x.row,reverse=True))
        return keysSorted[-1].row, keysSorted[0].row

    def getRow(self, rowID):
        return list(sorted(filter(lambda x: x.row == rowID,self.keys),key=lambda x: x.position))
    
    def getAllRows(self):
        min,max=self.getMinMaxRow()
        allRows = []
        for i in range(min,max+1):
            allRows.append(self.getRow(i))
        return allRows

    def getKey(self, keyID):
        try:
            return list(filter(lambda x: x.id==keyID, self.keys))[0]
        except:
            return None
    
    def getLayers(self):
        layers = []
        for s in self.symbols:
            l = s.layerName
            if not l in layers:
                layers.append(l)
        return layers
    
    def press(self, s):
        symbol = self.symboldict[s]
        symbol.key.pressed +=1
        try:
            symbol.layerShiftKey.pressed+=1
        except:
            pass
        return symbol.key.finger, symbol.key.hand
        

    def totalEffort(self):
        return sum([x.effort*x.pressed for x in self.keys])/self.totalPressed()

    def totalPressed(self):
        return sum([x.pressed for x in self.keys])
    
    def leftRightHand(self):
        right = sum(x.pressed for x in filter(lambda x: x.hand=="r",self.keys))
        left = self.totalPressed() - right
        return left,right
    def leftRightHandPercent(self):
        left, right = self.leftRightHand()
        total = self.totalPressed()
        return left/total, right/total   
    def calcPressedPercent(self):
        total = self.totalPressed()
        for k in self.keys:
            k.pressedPerc = k.pressed/total
class Symbol:
    def __init__(self) -> None:
        self.value = ""
        self.layerEffort = 1.0
        self.layerShiftKey = None
        self.key = None
        self.additionalEffort = 1.0
        self.layerName = ""

    def parse(self, element):
        self.value = element.attrib["value"]
        try: 
            self.additionalEffort = element.attrib["additionalEffort"]
        except:
            self.additionalEffort = 1.0    