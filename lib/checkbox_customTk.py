# Amogh NG
# Nice looking checkbox

from customtkinter import *
from PIL import ImageTk, Image

"""root = Tk()
root.geometry("600x400")"""

class Checkbox(CTkBaseClass):
    def __init__(self,parent:CTk,x,y,size:tuple,relWidget=None,command=None,commandArgs=None):
        super().__init__(master=parent)
        self.x = x
        self.y = y
        self.parent = parent
        self.relWidget = relWidget
        self.command = command
        self.commandArgs = commandArgs

        self.emptyImg = CTkImage(Image.open("lib//checkbox//empty.png"),size=size)
        self.emptyImgPanel = CTkLabel(parent,image=self.emptyImg,cursor="hand2",text="")

        self.checkedImg = CTkImage(Image.open("lib//checkbox//checked.png"),size=size)
        self.checkedImgPanel = CTkLabel(parent,image=self.checkedImg,cursor="hand2",text="")

        
        #self.emptyImgPanel.bind("<Enter>",self.setChecked)
        #self.checkedImgPanel.bind("<Leave>",self.setEmpty)
        self.emptyImgPanel.bind("<Button-1>",lambda event:self.boxClicked(event))
        self.checkedImgPanel.bind("<Button-1>",lambda event:self.boxClicked(event))

        self.__value = False
        self.justAccessed = False

    def placeWidget(self):
        self.emptyImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)

    def setChecked(self,_):
        self.emptyImgPanel.place_forget()
        self.checkedImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)
        
        if self.command != None:
            self.after(300,lambda:self.command(**self.commandArgs))
            

    def setEmpty(self,_):
        self.checkedImgPanel.place_forget()
        self.emptyImgPanel.place(in_=self.relWidget,x=self.x,y=self.y)
    
    def boxClicked(self,_):
        self.checkedImgPanel.focus()
        if self.__value == False:
            self.__value = True
            self.setChecked(_)
            
        else:
            self.__value = False
            self.setEmpty(_)

    def disableClicks(self):
        print("helloooo")
        if self.__value:
            self.boxClicked(None)
        self.emptyImgPanel.bind("<Button-1>",None)
    
    def enableClicks(self):
        self.emptyImgPanel.bind("<Button-1>",lambda event:self.boxClicked(event))

    def getValue(self):
        return self.__value

#myBox = Checkbox(parent=root,x=10,y=20,size=(50,50))
