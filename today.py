from customtkinter import *
from datetime import date

class Today(CTk):
    globalFontName = "Bahnschrift"
    def __init__(self,userName):
        super().__init__()
        self.geometry("1200x700")

        self.userName = userName

        self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)

        set_appearance_mode("Dark")
        #self.bind("<Configure>",lambda event:self.mode())
        

        deactivate_automatic_dpi_awareness()
        self.widgets()


    def mode(self):
        print(f"{self.winfo_width()},{self.winfo_height()}")
    
    def widgets(self):
        globalFontName = self.globalFontName
        self.title = CTkLabel(self,text=self.todaysDate,font=(globalFontName,40))
        
        self.textVar = f"Welcome {self.userName}"
        self.lblWelcome = CTkLabel(self,text=self.textVar,font=(globalFontName,30))
        self.placeWidgets()
        self.mainloop()
    
    def placeWidgets(self):
        self.title.grid(row=0,column=0,padx=(30,0),pady=(20,0))
        self.lblWelcome.grid(row=0,column=1,padx=(30,0),pady=(30,0))
    
    def placeWelcome(self):
        self.welcome


today = Today(userName="amoghng")
