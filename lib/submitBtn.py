# Amogh NG
# Submit button inheriting from CTkButton

from customtkinter import *
from PIL import Image


class SubmitButton(CTkButton):
    def __init__(self,parent,command,colour,buttonSize:tuple=(20,20)):
        self.img = CTkImage(Image.open("logo//tick.png"),size=buttonSize)
        super().__init__(master=parent,width=1,image=self.img,fg_color=colour,command=command,text="")


    