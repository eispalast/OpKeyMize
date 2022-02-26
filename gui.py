import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from turtle import bgcolor
from unittest import TestCase

from pyparsing import anyOpenTag
from keyboard import Key
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class App(tk.Tk):
    def __init__(self,analyzer) -> None:
        super().__init__()
        self.analyzer = analyzer
        ttk.Label(self,text=f"{self.analyzer.keyboard.layoutName} on {self.analyzer.keyboard.name}").pack()
        self.title("OpKeyMize")
        self.geometry('1800x1000+50+50')
        self.iconbitmap("assets/ok_logo.ico")
        self.layer_checkboxes = []
        self.kbView = self.new_keyboard()
        
        self.optionsView = OptionsView(self)
        self.layers = {}
        self.initLayers()
        self.initKb()
        ttk.Button(self.optionsView,text="Analyze",command=self.analyze).grid(column=1,row=1)
        self.showResults()
    

    def analyze(self):
        self.analyzer.testAll()
        self.kbView.color_by_percent()
        self.analyzer.printResults()
        self.showResults()

    def showResults(self):
        self.optionsView.updateResults(self.analyzer)

    def initKb(self):
        for id, row in enumerate(self.analyzer.keyboard.getAllRows()):
            self.kbView.addRow(position=id,keys=row)
        self.add_layer_names(self.analyzer.keyboard.getLayers())
        self.kbView.color_by_percent()


    def initLayers(self):
        self.layers = {}
        self.add_layer_names(["id","effort","pressed","pressedPerc"])

    def layer_checkbox_pressed(self):
        active_layers= []
        for layer, var in self.layers.items():
            if var.get()=="1":
                active_layers.append(layer)
        self.kbView.change_labels(active_layers)        

    def draw_layer_choice(self):
        self.optionsView.destroy()
        self.optionsView = OptionsView(self)
        pos = 1
        self.layer_checkboxes = []
        for layer, var in self.layers.items():
            layer_checkbox = ttk.Checkbutton(self.optionsView,text=layer,command=self.layer_checkbox_pressed,variable=var)
            layer_checkbox.grid(row=pos,column=0,sticky="w")
            self.layer_checkboxes.append(layer)
            pos += 1
    
    def new_keyboard(self):
        return KeyboardView(self)
        
    
    def add_layer_names(self,new_layers):
        for layer in new_layers:
            if layer in self.layers:
                continue
            self.layers[layer]=tk.StringVar()    
        self.draw_layer_choice()


class OptionsView(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack(fill="x")
        ttk.Label(master=self,text="Toggle layer visibility").grid(row=0,column=0)
        ttk.Label(master=self,text="Actions").grid(row=0,column=1)
        

        ttk.Label(master=self,text="Results").grid(row=0,column=2,columnspan=2)
        ttk.Label(self,text="Total effort: ").grid(row=1,column=2,sticky="W")
        self.totalEffort = ttk.Label(self,text="0")
        self.totalEffort.grid(column=3,row=1)

        ttk.Label(self,text="Alternating Hands: ").grid(row=2,column=2, sticky="W")
        self.alternatingHands = ttk.Label(self,text="0")
        self.alternatingHands.grid(column=3,row=2)
        
        ttk.Label(self,text="Left/Right Hand: ").grid(row=3,column=2, sticky="W")
        self.leftRightHand = ttk.Label(self,text="0")
        self.leftRightHand.grid(column=3,row=3)
        
        ttk.Label(self,text="Collision: ").grid(row=4,column=2, sticky="W")
        self.collisions = ttk.Label(self,text="0")
        self.collisions.grid(column=3,row=4)

    def updateResults(self,analyzer):
        self.totalEffort["text"] = f"{analyzer.totalEffort:.2f}"
        self.alternatingHands["text"] = f"{analyzer.alternatingHands/analyzer.totalPressed:.2f}%"
        left, right = analyzer.getLeftRightPercent()
        self.leftRightHand["text"] = f"{left:.2f}%/{right:.2f}%"
        self.collisions["text"] = f"{(analyzer.collisions/analyzer.totalPressed):.4f}%"

# control elements (save, open, ...)


class ButtonOptionWindow(tk.Toplevel):
    def __init__(self, master,key:Key):
        super().__init__(master)
        self.key = key
        self.title("Key options")
        self.geometry("400x400+50+50")
        ttk.Label(self, text="Layer").grid(row=0,column=0)
        ttk.Label(self, text="Value").grid(row=1,column=0)
        self.selectedLayer = tk.StringVar(self)
        self.prevSelectedLayer = tk.StringVar(self)
        self.currentValue = tk.StringVar(self)
        self.labelValues = {}
        self.createLayerSelect()
        self.createValueSelect()
        ttk.Button(self,text="OK",command=self.saveChanges).grid(row=2,column=0)
        ttk.Button(self,text="Cancel",command=self.destroy).grid(row=2,column=1)

    def createLayerSelect(self):
        self.prevSelectedLayer.set("id")
        options = [x for x in list(self.master.master.master.master.layers.keys()) if x not in ["pressed", "pressedPerc"]]
        options+=["hand","finger"]
        option_menu = ttk.OptionMenu(
            self,
            self.selectedLayer,
            "id",
            *options,
            command=self.layerChanged)
        option_menu.grid(row=0,column=1)
    
    def createValueSelect(self):
        self.currentValue.set(self.key.id)
        entry = ttk.Entry(self, textvariable=self.currentValue)
        entry.grid(row=1, column=1)

    def layerChanged(self,*args):
        self.labelValues[self.prevSelectedLayer.get()]=self.currentValue.get()
        self.prevSelectedLayer.set(self.selectedLayer.get())
        print(self.labelValues)

        # try to get value that was just recently set
        try:
            self.currentValue.set(self.labelValues[self.selectedLayer.get()])
        except:
            self.currentValue.set(self.key.getValueAtLabel(self.selectedLayer.get()))
        pass

    def saveChanges(self):
        self.labelValues[self.selectedLayer.get()]=self.currentValue.get()
        print(self.labelValues)
        self.key.set(self.labelValues)
        self.destroy()

class KeyView(tk.Button):
    def __init__(self, master, text, bg,fg, width,key:Key) -> None:
        super().__init__(master)
        self["text"]=text
        self["bg"]=bg
        self["fg"]=fg
        self["font"]=("Bahnschrift",9,"bold")
        self["width"]=width
        self["height"]=3
        self["relief"]="solid"
        self["borderwidth"]=0
        self.key=key
        self.bind('<Button>',self.open_options)
        self.labels = ["id"]
        
    
    def open_options(self,event):
        ButtonOptionWindow(self,self.key)
        
    
    def change_labels(self,layers=["id"]):
        self.labels = layers
        self.show_labels()

    def show_labels(self):
        t=""
        for layer in self.labels:
            t+=f"{(self.key.layoutString(layer))[1:].lstrip()}\n"
        self["text"]=t

    def color_by_percent(self):
        r = 13
        g = 13
        b = 13
        percentage = self.key.pressedPerc*100
        zones = [0.5,4,8,18]
        # blue zone
        if percentage < zones[0]:
            b = 190
            g = 177*(percentage/zones[0])+13
        # green zone
        elif percentage < zones[1]:
            g = 190
            b = 177*(1-(percentage-zones[0])/(zones[1]-zones[0]))+13
        # yellow zone
        elif percentage < zones[2]:
            g = 190
            r = 177*((percentage-zones[1])/(zones[2]-zones[1]))+13
        # red zone
        elif percentage < zones[3]:
            r = 190
            g =177*(1-(percentage-zones[2])/(zones[3]-zones[2]))+13
        else:
            r = 190
            g = 0
            b = 0
        # r = int(r)
        # g = int(g)
        # b = int(b)

        rhex= ("00"+hex(int(r))[2:].lstrip('x'))[-2:]
        ghex= ("00"+hex(int(g))[2:].lstrip('x'))[-2:]
        bhex= ("00"+hex(int(b))[2:].lstrip('x'))[-2:]
        color=f"#{rhex}{ghex}{bhex}"
        #if self.key.pressedPerc < 0.01:
        #    color="#c4c4c4"
        self["bg"]=color
        
# main kb view
class KeyBoardRowView(tk.Canvas):
    def __init__(self,container,keys,position) -> None:
        super().__init__(container)
        self.position = position
        self["width"]=1700
        self["height"]=110
        self["bg"]="grey"
        #self.grid_propagate(0)
        placing_pos = 30
        size_factor = 8
        self.keys = []

        for k in keys:
            #self.columnconfigure(id)
            color = "#AAAAAA"
            if k.id %2 == 0:
                color = "#BBBBBB"
            #key=self.create_rectangle(placing_pos,5,size_factor*width+placing_pos,size_factor+5,fill=color)
            #key.place(y=10, x=placing_pos+10)
            key=KeyView(self,text=k.id,bg=color,fg="#FDFDFD",width=int(size_factor*k.width),key=k)
            key.place(x=placing_pos,y=10) 
            self.keys.append(key)  
            placing_pos += int(size_factor*10*k.width)+30
        
class KeyboardView(tk.Canvas):
    def __init__(self, container) -> None:
        super().__init__(container)
        self["width"]=1700
        self["height"]=0
        self["bg"]="grey"
        #self.pack_propagate(0)
        self.pack()
        self.rows = []
        #self.grid(row=0,column=0,sticky="e")
        
    
    def addRow(self,keys, position):
        print(self["height"])
        self["height"]=(int(self["height"])+110)
        row = KeyBoardRowView(self,keys,position)
        row.place(y=position*110,x=0)
        self.rows.append(row)
    
    def change_labels(self,layers=["id"]):
        for row in self.rows:
            for k in row.keys:
                k.change_labels(layers)

    def color_by_percent(self):
        for row in self.rows:
            for k in row.keys:
                k.color_by_percent()

