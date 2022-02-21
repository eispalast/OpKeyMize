import tkinter as tk
from tkinter import ttk
from turtle import bgcolor
from unittest import TestCase
from keyboard import Key
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        ttk.Label(self,text="Eyo, captain jack").pack()
        self.title("optiKey")
        self.geometry('1800x800+50+50')
        self.iconbitmap("ok_logo.ico")



# control elements (save, open, ...)


class KeyView(tk.Button):
    def __init__(self, master, text, bg,fg, width,key:Key) -> None:
        super().__init__(master)
        self["text"]=text
        self["bg"]=bg
        self["fg"]=fg
        self["width"]=width
        self["height"]=3
        self["relief"]="solid"
        self["borderwidth"]=0
        self.key=key
        self.bind('<Button>',self.change_color)
    def change_color(self,event):
        current_color=str(self["bg"])
        if current_color != "blue":
            self["bg"]="blue"
        else:
            self["bg"]="grey"
        print(self["bg"])
    def show_label(self,layers=["id"]):
        t=""
        for layer in layers:
            t+=f"{(self.key.layoutString(layer))[1:].lstrip()}\n"
        self["text"]=t
    
        
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
            key=KeyView(self,text=k.id,bg=color,fg="white",width=int(size_factor*k.width),key=k)
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
    
    def showLabels(self,layers=["id"]):
        for row in self.rows:
            for k in row.keys:
                k.show_label(layers)


#if __name__ == "__main__":
#    app = App()
#    kbView = KeyboardView(app)
#    keys=[]
#    for i in range(5):
#        k = Key(0)
#        k.id=i
#        k.width=1.0
#        keys.append(k)
#    kbView.addRow(keys,0)
#    kbView.addRow(keys,1)
#    #kbView.addRow([1.25,1,1,1,1,1],1)
#    app.mainloop()
