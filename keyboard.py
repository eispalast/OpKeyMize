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
        self.id         = element.find("id").text
        self.position   = element.find("position").text
        self.width      = element.find("width").text
        self.hand       = element.find("hand").text
        self.finger     = element.find("finger").text
        self.effort     = element.find("effort").text

class Keyboard:
    def __init__(self,name) -> None:
        self.name = name
        self.keys = {}
    def addKey(self,key:Key):
        self.keys[key.id]=Key

class Symbol:
    def __init__(self, value:str, layerEffort:float, keyID:int, additionalEffort:float=1.0) -> None:
        self.value = value
        self.layerEffort = layerEffort
        self.keyID = keyID
        self.additionalEffort = additionalEffort
        self.key = None
    
    def addKey(self, keys):
        self.key = keys[self.keyID]