# Amogh NG
# Nice looking checkbox

from customtkinter import *
from PIL import ImageTk, Image

"""root = Tk()
root.geometry("600x400")"""

class Checkbox:
    def __init__(self,parent:CTk,x,y,size:tuple,relWidget=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.relWidget = relWidget

        self.emptyImg = CTkImage(Image.open("lib//checkbox//empty.png"),size=size)
        self.emptyImgPanel = CTkLabel(parent,image=self.emptyImg,cursor="hand2",text="")

        self.checkedImg = CTkImage(Image.open("lib//checkbox//checked.png"),size=size)
        self.checkedImgPanel = CTkLabel(parent,image=self.checkedImg,cursor="hand2",text="")

        
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
