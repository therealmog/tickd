# Amogh NG
# Nice looking checkbox

from tkinter import *
from PIL import ImageTk, Image

"""root = Tk()
root.geometry("600x400")"""

class Checkbox():
    def __init__(self,parent:Tk,x,y,relWidget,size:tuple):
        self.x = x
        self.y = y
        self.parent = parent
        self.relWidget = relWidget

        self.emptyImg = ImageTk.PhotoImage(Image.open("checkbox//empty.png").resize(size))
        self.emptyImgPanel = Label(parent,image=self.emptyImg,cursor="hand2")

        self.checkedImg = ImageTk.PhotoImage(Image.open("checkbox//checked.png").resize(size))
        self.checkedImgPanel = Label(parent,image=self.checkedImg,cursor="hand2")

        
        #self.emptyImgPanel.bind("<Enter>",self.setChecked)
        #self.checkedImgPanel.bind("<Leave>",self.setEmpty)
        self.emptyImgPanel.bind("<Button-1>",lambda event:self.boxClicked(event))
        self.checkedImgPanel.bind("<Button-1>",lambda event:self.boxClicked(event))

        self.value = False
        self.justAccessed = False

    def placeWidget(self):
        self.emptyImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)

    def setChecked(self,_):
        self.emptyImgPanel.place_forget()
        self.checkedImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)
    
    def setEmpty(self,_):
        self.checkedImgPanel.place_forget()
        self.emptyImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)
    
    def boxClicked(self,_):
        if self.value == False:
            self.value = True
            self.setChecked(_)
        else:
            self.value = False
            self.setEmpty(_)

#myBox = Checkbox(parent=root,x=10,y=20,size=(50,50))
