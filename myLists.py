from customtkinter import * 
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
from lib.detailsPanel import DetailsPanel
from lib.getListImgs import getListImgs
import glob
from listClass import List
from lib.aestheticsConfig import getAccent,setAccent
from lib.getValueWindow import GetValueWin
from tkinter import messagebox
from lib.checkListName import checkListName
from sharinglists import RequestsMenu,SharedListContainer
import textwrap
import json
from lib.checkListID import checkListID


from PIL import Image

class MyLists(CTkFrame):
    
    textgrey="#9e9f9f"
    def __init__(self,mainWindow,email,userPath,todaysDate,userAccent="dodgerblue2",fontName="Bahnschrift"):
        """The 'My lists' frame class."""
        
        
        super().__init__(mainWindow,width=1400,height=900,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        
        self.mainWindow = mainWindow
        self.mainWindow.title("My lists - Tickd")

        self.userPath = userPath
        self.listName = "My lists"
        self.email = email
        self.todaysDate = todaysDate
        self.globalFontName = fontName

        """self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)"""


        self.accent = userAccent
        self.userName = getDetailsIndividual(self.email)

        self.elements = {
            
        } 

        

        self.widgets()
        self.placeWidgets()
        #self.topButtonCallback("ownedByMe")

        self.creatingNewList = False
        self.getSharedLists()

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
       
        print("Bonjour.")
        self.lblListName = CTkLabel(self,text="My lists",font=(globalFontName,50))
        
        self.textVar = StringVar()
        self.textVar.set(f"Welcome, {self.userName}!")
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49)) 
        self.logoPanel = CTkLabel(self,text="",image=self.imgLogo)
        
        
        #self.btnOwnedByMe = CTkButton(self,text="Owned by me",font=(globalFontName,35),command=lambda btn="ownedByMe":self.topButtonCallback(btn),fg_color="grey28",hover=False,border_width=5,border_color="grey5",corner_radius=60)
        #self.btnSharedWithMe = CTkButton(self,text="Shared with me",font=(globalFontName,35),command=lambda btn="sharedWithMe":self.topButtonCallback(btn),fg_color="grey28",hover=False,border_width=5,border_color="grey5",corner_radius=60)

        #---------# System lists #---------#

        # Defining image and label for default lists title.
        self.imgLogoDefaultLists = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(114,36))
        self.lblDefaultLists = CTkLabel(self,text="default lists",font=(globalFontName,30),image=self.imgLogoDefaultLists,compound="left")

        # Gets a list of icons to use for lists.
        self.listImgs = getListImgs((36,36))

        self.tickdDefaults = []
        # List of titles for the buttons, also acts as key for the icons dict.
        buttons = ["Inbox","Today","Starred"]
        
        for each in buttons:
            button = CTkButton(self,text=each,font=(globalFontName,40),width=280,fg_color="grey28",hover_color="grey24",\
                               border_width=5,border_color="grey5",corner_radius=60,image=self.listImgs[each],compound="left",\
                               cursor="hand2",command=lambda listName=each.lower():self.mainWindow.loadFrame(listName))
            self.tickdDefaults.append(button)
            

        # Other two titles defined
        self.lblYourCustomLists = CTkLabel(self,text="Your custom lists",font=(globalFontName,30))
        self.lblYourSharedLists = CTkLabel(self,text="Your shared lists",font=(globalFontName,30))

        # User's custom lists are retrieved.
        self.getCustomLists()

        # Button to add lists is defined.
        self.btnAddList = CTkButton(self,text="Create list",font=(globalFontName,28),
                                    width=180,fg_color=self.accent,hover_color="green",border_width=3,\
                                    border_color="grey5",corner_radius=60,image=self.listImgs["Add"],
                                    compound="left",cursor="hand2",command=self.createList)
        
        
        # Creates scrollable frame to store shared lists.
        self.frameSharedLists = CTkScrollableFrame(self,width=350,height=400,fg_color=("white","gray9"))
        self.sharedLists = []

        # Creates requests menu frame to appear when requests button clicked. 
        self.requestsMenu = RequestsMenu(self,self.email,self.globalFontName,self.accent)

        self.btnRequests = CTkButton(self,text="Requests",font=(globalFontName,28),
                                    width=180,fg_color=self.accent,hover_color="grey24",border_width=3,\
                                    border_color="grey5",corner_radius=60,image=self.listImgs["My lists"],
                                    compound="left",cursor="hand2",command=self.placeRequestsMenu)

    def placeWidgets(self):
        #self.place(relx=0.5,rely=0.5,anchor="center")
        #self.panelImgBG.place(x=0,y=0)
        
        self.lblListName.place(x=125,y=30)
        #self.lblDate.place(in_=self.lblListName,x=0,y=-25)
        self.logoPanel.place(relx=0.98,y=40,anchor=E)

        #self.btnOwnedByMe.place(in_=self.lblListName,x=300)
        #self.btnSharedWithMe.place(in_=self.btnOwnedByMe,x=260)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.lblDefaultLists.place(in_=self.lblListName,y=150)
        self.lblYourCustomLists.place(in_=self.lblDefaultLists,x=450)
        self.lblYourSharedLists.place(in_=self.lblYourCustomLists,x=450)
        
        self.frameSharedLists.place(in_=self.btnRequests,y=40)

        self.tickdDefaults[0].place(in_=self.lblDefaultLists,y=50)
        for each in range(1,len(self.tickdDefaults)):
            self.tickdDefaults[each].place(in_=self.tickdDefaults[each-1],y=70)
        
        self.btnAddList.place(in_=self.lblYourCustomLists,y=50)
        if len(self.customListsBtnsArray) > 0:
            self.customListsBtnsArray[0].place(in_=self.btnAddList,y=50)
            if len(self.customListsBtnsArray)>1:
                for each in range(1,len(self.customListsBtnsArray)):
                    self.customListsBtnsArray[each].place(in_=self.customListsBtnsArray[each-1],y=50)
        
        self.btnRequests.place(in_=self.lblYourSharedLists,y=50)

        
        

        

        self.currentAttribute = ""

    def placeCustomLists(self):
        if len(self.customListsBtnsArray) !=0:
            for each in self.customListsBtnsArray:
                each.place_forget()

            self.customListsBtnsArray[0].place(in_=self.btnAddList,y=50)
            if len(self.customListsBtnsArray) > 1:
                for each in range(1,len(self.customListsBtnsArray)):
                    self.customListsBtnsArray[each].place(in_=self.customListsBtnsArray[each-1],y=50)

    def placeRequestsMenu(self):
        if self.requestsMenu.winfo_ismapped():
            self.requestsMenu.place_forget()
        else:
            self.requestsMenu.place(in_=self.btnRequests,y=50)


    def frameDimensions(self):
        print(f"Width: {self.winfo_screenwidth()}, Height: {self.winfo_screenheight()}")
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
    

    def topButtonCallback(self,btn):
        if btn == "ownedByMe":
            self.btnOwnedByMe.configure(fg_color=self.accent)
            self.btnSharedWithMe.configure(fg_color="grey28")
        else:
            self.btnSharedWithMe.configure(fg_color=self.accent)
            self.btnOwnedByMe.configure(fg_color="grey28")

    def getCustomLists(self):
        globalFontName = self.globalFontName
        self.customLists = {} 
        # key should be name of list, followed by a list with frame object and button object.

        paths = glob.glob(f"{self.userPath}//*.json")
        toRemove = ["inbox.json","shared.json"]
        for each in paths.copy():
            for disallowedPhrase in toRemove:
                if disallowedPhrase in each:
                    paths.remove(each)
        
        for each in paths:
            listName = each.replace(f"{self.userPath}\\","")
            listName = listName.replace(".json","")
            
            listFrame = List(self.mainWindow,self.email,self.userPath,self.todaysDate,getAccent(self.email),listName=listName,
                             fontName=self.globalFontName)
            self.mainWindow.frames[listName] = listFrame
            
            listBtnText = textwrap.fill(listName,18)

            listBtn = CTkButton(self,text=listBtnText,font=(globalFontName,30),width=280,fg_color="grey28",hover_color="grey24",border_width=3,border_color="grey5",corner_radius=60,compound="left",cursor="hand2",command=lambda listName=listName:self.mainWindow.loadFrame(listName))

            self.customLists[listName] = [listFrame,listBtn]
        
        self.customListsBtnsArray = []
        for each in self.customLists:
            self.customListsBtnsArray.append(self.customLists[each][1])

    def getSharedLists(self):
        # Loads in shared JSON file.
        with open(f"{self.userPath}//shared.json","r") as f:
            sharedFile = json.load(f)

        # Removes requests section from shared JSON file
        sharedFile.pop("requests")

        # Iterates through users who have shared lists.
        for user in sharedFile:
            # Iterates through all of the shared listIDs.
            for listID in sharedFile[user]:
                listOwner = user

                # Uses the same procedure used in the RequestsMenu class to get the list name.
                listName = checkListID(user,listID)

                # Creates item in frames dictionary in main app.
                self.mainWindow.frames[listName] = List(self.mainWindow,listOwner,userPath=f"users//{listOwner}",todaysDate=self.todaysDate,
                                                userAccent=self.accent,listName=listName,fontName=self.globalFontName,shared=True)
                
                # Creates new button for the My lists page.
                sharedlist = SharedListContainer(self.frameSharedLists,listName,listOwner,self.mainWindow.loadFrame,{"frameName":listName},
                                                 self.globalFontName,self.accent)
                
                # Places list into shared lists frame and adds it to a list.
                sharedlist.grid(row=len(self.sharedLists),column=0,pady=(5,2))
                self.sharedLists.append(sharedlist)


    def placeSharedList(self,listName,listOwner):
        # Adds to frames dictionary
        self.mainWindow.frames[listName] = List(self.mainWindow,listOwner,userPath=f"users//{listOwner}",todaysDate=self.todaysDate,
                                                userAccent=self.accent,listName=listName,fontName=self.globalFontName,shared=True)
        
        # Creates new shared list object and adds it to the requests frame.
        sharedListObj = SharedListContainer(self.frameSharedLists,listName,listOwner,command=self.mainWindow.loadFrame,
                                            commandArgs={"frameName":listName},font=self.globalFontName,accent=self.accent)

        sharedListObj.grid(row=len(self.sharedLists),column=0,pady=(5,2))
        self.sharedLists.append(sharedListObj)

    def changeNewListFlag(self):
        self.creatingNewList = not self.creatingNewList

    def createNewCustomListBtn(self,listName):
        globalFontName = self.globalFontName
        
        # Sets flag for list name window to False
        self.creatingNewList = False

        # Creates new List object.
        listFrame = List(self.mainWindow,self.email,self.userPath,self.todaysDate,getAccent(self.email),listName=listName)

        # Adds to frames dictionary in main window.
        self.mainWindow.frames[listName] = listFrame

        # Creates button text, but shortens it down to fit within 19 characters
        listBtnText = textwrap.fill(listName,18)

        # Creates new list button for "My lists" page
        # The command for this button is to use the "loadFrame" procedure.
        listBtn = CTkButton(self,text=listBtnText,font=(globalFontName,30),width=280,fg_color="grey28",hover_color="grey24",
                            border_width=3,border_color="grey5",corner_radius=60,compound="left",cursor="hand2",
                            command=lambda listName=listName:self.mainWindow.loadFrame(listName))

        # Appends to array with list buttons
        self.customListsBtnsArray.append(listBtn)
        self.customLists[listName] = [listFrame,listBtn]

        # Places under previous buttons if they exist, otherwise underneath the "Create new list" button
        # The index [-2] indicates the second last button, since the last item in the array will be the button being placed.
        if len(self.customLists) > 1:
            listBtn.place(in_=self.customListsBtnsArray[-2],y=50)
        else:
            listBtn.place(in_=self.btnAddList,y=50)

    def createList(self):
        # self.creatingNewList is a flag variable used to indicate whether the window to get the new list name is open or not.
        # This ensures that two windows are not open simultaneously.
        if self.creatingNewList:
            # Shows error message since another window is already open.
            messagebox.showinfo("New list being created.",
                                "A new list is already being created.\nPlease close the previous box before opening a new one.")
        else:
            # Sets flag to True
            self.creatingNewList = True

            # Creates window to get the value of the new task list name.
            # Function to create new list is passed into this window.
            validationKwargs = {"userPath":self.userPath}
            getValueWin = GetValueWin("list name",assigningFunc=self.createNewCustomListBtn,
                                      validationFunc=checkListName,validationFuncArgs=validationKwargs,
                                      customTitle="Enter name of new list.",accent=self.accent,flagFunc=self.changeNewListFlag,fontName=self.globalFontName)

            



    def renameMainWin(self):
        self.mainWindow.title("My lists - Tickd")

    #--------------------# Task entry and button functions #------------------#
    def taskEntryEnter(self):
        self.placeAttributeEntries()   
        #self.entryTask.unbind("<Key>")

    def bindEnterKey(self):
        self.bind("<Return>",lambda event: self.taskSubmitted)
        print("enter is back")
    
    
     

#today = Today(mainWindow=None,email="omar@gmail.com",userPath="users//omar@gmail.com",theme="dark",listName="inbox")
