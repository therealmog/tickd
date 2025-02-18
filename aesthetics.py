# Contains classes for changing aesthetics

from customtkinter import *
from lib.task import Task
from PIL import Image
from lib.aestheticsConfig import getAccent,setAccent,getFont,setFont,getWallpapersNum,setWallpapers
from datetime import date
from tkinter import messagebox
import os
import textwrap
from lib.getListImgs import getListImgs

class ChangeAccentWin(CTkToplevel):
    def __init__(self,master,email,font="Bahnschrift",flagFunc=None):
        super().__init__(master=master)

        # Sets window size and title.
        self.geometry("500x480")
        self.title("Change your accent colour - Tickd")
        self.minsize(500,480)
        self.maxsize(500,480)

        # Defines class attributes
        self.font = font
        self.email = email
        self.currentAccent = getAccent(email)
        self.today = date.today()
        self.flagFunc = flagFunc

        self.fontsDict = {"Bahnschrift":["Bahnschrift",32],
                            "Georgia":["Georgia",32],
                            "Franklin Gothic Demi":["Franklin Gothic Demi",32],
                            "Cascadia Code":["Cascadia Code",28],
                            "Century Gothic":["Century Gothic",30],
                            "Calibri":["Calibri",34],
                            "Wingdings":["Wingdings",30]}
        
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
        self.frameWin = CTkFrame(self,width=470,height=460,corner_radius=20,
                                 border_width=4,border_color="grey4",fg_color=("white","gray9"))
        
        titleFontSize = self.fontsDict[globalFontName][1]
        self.lblTitle = CTkLabel(self.frameWin,text="Change your accent colour.",
                                 font=(globalFontName,titleFontSize))
        
        
        self.lblSubtitle = CTkLabel(self.frameWin,text="Select a colour to view its preview.",
                                 font=(globalFontName,18))
        
        self.lblPreview = CTkLabel(self.frameWin,text="Preview:",
                                 font=(globalFontName,15))
        
        imgLogo = CTkImage(Image.open("logo//whiteBGLogo.png"),
                           Image.open("logo//blackBGLogo.png"),
                           size=(106,34))
        self.logoPanel = CTkLabel(self.frameWin,text="",image=imgLogo)

        
        self.accentsDict = {"Crimson":"crimson",
                            "Dodger Blue":"dodgerblue2",
                            "Lime":"lime",
                            "Sky Blue":"skyblue",
                            "Deep Pink":"deep pink",
                            "Dark Orange":"darkorange2"}
        
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(35,35))
        self.btnSave = CTkButton(self,text="",font=(globalFontName,28),fg_color="grey24",
                                            command=lambda:self.setNewAccent(),width=70,
                                            image=self.imgSave,corner_radius=20)
        self.tickImg = CTkImage(Image.open("logo//tick.png"),size=(25,25))
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",
                                font=(globalFontName,25),image=self.tickImg,compound="left")
        
        # Defines options for the option menu
        self.options = []
        
        for each in self.accentsDict:
            # options should always have user's currently chosen accent colour first.
            if self.currentAccent == self.accentsDict[each]:
                self.options.insert(0,each)
            else:
                self.options.append(each)
        self.chosen = self.currentAccent

        

        

        self.chosen = self.options[0]
        self.coloursMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,30),
                                         dropdown_font=(globalFontName,22),values=self.options,
                                         width=230,
                                         fg_color=("grey","gray24"),button_color="gray16",button_hover_color=self.chosen,
                                         dropdown_text_color="white",
                                         command=lambda event:self.createPreview(),
                                         dropdown_fg_color=("grey","grey16"),
                                         corner_radius=15,
                                         cursor="hand2")
        
        self.createPreview(self.currentAccent)

    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5, anchor="center")

        self.lblTitle.place(x=40,y=55)
        self.logoPanel.place(in_=self.lblTitle,x=130,y=-30)
        self.lblSubtitle.place(in_=self.lblTitle,x=45,y=70)
        
        self.coloursMenu.place(in_=self.lblSubtitle,x=20,y=35)
        self.lblPreview.place(in_=self.lblTitle,y=180)
    
    def createPreview(self,colour=None):
        # If preview needs to be created (not being called by options menu), a colour can be specified.
        # Otherwise, if no colour is specified (colour is None) then colour is the current item in the options menu.
        if colour==None:
            self.chosen=self.coloursMenu.get()
            colour=self.accentsDict[self.chosen]
        
        # Sets hover colour of menu to chosen colour.
        self.coloursMenu.configure(button_hover_color=self.chosen)

        # Places save button if chosen colour is not the same as user's currently set accent colour.
        if colour != self.currentAccent:
            self.btnSave.place(in_=self.coloursMenu,x=240)
        else:
            self.btnSave.place_forget()

        try:
            self.colourLbl.place_forget()
        except:
            pass

        # Defines two labels: one static label to show the colour, and one which can be hovered over.
        # Hovering over second label changes its colour and makes it underlined.
        self.colourLbl = CTkLabel(self.frameWin,text="This is the colour",font=(self.font,30),
                                  text_color=colour)
        self.hoverLbl = CTkLabel(self.frameWin,text="Hover over me!",font=(self.font,22),
                                 text_color=("black","white"),cursor="hand2")

        # Binding for the hover text.
        self.hoverLbl.bind("<Enter>",lambda event,colour=colour:
                           self.hoverLbl.configure(text_color=colour,font=(self.font,22,"underline")))
        self.hoverLbl.bind("<Leave>",lambda event,colour=("black","white"):
                           self.hoverLbl.configure(text_color=colour,font=(self.font,22)))

        # Creates a small preview task
        self.previewTask = Task(self.frameWin,{"title":"Do your homework",
                                               "date":self.today.strftime("%d/%m/%Y"),
                                               "taskID":"asdojajsd",
                                               "time":"",
                                               "priority":"",
                                               "description":"",
                                               "listName":""},userPath=None,font=self.font,
                                               accent=colour,size=28)
        
        # Places label and preview task.
        self.colourLbl.place(in_=self.lblPreview,y=30)
        self.hoverLbl.place(in_=self.colourLbl,y=50)
        self.previewTask.place(in_=self.hoverLbl,y=50)
    
    def setNewAccent(self):
        # Runs procedure to set accent, passing in user email and actual colour name (stored in dictionary accentsDict).
        setAccent(self.email,self.accentsDict[self.coloursMenu.get()])
        
        # Changes value of flag in app window by calling specified function.
        if self.flagFunc != None:
            self.flagFunc()

        # Creates a message box to notify the user that the colour has been set.
        messagebox.showinfo("New accent set","Your new accent colour has been set.\nClick 'OK' to restart the app.")
        
        # Restarts the app to recreate all widgets with new accent colour.
        self.master.createNewApp()

        # Closes this window.
        self.destroy()

class ChangeFontWin(CTkToplevel):
    def __init__(self,master,email,font="Bahnschrift",flagFunc=None):
        super().__init__(master=master)

        # Sets window size and title.
        self.geometry("520x460")
        self.title("Change your display font - Tickd")
        self.minsize(520,460)
        self.maxsize(520,460)

        # Defines class attributes
        self.font = font
        self.email = email
        self.currentFont = getFont(email)
        self.accent = getAccent(email)
        self.today = date.today()
        self.flagFunc = flagFunc

        # Each list contains font name and title label font size.
        self.fontsDict = {"Bahnschrift (default)":["Bahnschrift",32],
                            "Georgia":["Georgia",32],
                            "Franklin Gothic Demi":["Franklin Gothic Demi",32],
                            "Cascadia Code":["Cascadia Code",28],
                            "Century Gothic":["Century Gothic",30],
                            "Calibri":["Calibri",34],
                            "Wingdings":["Wingdings",30]}

        
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
        if globalFontName == "Bahnschrift":
            size = self.fontsDict["Bahnschrift (default)"][1]
        else:
            size = self.fontsDict[globalFontName][1]
        self.frameWin = CTkFrame(self,width=485,height=440,corner_radius=20,
                                 border_width=4,border_color="grey4",fg_color=("white","gray9"))
        
        self.lblTitle = CTkLabel(self.frameWin,text="Change your display font.",
                                 font=(globalFontName,size))
        
        self.lblSubtitle = CTkLabel(self.frameWin,text="Select a font to view its preview.",
                                 font=(globalFontName,18))
        
        self.lblPreview = CTkLabel(self.frameWin,text="Preview:",
                                 font=(globalFontName,15))
        
        imgLogo = CTkImage(Image.open("logo//whiteBGLogo.png"),
                           Image.open("logo//blackBGLogo.png"),
                           size=(106,34))
        self.logoPanel = CTkLabel(self.frameWin,text="",image=imgLogo)

        
        
        
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(32,32))
        self.btnSave = CTkButton(self,text="",font=(globalFontName,28),fg_color="grey24",
                                            command=lambda:self.setNewFont(),width=70,
                                            image=self.imgSave,corner_radius=20)
        self.tickImg = CTkImage(Image.open("logo//tick.png"),size=(25,25))
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",
                                font=(globalFontName,25),image=self.tickImg,compound="left")
        
        # Defines options for the option menu
        self.options = []
        
        for each in self.fontsDict:
            # options should always have user's currently chosen accent font first.
            if self.currentFont == self.fontsDict[each][0]:
                self.options.insert(0,each)
            else:
                self.options.append(each)

        self.chosen = self.options[0]
        self.fontsMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,25),
                                         dropdown_font=(globalFontName,22),values=self.options,
                                         width=285,
                                         fg_color=("grey","gray24"),button_color="gray16",button_hover_color=self.accent,
                                         dropdown_text_color="white",
                                         command=lambda event:self.createPreview(),
                                         dropdown_fg_color=("grey","grey16"),
                                         corner_radius=15,
                                         cursor="hand2")
        
        self.createPreview(self.fontsDict[self.chosen])

    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5, anchor="center")

        self.lblTitle.place(x=65,y=55) # Originally x=40
        self.logoPanel.place(in_=self.lblTitle,x=110,y=-30) # Originally x=130
        self.lblSubtitle.place(in_=self.lblTitle,x=10,y=70)
        
        self.fontsMenu.place(in_=self.lblSubtitle,y=35)
        self.lblPreview.place(x=35,y=230) # Originally x=15,y=180
    
    def createPreview(self,newFont=None):
        """newFont should be a list with font name and title font size."""
        # If preview needs to be created (not being called by options menu), a font can be specified.
        # Otherwise, if no font is specified (font is None) then font is the current item in the options menu.
        if newFont==None:
            self.chosen=self.fontsMenu.get()
            newFont=self.fontsDict[self.chosen]
        
        # Places save button if chosen font is not the same as user's currently set accent font.
        if newFont[0] != self.currentFont:
            self.btnSave.place(in_=self.fontsMenu,x=300,y=-5)
        else:
            self.btnSave.place_forget()
        
        self.fontsMenu.configure(font=(newFont[0],25))

        # Change above labels (title, preview and subtitle) with new font.
        # Title size is stored within the dictionary.
        self.lblTitle.configure(font=(newFont[0],newFont[1]))
        labels = [self.lblSubtitle,self.lblPreview]
        for each in labels:
            original = each._font
            each.configure(font=(newFont[0],original[1]))
            

        try:
            self.fontLbl.place_forget()
        except:
            pass
                
        # Defines a wraplength depending on the font being used.
        if "Cascadia" in newFont[0]:
            wraplength = 30
            fontSize = 22
        elif "Century" in newFont[0]:
            wraplength = 30
            fontSize = 25
        else:
            wraplength = 35
            fontSize=25
        
        wrappedText = textwrap.fill("Grumpy wizards make toxic brew for the evil Queen and Jack.",wraplength)
        self.fontLbl = CTkLabel(self.frameWin,text=wrappedText,
                                font=(newFont[0],fontSize),text_color=("black","white"),justify="left")

        # Creates a small preview task
        self.previewTask = Task(self.frameWin,{"title":"Do your homework",
                                               "date":self.today.strftime("%d/%m/%Y"),
                                               "taskID":"asdojajsd",
                                               "time":"",
                                               "priority":"",
                                               "description":"",
                                               "listName":""},userPath=None,font=newFont[0],
                                               accent=self.accent,size=28)
        
        # Places label and preview task.
        self.fontLbl.place(in_=self.lblPreview,y=30)
        self.previewTask.place(in_=self.fontLbl,y=80) # Reduced from y=130
    
    def setNewFont(self):
        # Runs procedure to set accent, passing in user email and actual font name (stored in dictionary fontsDict).
        setFont(self.email,self.fontsDict[self.fontsMenu.get()][0])
        
        # Changes value of flag in app window by calling specified function.
        if self.flagFunc != None:
            self.flagFunc()

        # Creates a message box to notify the user that the font has been set.
        messagebox.showinfo("New font set","Your new display font has been set.\nClick 'OK' to restart the app.")
        
        # Restarts the app to recreate all widgets with new accent font.
        self.master.createNewApp()

        # Closes this window.
        self.destroy() 

class ChangeWallpaperWin(CTkToplevel):
    def __init__(self,master,email,font="Bahnschrift",accent="dodgerblue2",flagFunc=None):
        super().__init__(master=master)

        # Sets window size and title.
        dims = [1030,620]
        self.geometry(f"{dims[0]}x{dims[1]}")
        self.title("Change your app wallpaper - Tickd")
        self.minsize(dims[0],dims[1])
        self.maxsize(dims[0],dims[1])

        # Defines class attributes
        self.font = font
        self.email = email
        self.accent = accent
        self.today = date.today()
        self.flagFunc = flagFunc

        # These will be just a number, referring to the number wallpaper (e.g. Light "5", Dark "2")
        self.currentLightBG,self.currentDarkBG = getWallpapersNum(self.email)

        # Defining size of title text for each font.
        self.fontsDict = {"Bahnschrift":["Bahnschrift",32],
                            "Georgia":["Georgia",32],
                            "Franklin Gothic Demi":["Franklin Gothic Demi",32],
                            "Cascadia Code":["Cascadia Code",28],
                            "Century Gothic":["Century Gothic",30],
                            "Calibri":["Calibri",34],
                            "Wingdings":["Wingdings",30]}
        
        self.lightBGsDict = {"Light 1":"1","Light 2":"2","Light 3":"3","Light 4":"4","None":"none"}
        
        self.darkBGsDict = {"Dark 1":"1","Dark 2":"2","Dark 3":"3","Dark 4":"4","Dark 5":"5","Dark 6":"6","None":"none"}
        
        
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
       
        # Frames are created: main content frame, light preview frame and dark preview frame.
        self.frameWin = CTkFrame(self,width=1000,height=600,corner_radius=20,
                                 border_width=4,border_color="grey4",fg_color=("white","gray9"))
        
        self.frameLightPreview = CTkFrame(self.frameWin,width=425,height=250,fg_color="white",
                                          border_width=2,border_color=("gray15","gray18"))
        self.frameDarkPreview = CTkFrame(self.frameWin,width=425,height=250,fg_color="gray18",
                                         border_width=2,border_color=("gray18","gray"))

        # Title is created.
        titleFontSize = self.fontsDict[globalFontName][1]
        self.lblTitle = CTkLabel(self.frameWin,text="Change your app wallpaper.",
                                 font=(globalFontName,titleFontSize))
        
        
        imgLogo = CTkImage(Image.open("logo//whiteBGLogo.png"),
                           Image.open("logo//blackBGLogo.png"),
                           size=(106,34))
        self.logoPanel = CTkLabel(self.frameWin,text="",image=imgLogo)

        self.lblWarning = CTkLabel(self.frameWin,text="Click on an option in the menus to view a preview of what the\
                                    wallpaper looks like in the app\n(Note: Inbox frame is an example, may not be representative of what your app looks like.)",
                                 font=(globalFontName,15))

        
        # Creates save button
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(32,32))
        self.btnSave = CTkButton(self,text="save wallpapers",font=(globalFontName,28),fg_color="grey24",
                                            command=lambda:self.setNewWallpapers(),width=70,
                                            image=self.imgSave,corner_radius=20,compound="left")
        
        # Defines options for the option menu
        self.lightOptions = []
        self.darkOptions = []
        
        # Sorts through both sets of options to find the user's currently selected one.
        bgDicts = [[self.lightBGsDict,"Light "],[self.darkBGsDict,"Dark "]]

        for bgDictSet in bgDicts:
            bgDict = bgDictSet[0]
            prefix = bgDictSet[1]
            for each in bgDict:
                # options should always have user's currently chosen wallpaper first.

                # Removes prefix from number
                num = bgDict[each].replace(prefix,"")
                
                if prefix == "Light ":
                    if num == self.currentLightBG:
                        self.lightOptions.insert(0,each)
                    else:
                        self.lightOptions.append(each)
                else:
                    if num == self.currentDarkBG:
                        self.darkOptions.insert(0,each)
                    else:
                        self.darkOptions.append(each)
        
        # Declares preview frame images (panels declared in preview functions) 
        self.imgLightFrame = CTkImage(Image.open("light frame.png"),size=(400,225))
        self.imgDarkFrame = CTkImage(Image.open("dark frame.png"),size=(400,225))
        

        # Declares option menu labels
        iconsImgs = getListImgs((30,30))
        self.lblLight = CTkLabel(self.frameWin,text=" Light:",font=(self.font,25),image=iconsImgs["Light mode"],compound="left")
        self.lblDark = CTkLabel(self.frameWin,text=" Dark:",font=(self.font,25),image=iconsImgs["Dark mode"],compound="left")

        # Creates light and dark menus.
        self.lightChosen = self.lightOptions[0]
        self.darkChosen = self.darkOptions[0]
        self.lightMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,25),
                                         dropdown_font=(globalFontName,22),values=self.lightOptions,
                                         width=140,
                                         fg_color=("grey","gray24"),button_color="gray16",button_hover_color=self.accent,
                                         dropdown_text_color="white",
                                         command=lambda event:self.createLightPreview(),
                                         dropdown_fg_color=("grey","grey16"),
                                         corner_radius=15,
                                         cursor="hand2")
        
        self.darkMenu = CTkOptionMenu(self.frameWin,font=(globalFontName,25),
                                         dropdown_font=(globalFontName,22),values=self.darkOptions,
                                         width=140,
                                         fg_color=("grey","gray24"),button_color="gray16",button_hover_color=self.accent,
                                         dropdown_text_color="white",
                                         command=lambda event:self.createDarkPreview(),
                                         dropdown_fg_color=("grey","grey16"),
                                         corner_radius=15,
                                         cursor="hand2")
        
        self.createLightPreview()
        self.createDarkPreview()

    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5, anchor="center")
        

        self.lblTitle.place(x=310,y=55)
        self.logoPanel.place(in_=self.lblTitle,x=110,y=-30)
        #self.lblSubtitle.place(in_=self.lblTitle,x=10,y=70)
        
        #self.lblPreview.place(x=35,y=230) # Originally x=15,y=180

        self.lblLight.place(x=60,y=150)
        self.lightMenu.place(in_=self.lblLight,x=100)
        self.lblDark.place(in_=self.lblLight,x=550)
        self.darkMenu.place(in_=self.lblDark,x=100)

        self.frameLightPreview.place(in_=self.lblLight,x=-20,y=50)
        self.frameDarkPreview.place(in_=self.lblDark,x=-60,y=50)
        
        self.lblWarning.place(in_=self.frameLightPreview,x=140,y=260)

    
    def createLightPreview(self,newBG=None):
        """newFont should be a file name, e.g. light-1, dark-4, etc."""
        # If preview needs to be created (not being called by options menu), a wallpaper can be specified.
        # Otherwise, if no wallpaper is specified (newBG is None) then font is the current item in the options menu.
        
        if newBG==None:
            self.lightChosen=self.lightMenu.get()
            newBG = self.lightChosen.lower()
        
        
        # Places save button if chosen font is not the same as user's currently set accent font.
        if newBG[0] != self.currentLightBG.lower():
            self.btnSave.place(in_=self.lblTitle,x=60,y=460)
        else:
            self.btnSave.place_forget()
        

        # Change above labels (title, preview and subtitle) with new font.
        # Title size is stored within the dictionary.
        
            
        num = 2
        
        for i in range(num):
            try:
                widgetsToRemove = [self.panelLightBGPreview,self.panelLightFrame]
                widgetsToRemove[i].place_forget()
            except:
                pass
                
        # Creates new wallpaper preview image.
        if newBG != "none":
            imgLightBG = CTkImage(Image.open(f"wallpapers//{newBG.replace(" ","")}.png"),size=(600,432))
            self.panelLightBGPreview = CTkLabel(self.frameLightPreview,text="",image=imgLightBG)
            self.panelLightBGPreview.place(x=2,y=2)
        self.panelLightFrame = CTkLabel(self.frameLightPreview,text="",image=self.imgLightFrame)
        self.panelLightFrame.place(x=13,y=12)

    def createDarkPreview(self,newBG=None):
        """newFont should be a file name, e.g. light-1, dark-4, etc."""
        # If preview needs to be created (not being called by options menu), a wallpaper can be specified.
        # Otherwise, if no wallpaper is specified (newBG is None) then font is the current item in the options menu.
        
        if newBG==None:
            self.darkChosen=self.darkMenu.get()
            newBG = self.darkChosen.lower()
        
        # Places save button if chosen font is not the same as user's currently set accent font.
        if newBG[0] != self.currentDarkBG.lower():
            self.btnSave.place(in_=self.lblTitle,x=60,y=460)
        else:
            self.btnSave.place_forget()
        

        # Change above labels (title, preview and subtitle) with new font.
        # Title size is stored within the dictionary.
        
            
        num = 2
        
        for i in range(num):
            try:
                widgetsToRemove = [self.panelDarkBGPreview,self.panelDarkFrame]
                widgetsToRemove[i].place_forget()
            except:
                pass
                
        # Creates new wallpaper preview image.
        if newBG != "none":
            imgDarkBG = CTkImage(Image.open(f"wallpapers//{newBG.replace(" ","")}.png"),size=(576,432))
            self.panelDarkBGPreview = CTkLabel(self.frameDarkPreview,text="",image=imgDarkBG)
            self.panelDarkBGPreview.place(x=0,y=0)
        self.panelDarkFrame = CTkLabel(self.frameDarkPreview,text="",image=self.imgDarkFrame)
        self.panelDarkFrame.place(x=13,y=12)


    
    def setNewWallpapers(self):
        # Runs procedure to set wallpapers, passing in user email and actual wallpaper number (stored in dictionaries).
        
        setWallpapers(self.email,self.lightBGsDict[self.lightMenu.get()],self.darkBGsDict[self.darkMenu.get()])
        
        # Changes value of flag in app window by calling specified function.
        if self.flagFunc != None:
            self.flagFunc()

        # Creates a message box to notify the user that the font has been set.
        messagebox.showinfo("New wallpapers set","Your new app wallpapers have been set.\nClick 'OK' to restart the app.")
        
        # Restarts the app to recreate all widgets with new accent font.
        self.master.createNewApp()

        # Closes this window.
        self.destroy()
    

"""root = CTk()
accentWin = ChangeAccentWin(root,email="amoghg75@yahoo.com")
#accentWin.bind("<Configure>",lambda event:print(f"{accentWin.winfo_width()}x{accentWin.winfo_height()}"))
root.mainloop()"""




