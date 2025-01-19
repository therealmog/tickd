# Change accent colour window

from customtkinter import *
from lib.task import Task
from PIL import Image
from lib.accentsConfig import getAccent,setAccent
from datetime import date

class ChangeAccentWin(CTkToplevel):
    def __init__(self,master,email,font="Bahnschrift"):
        super().__init__(master=master)

        self.geometry("880x340")
        self.iconbitmap("logo//tickd.ico")
        self.minsize(880,340)
        self.maxsize(880,340)
        self.font = font
        self.email = email
        self.currentAccent = getAccent(email)
        self.today = date.today()
        

        self.widgets()
        self.placeWidgets()

    
    def widgets(self):
        globalFontName = self.font
        self.frameWin = CTkFrame(self,width=850,height=320,corner_radius=20,
                                 border_width=4,border_color="grey4",)
        
        self.lblTitle = CTkLabel(self.frameWin,text="Change your accent colour",
                                 font=(globalFontName,30))
        
        self.lblPreview = CTkLabel(self.frameWin,text="Preview:",
                                 font=(globalFontName,25))

        
        self.accentsDict = {"Crimson":"crimson",
                            "Dodger Blue":"dodgerblue2",
                            "Lime":"lime",
                            "Sky Blue":"skyblue",
                            "Deep Pink":"deep pink",
                            "Dark Orange":"darkorange2"}
        
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(25,25))
        self.btnSave = CTkButton(self,text="save",font=(globalFontName,25),fg_color="grey24",\
                                            command=lambda:self.saveDescription(),width=70,image=self.imgSave)
        self.tickImg = CTkImage(Image.open("logo//tick.png"),size=(35,35))
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",font=(globalFontName,25),\
                                image=self.tickImg,compound="left")
        
        self.options = []
        
        for each in self.accentsDict:
            # options should always have current one first.
            if self.currentAccent == self.accentsDict[each]:
                self.options.insert(0,each)
            else:
                self.options.append(each)
        
        self.chosen = self.currentAccent

        self.createPreview(self.currentAccent)

        

        self.chosen = self.options[0]
        self.coloursMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,30),
                                         dropdown_font=(globalFontName,25),values=self.options,
                                         width=230,
                                         command=lambda event:self.createPreview())

    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5, anchor="center")

        self.lblTitle.place(x=30,y=20)
        
        self.coloursMenu.place(x=30,y=80)
        self.lblPreview.place(in_=self.coloursMenu,x=400)
    
    def createPreview(self,colour=None):
        if colour==None:
            self.chosen=self.coloursMenu.get()
            colour=self.accentsDict[self.chosen]
        
        if self.chosen != self.currentAccent:
            self.btnSave.place(in_=self.coloursMenu,x=50,y=50)
        else:
            self.btnSave.place_forget()


        self.colourLbl = CTkLabel(self.frameWin,text="This is the colour",font=(self.font,25),
                                  text_color=colour)
        self.hoverLbl = CTkLabel(self.frameWin,text="Hover over me!",font=(self.font,25),
                                 text_color=("black","white"),cursor="hand2")

        self.hoverLbl.bind("<Enter>",lambda event,colour=colour:self.hoverLbl.configure(text_color=colour))
        self.hoverLbl.bind("<Leave>",lambda event,colour=("black","white"):self.hoverLbl.configure(text_color=colour))

        self.previewTask = Task(self.frameWin,{"title":"Do your homework",
                                               "date":self.today.strftime("%d/%m/%Y"),
                                               "taskID":"asdojajsd",
                                               "time":"",
                                               "priority":"",
                                               "description":""},accent=colour,
                                               size=30)
        
        self.colourLbl.place(in_=self.lblPreview,y=50)
        self.hoverLbl.place(in_=self.colourLbl,y=50)
        self.previewTask.place(in_=self.hoverLbl,y=50)
        
    

root = CTk()
accentWin = ChangeAccentWin(root,email="amoghg75@yahoo.com")
#accentWin.bind("<Configure>",lambda event:print(f"{accentWin.winfo_width()}x{accentWin.winfo_height()}"))
root.mainloop()




