from customtkinter import *
from lib.task import Task
from PIL import Image
from lib.accentsConfig import getAccent,getFont,setFont
from datetime import date
from tkinter import messagebox
import textwrap

class ChangeFontWin(CTkToplevel):
    def __init__(self,master,email,font="Bahnschrift",flagFunc=None):
        super().__init__(master=master)

        # Sets window size and title.
        self.geometry("550x480")
        self.title("Change your display font - Tickd")
        self.minsize(550,480)
        self.maxsize(550,480)

        # Defines class attributes
        self.font = font
        self.email = email
        self.currentFont = getFont(email)
        self.accent = getAccent(email)
        self.today = date.today()
        self.flagFunc = flagFunc
        
        # Assigns a custom function for when the close button (X) is clicked
        self.protocol("WM_DELETE_WINDOW",self.close_window)

        self.widgets()
        self.placeWidgets()

        # Uses tkinter grab_set and lift methods to bring window infront of main app window. 
        self.grab_set()
        self.lift()
        self.after(1000,self.grab_release)

    def close_window(self):
        if self.flagFunc != None:
            self.flagFunc()
        
        self.destroy()
    
    def widgets(self):
        globalFontName = self.font
        self.frameWin = CTkFrame(self,width=515,height=460,corner_radius=20,
                                 border_width=4,border_color="grey4",fg_color=("white","gray9"))
        
        self.lblTitle = CTkLabel(self.frameWin,text="Change your display font.",
                                 font=(globalFontName,30))
        
        self.lblSubtitle = CTkLabel(self.frameWin,text="Select a font to view its preview.",
                                 font=(globalFontName,18))
        
        self.lblPreview = CTkLabel(self.frameWin,text="Preview:",
                                 font=(globalFontName,15))
        
        imgLogo = CTkImage(Image.open("logo//whiteBGLogo.png"),
                           Image.open("logo//blackBGLogo.png"),
                           size=(106,34))
        self.logoPanel = CTkLabel(self.frameWin,text="",image=imgLogo)

        
        self.fontsDict = {"Bahnschrift (default)":"Bahnschrift",
                            "Georgia":"Georgia",
                            "Franklin Gothic Demi":"Franklin Gothic Demi",
                            "Cascadia Code":"Cascadia Code",
                            "Century Gothic":"Century Gothic",
                            "Calibri":"Calibri",
                            "Wingdings":"Wingdings"}
        
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(35,35))
        self.btnSave = CTkButton(self,text="",font=(globalFontName,28),fg_color="grey24",
                                            command=lambda:self.setNewFont (),width=70,
                                            image=self.imgSave,corner_radius=20)
        self.tickImg = CTkImage(Image.open("logo//tick.png"),size=(25,25))
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",
                                font=(globalFontName,25),image=self.tickImg,compound="left")
        
        # Defines options for the option menu
        self.options = []
        
        for each in self.fontsDict:
            # options should always have user's currently chosen accent font first.
            if self.currentFont == self.fontsDict[each]:
                self.options.insert(0,each)
            else:
                self.options.append(each)

        self.chosen = self.options[0]
        self.fontsMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,25),
                                         dropdown_font=(globalFontName,22),values=self.options,
                                         width=300,
                                         fg_color=("grey","gray24"),button_color="gray16",button_hover_color=self.accent,
                                         dropdown_text_color="white",
                                         command=lambda event:self.createPreview(),
                                         dropdown_fg_color=("grey","grey16"),
                                         corner_radius=15,
                                         cursor="hand2")
        
        self.createPreview(self.currentFont)

    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5, anchor="center")

        self.lblTitle.place(x=40,y=55)
        self.logoPanel.place(in_=self.lblTitle,x=130,y=-30)
        self.lblSubtitle.place(in_=self.lblTitle,x=45,y=70)
        
        self.fontsMenu.place(in_=self.lblSubtitle,x=20,y=35)
        self.lblPreview.place(in_=self.lblTitle,y=180)
    
    def createPreview(self,newFont=None):
        # If preview needs to be created (not being called by options menu), a font can be specified.
        # Otherwise, if no font is specified (font is None) then font is the current item in the options menu.
        if newFont==None:
            self.chosen=self.fontsMenu.get()
            newFont=self.fontsDict[self.chosen]
        
        # Places save button if chosen font is not the same as user's currently set accent font.
        if newFont != self.currentFont:
            self.btnSave.place(in_=self.fontsMenu,x=240)
        else:
            self.btnSave.place_forget()

        try:
            self.fontLbl.place_forget()
        except:
            pass
        
        # Defines two labels: one static label to show the font.
        
        # Defines a wraplength depending on the font being used.
        if "Cascadia" in newFont:
            wraplength = 30
        elif "Century" in newFont:
            wraplength = 35
        else:
            wraplength = 40
        
        wrappedText = textwrap.fill("Grumpy wizards make toxic brew for the evil Queen and Jack.",wraplength)
        self.fontLbl = CTkLabel(self.frameWin,text=wrappedText,
                                font=(newFont,25),text_color=("black","white"),justify="left")

        # Creates a small preview task
        self.previewTask = Task(self.frameWin,{"title":"Do your homework",
                                               "date":self.today.strftime("%d/%m/%Y"),
                                               "taskID":"asdojajsd",
                                               "time":"",
                                               "priority":"",
                                               "description":"",
                                               "listName":""},userPath=None,font=newFont,
                                               accent=self.accent,size=28)
        
        # Places label and preview task.
        self.fontLbl.place(in_=self.lblPreview,y=30)
        self.previewTask.place(in_=self.fontLbl,y=100)
    
    def setNewFont(self):
        # Runs procedure to set accent, passing in user email and actual font name (stored in dictionary fontsDict).
        setFont(self.email,self.fontsDict[self.fontsMenu.get()])
        
        # Changes value of flag in app window by calling specified function.
        if self.flagFunc != None:
            self.flagFunc()

        # Creates a message box to notify the user that the font has been set.
        messagebox.showinfo("New font set","Your new display font has been set.\nClick 'OK' to restart the app.")
        
        # Restarts the app to recreate all widgets with new accent font.
        self.master.createNewApp()

        # Closes this window.
        self.destroy()
    

"""root = CTk()
accentWin = ChangeAccentWin(root,email="amoghg75@yahoo.com")
#accentWin.bind("<Configure>",lambda event:print(f"{accentWin.winfo_width()}x{accentWin.winfo_height()}"))
root.mainloop()"""




