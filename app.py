from customtkinter import *
from PIL import Image
from datetime import date,timedelta
from lib.getDetails import getDetailsIndividual
from lib.menuAndButton import MenuAndButton
from today import Today
from myLists import MyLists
from lib.aestheticsConfig import getAccent,getFont,getWallpapersNum
from lib.getWallpaper import getFromNum
from lib.menu import Menu
from listClass import List
from starred import Starred
from aesthetics import ChangeAccentWin, ChangeFontWin, ChangeWallpaperWin
from tkinter import messagebox
import cProfile
import pstats
from sharinglists import SharedListContainer




class App(CTk):
    # Key class attributes are defined here.

    textgrey="#9e9f9f"
    def __init__(self,email,userPath,theme="dark"):
        """Main app container for Tickd."""

        # Initialise CTk instance
        super().__init__()

        deactivate_automatic_dpi_awareness()
        
        # Define size of window and minsize.
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(750,800)
        
        set_appearance_mode(theme)
        print(self.winfo_screenwidth(),"by",self.winfo_screenheight())

        self.maxdims = [2000,1100]
        self.maxsize(self.maxdims[0],self.maxdims[1])

        # Set window title and favicon
        self.title("Tickd")
        self.iconbitmap("logo//tickd.ico")

        # Calcuate today's date and put into "long date" format.
        self.today = date.today()
        self.todaysDate = self.today

        # Define key object attributes
        # (Defined here since they are used repeatedly throughout the program)
        self.userEmail = email
        self.userPath = userPath

        # Gets user's font from preferences file.
        self.globalFontName = getFont(email)
        
        self.userDetails,self.userIndex = getDetailsIndividual(email)
        try:
            self.userName = self.userDetails[2]
        except TypeError:
            # Handles error if user's details can't be found.
            print("Invalid email entered. Have you registered?")
            
        # Gets user's accent colour from the preferences.json file.
        self.accent = getAccent(email)

        if self.accent == False:
            print("User not found in preferences file. Setting colour to default.")
            self.accent = "dodgerblue2"

        
        self.frames = {}

        self.widgets()
        self.placeWidgets()


        # Menu dictionary is defined to be passed into MenuAndButton class.
        self.dictForMenu = {"Inbox":lambda:self.loadFrame("inbox"),
                            "Today":lambda:self.loadFrame("today"),
                            "My lists":lambda:self.loadFrame("myLists"),
                            "Starred":lambda:self.loadFrame("starred"),
                            "Leaderboard":lambda:self.loadFrame("leaderboard")}
        
        # MenuAndButton object is defined
        self.menu = MenuAndButton(self.currentFrame,self.dictForMenu,origin=self,userName=self.userName)
        self.menu.place(x=20,y=30)

        # Inbox frame is loaded.
        self.loadFrame("inbox")

        # Binding changing window size to calling resizeFrame procedure.
        self.bind("<Configure>",lambda event:self.resizeFrame())

        self.protocol("WM_DELETE_WINDOW",lambda: self.close_window())

        

            
        self.mainloop()
        


    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
        
        # Checks wallpaper
        lightBGNum,darkBGNum = getWallpapersNum(self.userEmail)
              
        self.imgWallpaper = getFromNum(lightBGNum,darkBGNum)
        self.panelWallpaper = CTkLabel(self,text="",image=self.imgWallpaper)

        frameX,frameY = self.frameDimensions()
        self.dummyFrame = CTkFrame(self,width=frameX,height=frameY,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.currentFrame = self.dummyFrame
        
        # Different images specified for light and dark mode.
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),
                                dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49))
        
        
        self.logoPanel = CTkLabel(self.currentFrame,text="",image=self.imgLogo,cursor="hand2")
        
        self.lblNoTasks = CTkLabel(self.currentFrame,text="Load a content frame.",font=(globalFontName,40))


        self.taskFrame = CTkScrollableFrame(self.currentFrame,width=410,height=600,fg_color="#191616")

        #-----------------# Regular app frames #------------------#
        self.frameInbox = List(self,email=self.userEmail,userPath=self.userPath,
                               todaysDate=self.todaysDate,userAccent=self.accent,
                               listName="inbox",fontName=self.globalFontName)
        self.frameToday = Today(self,email=self.userEmail,userPath=self.userPath,
                                todaysDate=self.todaysDate,userAccent=self.accent,
                                fontName=self.globalFontName)
        
        self.frameMyLists = MyLists(self,email=self.userEmail,userPath=self.userPath,
                                    todaysDate=self.todaysDate,userAccent=self.accent,
                                    fontName=self.globalFontName)

        self.frameStarred = Starred(self,email=self.userEmail,userPath=self.userPath,
                                todaysDate=self.todaysDate,userAccent=self.accent)

        framesToAdd = {"today":self.frameToday,
                       "myLists":self.frameMyLists,
                       "starred":self.frameStarred,
                       "leaderboard":self.dummyFrame,
                       "inbox":self.frameInbox}
        
        for each in framesToAdd:
            self.frames[each] = framesToAdd[each]
        
        if self._get_appearance_mode() == "light":
            themeToSet = "Dark mode"
        else:
            themeToSet = "Light mode"

        self.flagNewAccent = False
        self.flagNewFont = False
        self.flagNewWallpaper = False
        self.preferencesMenuDict = {f"{themeToSet}":lambda:self.mode(),
                                    "Accent colour":lambda:self.createNewAccentWin(),
                                    "Display font":lambda:self.createNewFontWin(),
                                    "App wallpaper":lambda:self.createNewWallpaperWin()}
        self.preferencesMenu = Menu(self,self.preferencesMenuDict,self.accent,topLabel=f"{self.userName}",bottomLabel="Your preferences.",
                                    font=self.globalFontName)
        
        self.logoMenuIsOpen = False


        
        
        

    def placeWidgets(self):
        # Not many widgets are placed here, since most of the functionality
        # lies within the currentFrame, placed here in the middle of the screen.
        self.panelWallpaper.place(x=0,y=0)
        self.currentFrame.place(relx=0.5,rely=0.5,anchor="center")
        
        self.logoPanel.place(relx=0.98,y=40,anchor=E)
        self.lblNoTasks.place(relx=0.4,rely=0.4)

        self.currentAttribute = ""

    def close_window(self):
        self.unbind("<Configure>")
        self.destroy()

    def mode(self):
        # Checks current mode
        if get_appearance_mode().lower() == "light":
            set_appearance_mode("dark")
            themeToSet = "Light mode"
        else:
            set_appearance_mode("light")
            themeToSet = "Dark mode"

        
        
        # Redefines preferences menu with correct label. 
        self.preferencesMenuDict = {f"{themeToSet}":lambda:self.mode(),
                                    "Accent colour":self.createNewAccentWin,
                                    "Display font":self.createNewFontWin,
                                    "App wallpaper":self.createNewWallpaperWin}
        self.preferencesMenu = Menu(self,self.preferencesMenuDict,self.accent,
                                    topLabel=f"{self.userName}",bottomLabel="Your preferences.",
                                    font=self.globalFontName)

    def flagFuncAccent(self):
        self.flagNewAccent = not self.flagNewAccent
    
    def flagFuncFont(self):
        self.flagNewFont = not self.flagNewFont
    
    def flagFuncWallpaper(self):
        self.flagNewWallpaper = not self.flagNewWallpaper

    
    def createNewAccentWin(self):
        if self.flagNewAccent:
            messagebox.showinfo("Window already active","Another accent colour window is already active.")            
        else:
            self.flagNewAccent = True
            ChangeAccentWin(self,self.userEmail,self.globalFontName,self.flagFuncAccent)

    def createNewFontWin(self):
        if self.flagNewFont:
            messagebox.showinfo("Window already active","Another display font window is already active.")            
        else:
            self.flagNewFont = True
            ChangeFontWin(self,self.userEmail,self.globalFontName,self.flagFuncFont)

    def createNewWallpaperWin(self):
        if self.flagNewWallpaper:
            messagebox.showinfo("Window already active","Another wallpaper changing window is already active.")            
        else:
            self.flagNewWallpaper = True
            ChangeWallpaperWin(self,self.userEmail,self.globalFontName,self.accent,self.flagFuncWallpaper)

    def frameDimensions(self):
        print(f"Width: {self.winfo_screenwidth()}, Height: {self.winfo_screenheight()}")
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
    
    def logoClicked(self):
        if not self.logoMenuIsOpen:
            self.preferencesMenu.place(in_=self.logoPanel,x=-80,y=60)
            self.logoMenuIsOpen = True
        else:
            self.preferencesMenu.place_forget()
            self.logoMenuIsOpen = False


    def resizeFrame(self):
        # Frame size calculated based on size of window at that time.
        frameX = 0.95*self.winfo_width() # Usually 0.95
        frameY = 0.95*self.winfo_height() # Usually 0.95

        # Changes currentFrame width and height to calculated values.
        self.currentFrame.configure(width=frameX,height=frameY)            

        # When the window width is below a certain value.
        if self.winfo_width() < 1505:
            # All of these classes (Today, List and Starred) have an entry to move and remove.
            if isinstance(self.currentFrame,Today) or isinstance(self.currentFrame,List) or isinstance(self.currentFrame,Starred):
                # Removes entry box from view, since it does not fit in the window correctly.
                self.currentFrame.entryTask.place_forget()

                # Adjusts height so that both overdueFrame and taskFrame fit in.
                if isinstance(self.currentFrame,List):
                    if len(self.currentFrame.overdueList) >0:
                        self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.4)
                    else:
                        self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.7)

        if self.winfo_width() > 1505:
            if isinstance(self.currentFrame,Today) or isinstance(self.currentFrame,List) or isinstance(self.currentFrame,Starred):
                # Places entry task back if there is enough space to display it.
                self.currentFrame.entryTask.place(in_=self.currentFrame.logoPanel,x=-750,y=10)

                # Similar code to above.
                if isinstance(self.currentFrame,List) or isinstance(self.currentFrame,Starred):
                    if len(self.currentFrame.overdueList) >0:
                        self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.4)
                    else:
                        self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.7)

        
    def checkOverdueAll(self):
        for each in self.frames:
            frame = self.frames[each]
            try:
                if not isinstance(frame,Today) and not isinstance(frame,MyLists):
                    frame.checkNotOverdue()
                    frame.checkTasks()
            except:
                pass

    def updateTasks(self):
        for each in self.frames:
            # Selects each frame one by one.
            frame = self.frames[each]

            # Every frame, except for the 'My lists' frame, is called.
            if not isinstance(frame,MyLists):
                try:
                    # Runs the checkTasks function in every frame.
                    frame.checkTasks()
                except AttributeError:
                    # Just in case the frame does not have a checkTasks function.
                    # This ensures that the updating keeps going.
                    pass



    """and not isinstance(frame,Starred)"""

    def checkNewTasksAll(self):
        for each in self.frames:
            frame = self.frames[each]

            if not isinstance(frame,MyLists):
                try:
                    frame.checkNewTasksAdded()
                except AttributeError: pass

    def loadFrame(self,frameName):
        # Removes current frame from the screen
        self.currentFrame.place_forget()

        # Accesses the frame to be placed.
        self.currentFrame = self.frames[frameName]

        # Place the new frame
        self.currentFrame.place(relx=0.5,rely=0.5,anchor="center")

        try:
            # Redefines the menu, logoPanel and preferencesMenu.
            # This ensures that they can be displayed above the new frame, since they have been defined "last"
            self.menu = MenuAndButton(self.currentFrame,self.dictForMenu,\
                                      origin=self,userName=self.userName,accent=self.accent,
                                      font=self.globalFontName)
            

            self.logoPanel = CTkLabel(self.currentFrame,text="",image=self.imgLogo,cursor="hand2")
            
            self.preferencesMenu = self.preferencesMenu
            
            self.logoPanel.unbind("<Button-1>")
            self.logoPanel.bind("<Button-1>",lambda event:self.logoClicked())
                        
            self.menu.place(x=20,y=30)
            self.logoPanel.place(relx=0.98,y=40,anchor=E)
            
        except:
            pass

        try:
            # Runs the rename function in the new currentFrame
            # In the listClass, this has been defined as a procedure, so will work for every listClass object.
            self.currentFrame.renameMainWin()
        except:
            # If the renameMainWin procedure doesn't exist, the window is renamed by default to the new frame name.
            self.title(f"{frameName}")
    
    def createNewApp(self):
        self.destroy()
        App(self.userEmail,self.userPath)
  
    
    
    
     


#app = App(email="omar@gmail.com",userPath="users//omar@gmail.com")
#app = App(email="amoghg75@yahoo.com",userPath="users//amoghg75@yahoo.com")
