# Classes and functions for sharing lists
from customtkinter import *
import json
from lib.checkUserDetails import checkDetailsFound,checkEmail
from tkinter import messagebox
from PIL import Image
import textwrap
from lib.submitBtn import SubmitButton
from lib.getListImgs import getListImgs
from glob import glob


class SharingMenu(CTkToplevel):
    def __init__(self,master,listTitle,userEmail,userPath,font="Bahnschrift",accent="dodgerblue2",flagFunc=None):
        super().__init__(master)

        # Defines geometry, min and max sizes and title
        dims = [500,650]
        self.geometry(f"{dims[0]}x{dims[1]}")
        self.minsize(dims[0],dims[1])
        self.maxsize(dims[0],dims[1])
        self.title(f"Share '{listTitle}' - Tickd")

        # Defines key attributes, including list title, list path, accent colour, font and user email.
        self.listTitle = listTitle
        self.listPath = f"{userPath}//{listTitle}.json"
        self.fontName = font
        self.flagFunc = flagFunc
        self.accent = accent
        self.userEmail = userEmail

        # Dictionary for title heading sizes based on font name.
        self.fontsDict = {"Bahnschrift":["Bahnschrift",32],
                          "Georgia":["Georgia",32],
                          "Franklin Gothic Demi":["Franklin Gothic Demi",32],
                          "Cascadia Code":["Cascadia Code",28],
                          "Century Gothic":["Century Gothic",30],
                          "Calibri":["Calibri",34],
                          "Wingdings":["Wingdings",30]}

        # Gets listID and list of users with shared access from the list JSON file.
        with open(self.listPath,"r") as f:
            # Uses json.load to retrieve a JSON object of the list dictionary.
            theList = json.load(f)
            self.listID = theList["listID"]
            if theList["shared"] == "no":
                self.usersWithAccess = []
            else:
                self.usersWithAccess = theList["shared"]

            try:
                self.requestsSent = theList["requestsSent"]
            except KeyError:
                self.requestsSent = []


        self.widgets()
        self.placeWidgets()

        self.grabWin()
        self.protocol("WM_DELETE_WINDOW",self.close_window)

        # Checking requests at the start of the program.
        self.checkRequestsAccepted()

        self.loadSharedUsers()
        
        self.mainloop()
    
    def close_window(self):
        if self.flagFunc != None:
            self.flagFunc()
        
        self.destroy()
    
    def grabWin(self):
        self.grab_set()
        self.lift()
        self.after(1000,self.grab_release)
        self.entryEmail.focus()
        
    
    def widgets(self):
        globalFontName = self.fontName
        self.frameWin = CTkFrame(self,width=480,height=630,corner_radius=20,
                                 border_width=4,border_color="grey4",fg_color=("white","gray9"))
        
        # Title is created.
        titleFontSize = self.fontsDict[globalFontName][1]

        # Wraps title length to fit within page, and adds "..." to end if it has been shortened.
        # textwrap.wrap() returns a list
        titleWrapped = textwrap.wrap(self.listTitle,20)[0]
        if len(titleWrapped) < len(self.listTitle):
            titleWrapped += "..."

        # Creates title and subtitle labels
        self.lblTitle = CTkLabel(self.frameWin,text=f"Share '{titleWrapped}'.",
                                 font=(globalFontName,titleFontSize))
        
        self.lblSubtitle = CTkLabel(self.frameWin,
                                    text="Enter the email address of another Tickd user to send them\nan invitation for access to this list.",
                                    font=(globalFontName,16),justify="left")
        
        self.lblNoUsers = CTkLabel(self.frameWin,text=f"You have shared with no users.'.",
                                 font=(globalFontName,titleFontSize-5))
        
        imgLogo = CTkImage(Image.open("logo//whiteBGLogo.png"),
                           Image.open("logo//blackBGLogo.png"),
                           size=(106,34))
        self.logoPanel = CTkLabel(self.frameWin,text="",image=imgLogo)

        # Creates email entry and add/submit button
        self.entryEmail = CTkEntry(self.frameWin,placeholder_text="email",width=370,font=(globalFontName,22),corner_radius=25)
        self.btnAdd = SubmitButton(self.frameWin,command=self.addRecipientClicked,colour=self.accent,icon="add",buttonSize=(28,28))

        self.frameSharedUsers = CTkScrollableFrame(self,width=410,height=360,fg_color=("white","gray9"))
        self.sharedUsers = []

        self.bind("<Return>",lambda event:self.addRecipientClicked())
    
    def placeWidgets(self):
        self.frameWin.place(relx=0.5,rely=0.5,anchor=CENTER)
        
        # Makes use of anchor=CENTER to keep widget centred.
        # Alters relx to move widget slightly.
        self.lblTitle.place(relx=0.5,y=65,anchor=CENTER)
        self.logoPanel.place(relx=0.5,y=30,anchor=CENTER)
        self.lblSubtitle.place(in_=self.lblTitle,relx=0.5,y=85,anchor=CENTER)
        self.entryEmail.place(in_=self.lblSubtitle,y=60,relx=0.42,anchor=CENTER)
        self.btnAdd.place(in_=self.entryEmail,x=375)



    def loadSharedUsers(self):
        for each in self.usersWithAccess:
            self.placeSharedUser(self.listTitle,self.userEmail,each)
        
        if len(self.sharedUsers) != 0:
            self.frameSharedUsers.place(in_=self.lblSubtitle,y=80)
        else:
            self.lblNoUsers.place(in_=self.lblSubtitle,y=80)

    
    def placeSharedUser(self,listName,sender,recipient):
        # Creates new container object.
        sharedUserObj = SharedContainer(self.frameSharedUsers,self,self.listTitle,
                                            self.userEmail,recipient,self.listID,self.fontName,self.accent)
        
        # Places in scrollable frame.
        if len(self.sharedUsers) == 0:
            sharedUserObj.grid(row=0,column=0,pady=10)
        else:
            sharedUserObj.grid(row=len(self.sharedUsers),column=0,pady=(5,10))
        self.sharedUsers.append(sharedUserObj)

    def addRecipientClicked(self):
        userInput = self.entryEmail.get().strip()

        # First check that input is a valid email
        inputValid = checkEmail(userInput)

        if not inputValid:
            messagebox.showerror("Can't share list","The email you have entered is invalid.\nPlease try again.")
            self.grabWin()
        else:
            userRegistered,_ = checkDetailsFound(userInput)

            if not userRegistered:
                messagebox.showerror("Can't share list","We couldn't find a registered user with that email.\nPlease try again.")
            elif userInput.lower() == self.userEmail:
                messagebox.showerror("Can't share list","You cannot share your own list with yourself.\nPlease try again.")
            elif userInput.lower() in self.usersWithAccess:
                messagebox.showerror("Can't share list",
                                     "You have already shared the list with this user.\nYou can view users with access or revoke their access below.")
            elif userInput.lower() in self.requestsSent:
                messagebox.showinfo("Can't share list","You have already invited this user to this list.\nPlease wait for them to accept or decline the request.")
            else:
                self.sendRequest(userInput.lower())
            self.grabWin()

    def sendRequest(self,recipient):
        # Forms path of recipient's shared file and gets previous contents.
        recipientPath = f"users//{recipient}//shared.json"
        with open(recipientPath,"r") as f:
            recipientShared = json.load(f)

        try:
            # Tries to add listID to already existing list under user email in requests section of shared file.
            userSharedList = recipientShared["requests"][self.userEmail]
            if self.listID not in userSharedList:
                recipientShared["requests"][self.userEmail].append(self.listID)
                messagebox.showinfo("Invitation sent",f"Invitation sent to {recipient}\nIf they accept, they will be able to view this list in their account.\nYou can also revoke access at any time from this screen.")
                self.addToRequestsSent(recipient)
                self.grabWin()
            else:
                messagebox.showinfo("User already invited","This user has already been sent an invitation for access to this list.")
                self.grabWin()

        except KeyError:
            # No section exists called requests, or there is no section under the sender's email, so it is created.
            recipientShared["requests"][self.userEmail] = []
            recipientShared["requests"][self.userEmail].append(self.listID)
            messagebox.showinfo("Invitation sent",f"Invitation sent to {recipient}\nIf they accept, they will be able to view this list in their account.\nYou can also revoke access at any time from this screen.")
            self.addToRequestsSent(recipient)
            self.grabWin()
        
        with open(recipientPath,"w") as f:
            # Rewrites the contents.
            json.dump(recipientShared,f,indent=4)
        
        

        # Removes contents of entry box.
        self.entryEmail.delete(0,END)

    
    def addToRequestsSent(self,userToAdd):
        # Makes a record of which users have been sent requests.
        
        with open(self.listPath,"r") as f:
            # Uses json.load to retrieve a JSON object of the list dictionary.
            theList = json.load(f)
        

        try:
            theList["requestsSent"].append(userToAdd)
        except KeyError:
            theList["requestsSent"] = [userToAdd]
        
        with open(self.listPath,"w") as f:
            json.dump(theList,f,indent=4)
    

    def checkRequestsAccepted(self):
        # Checks through each of the users in "requestsSent" section.
        # Checks if they have accepted their request or not.

        # Get requestsSent list.
        with open(self.listPath,"r") as f:
            # Uses json.load to retrieve a JSON object of the list dictionary.
            theList = json.load(f)
            try:
                requestsSent = theList["requestsSent"]
            except KeyError:
                requestsSent = []
        
        requestsToRemove = []
        acceptedRequests = []
        for recipient in requestsSent:
            recipientPath = f"users//{recipient}//shared.json"

            with open(recipientPath,"r") as f:
                recipientShared = json.load(f)
            
            if self.listID in recipientShared["requests"][self.userEmail]:
                # Request has been sent, but not accepted.
                pass
            elif self.listID not in recipientShared["requests"][self.userEmail]:
                # Not in requests section, has either been accepted or declined.
                requestsToRemove.append(recipient)

                # Checking if accepted.
                try:
                    if self.listID in recipientShared[self.userEmail]:
                        # Request has been accepted.
                        acceptedRequests.append(recipient)
                except KeyError:
                    # Request has not been accepted.
                    pass

        # Remove finished requests (accepted or declined)
        for each in requestsToRemove:
            theList["requestsSent"].remove(each)
        
        # Add accepted requests
        for each in acceptedRequests:
            try:
                theList["shared"].append(each)
                self.usersWithAccess.append(each)
            except AttributeError:
                theList["shared"] = [each]
                self.usersWithAccess.append(each)
        
        # Overwrite previous contents.
        with open(self.listPath,"w") as f:
            json.dump(theList,f,indent=4)
    
    def removeUserFromList(self,removeIndex):
        # Removes all shared users from the one to remove till the end.
        for each in range(removeIndex,len(self.sharedUsers)):
            self.sharedUsers[each].grid_forget()
        
        # Removes actual request.
        self.sharedUsers.remove(self.sharedUsers[removeIndex])

        # Replaces all of the previously removed ones.
        for i in range(removeIndex,len(self.sharedUsers)):
            self.sharedUsers[i].grid(row=i,column=0,pady=(5,10))
        
        if len(self.sharedUsers) == 0:
            self.frameSharedUsers.place_forget()
            self.lblNoUsers.place(in_=self.lblSubtitle,y=70)

    def revokeAccess(self,user):
        # Remove from shared section
        with open(self.listPath,"r") as f:
            theList = json.load(f)
        
        theList["shared"].remove(user)

        with open(self.listPath,"w") as f:
            json.dump(theList,f,indent=4)
    
        # Remove from their shared file
        with open(f"users//{user}//shared.json","r") as f:
            sharedList = json.load(f)
        
        sharedList[self.userEmail].remove(self.listID)

        with open(f"users//{user}//shared.json","w") as f:
            json.dump(sharedList,f,indent=4)
        

        # Remove from the list.
        indexToRemove = ""
        for each in self.sharedUsers:
            if each.recipient == user:
                indexToRemove = self.sharedUsers.index(each)
                break
        self.removeUserFromList(indexToRemove)

        messagebox.showinfo("User access removed",f"You have removed list access for {user}.")
        self.grabWin()

class RequestsMenu(CTkFrame):
    # Shows requests that a user has received for list access.

    def __init__(self,master,email,font="Bahnschrift",accent="dodgerblue2"):
        super().__init__(master,width=430,height=460,corner_radius=20,border_width=4,
                         border_color="grey4",fg_color=("white","gray9"))
        
        self.userEmail = email
        self.font = font
        self.accent = accent

        self.widgets()
        self.placeWidgets()
        self.getRequests()

    def widgets(self):
        globalFontName = self.font

        # Defines key labels
        self.lblTitle = CTkLabel(self,text=f"Requests.",
                                 font=(globalFontName,25))
        self.lblSubtitle = CTkLabel(self,
                                    text="Check your invitations for list access to shared lists here.",
                                    font=(globalFontName,14),justify="left")
        
        self.lblNoRequests = CTkLabel(self,text=f"You have no requests.",
                                 font=(globalFontName,25))
        
        # Defines close button - similar to details panel.
        self.imgClose = CTkImage(Image.open("icons//cancel.png"),size=(20,20))
        self.btnClose = CTkButton(self,image=self.imgClose,text="",width=20,fg_color="grey12",hover_color="red",\
                                  border_color="grey5",border_width=2,command=self.place_forget)
        
        # Scrollable frame to hold requests.
        self.frameRequests = CTkScrollableFrame(self,width=370,height=300,fg_color=("white","gray9"))
        self.requestsList = []

        #self.sampleRequest = RequestContainer(self.frameRequests,"Test","omar@gmail.com",self.userEmail,self.font,self.accent)

        
        
    
    def placeWidgets(self):
        self.lblTitle.place(x=20,y=20)
        self.btnClose.place(in_=self.lblTitle,x=350)
        self.lblSubtitle.place(in_=self.lblTitle,y=30)
        self.frameRequests.place(in_=self.lblSubtitle,y=50)

        #self.sampleRequest.grid(row=0,column=0,pady=10)

    def getRequests(self):
        # Opening shared file to see requests.
        with open(f"users//{self.userEmail}//shared.json","r") as f:
            theList = json.load(f)
            requests = theList["requests"]

        for user in requests:
            for listID in requests[user]:
                # Goes to user who sent the request
                # Checks under listID

                sender = user

                listName = self.checkListID(user,listID)
                if listName != False:
                    self.placeRequest(listName,sender,listID)
        
        if len(self.requestsList) == 0:
            self.frameRequests.place_forget()
            self.lblNoRequests.place(in_=self.lblSubtitle,y=70)
        else:
            self.frameRequests.place(in_=self.lblSubtitle,y=50)

    def placeRequest(self,listName,sender,listID):
        # Creates new container object.
        request = RequestContainer(self.frameRequests,self,listName,sender,
                                   self.userEmail,listID,self.font,self.accent)
        
        # Places in scrollable frame.
        if len(self.requestsList) == 0:
            request.grid(row=0,column=0,pady=10)
        else:
            request.grid(row=len(self.requestsList),column=0,pady=(5,10))
        self.requestsList.append(request)
        
    def removeRequestFromList(self,removeIndex):
        # Removes all requests from the one to remove till the end.
        for each in range(removeIndex,len(self.requestsList)):
            self.requestsList[each].grid_forget()
        
        # Removes actual request.
        self.requestsList.remove(self.requestsList[removeIndex])

        # Replaces all of the previously removed ones.
        for i in range(removeIndex,len(self.requestsList)):
            self.requestsList[i].grid(row=i,column=0,pady=(5,10))
        
        if len(self.requestsList) == 0:
            self.frameRequests.place_forget()
            self.lblNoRequests.place(in_=self.lblSubtitle,y=70)

    def acceptRequest(self,listID,sender):
        # Moves listID from requests into an entry in the actual shared file.

        with open(f"users//{self.userEmail}//shared.json","r") as f:
            theList = json.load(f)
        
        # Removes request.
        theList["requests"][sender].remove(listID)

        # Adds listID to main menu.
        try:
            theList[sender].append(listID)
        except KeyError:
            theList[sender] = [listID]

        # Overwrite previous contents of shared file
        with open(f"users//{self.userEmail}//shared.json","w") as f:
            json.dump(theList,f,indent=4)
        
        requestListName = ""
        requestSender = ""
        # Remove request from menu.
        for each in self.requestsList:
            if each.listID == listID:
                requestListName = each.listName
                requestSender = each.sender
                removeIndex = self.requestsList.index(each)
                self.removeRequestFromList(removeIndex)
        
        # Remove request on sender's end
        with open(f"users//{requestSender}//{requestListName}.json","r") as f:
            senderList = json.load(f)
        
        # Adds user to shared section of list.
        try:
            senderList["shared"].append(self.userEmail)
        except AttributeError:
            senderList["shared"] = [self.userEmail]  

        # Removes user from requests sent, since they are now a shared user.     
        senderList["requestsSent"].remove(self.userEmail)

        # Overwrites previous contents of list.
        with open(f"users//{requestSender}//{requestListName}.json","w") as f:
            json.dump(senderList,f,indent=4)

        messagebox.showinfo("Request accepted",f"You have accepted the request for '{requestListName}' from {requestSender}. ")

        # Adds list to user's shared lists menu.
        self.master.placeSharedList(listName=requestListName,listOwner=requestSender)
        self.place_forget()




    def declineRequest(self,listID,sender):

        # Opens users's shared file to remove the request.
        with open(f"users//{self.userEmail}//shared.json","r") as f:
            sharedFile = json.load(f)

        # Removes list ID from requests section under sender name.
        sharedFile["requests"][sender].remove(listID)

        # Overwriting previous contents of shared file.
        with open(f"users//{self.userEmail}//shared.json","w") as f:
            json.dump(sharedFile,f,indent=4)

        requestListName = ""
        requestSender = ""
        # Remove request from menu.
        for each in self.requestsList:
            if each.listID == listID:
                requestListName = each.listName
                requestSender = each.sender
                removeIndex = self.requestsList.index(each)
                self.removeRequestFromList(removeIndex)
        
        # Remove request on sender's end
        with open(f"users//{requestSender}//{requestListName}.json","r") as f:
            senderList = json.load(f)
        
        # Removes on sender's end
        senderList["requestsSent"].remove(self.userEmail)

        with open(f"users//{requestSender}//{requestListName}.json","w") as f:
            json.dump(senderList,f,indent=4)
        
        messagebox.showinfo("Request declined",f"You have declined the request for '{requestListName}' from {requestSender}. ")


    def checkListID(self,userEmail,listID):
        path = f"users//{userEmail}//*.json"

        # Gets all of the lists in the sharing user's account.
        userLists = glob(path)
        for each in userLists.copy():
            if "inbox" in each or "shared" in each:
                # Removes inbox and shared file.
                userLists.remove(each)
        
        # Checks each list, compares listID to provided one
        for each in userLists:
            with open(each,"r") as f:
                theList = json.load(f)
                foundListID = theList["listID"]

            if foundListID == listID:
                print("Found list")
                # Takes path from the glob procedure, removes unnecessary details
                # Leaves with actual list name.
                listNameSplit = each.split("\\")
                listName = listNameSplit[1]
                listName = listName.replace(".json","")
                
                return listName
            
        # If no list name found.
        return False
            
class RequestContainer(CTkFrame):
    def __init__(self,master,mainMenu,listName,sender,recipient,listID,font="Bahnschrift",accent="dodgerblue2"):
        super().__init__(master=master,width=360,height=70,fg_color=("white","gray13"),border_color=("gray","gray15"),\
                         border_width=3,cursor="hand2",corner_radius=10)
        
        # Creates key attributes
        self.mainMenu = mainMenu
        self.listName = listName
        self.font = font
        self.accent = accent
        self.sender = sender
        self.recipient = recipient
        self.listID = listID

        self.widgets()
        self.placeWidgets()
        
    def widgets(self):
        globalFontName = self.font
        self.lblListName = CTkLabel(self,text=f"{self.listName}",font=(globalFontName,20))
        self.lblSharedBy = CTkLabel(self,text=f"Shared by {self.sender}.",
                                    font=(globalFontName,14),justify="left")

        # Defining binding of attributing for text highlighting
        # Similar to task class - highlighting text when hovering over it.
        self.lblListName.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblListName.bind("<Leave>",lambda event:self.onmouseLeave())
        self.lblSharedBy.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblSharedBy.bind("<Leave>",lambda event:self.onmouseLeave())

        # Defines two buttons.
        self.listImgs = getListImgs((20,20))
        self.btnDecline = CTkButton(self,image=self.listImgs["Cancel"],text="",width=20,fg_color="grey12",hover_color="red",\
                                  border_color="grey5",border_width=2,command=self.btnDeclineClicked)
        self.btnAccept = CTkButton(self,image=self.listImgs["Tick"],text="",width=20,fg_color="grey12",hover_color="limegreen",\
                                  border_color="grey5",border_width=2,command=self.btnAcceptClicked)
        
        
    def placeWidgets(self):
        self.lblListName.place(x=20,y=10)
        self.lblSharedBy.place(in_=self.lblListName,y=25)
        self.btnAccept.place(in_=self.lblListName,x=250)
        self.btnDecline.place(in_=self.btnAccept,x=40)
    
    def onmouseEnter(self):
        self.lblListName.configure(text_color=self.accent)
    
    def onmouseLeave(self):
        self.lblListName.configure(text_color=("black","white"))

    def btnAcceptClicked(self):
        self.mainMenu.acceptRequest(self.listID,self.sender)
    
    def btnDeclineClicked(self):
        # Asks again whether user definitely wants to reject request.
        check = messagebox.askyesno("Are you sure?","Are you sure you would like to cancel the request?")

        if check:
            self.mainMenu.declineRequest(self.listID,self.sender)

class SharedContainer(CTkFrame):
    def __init__(self,master,mainMenu,listName,sender,recipient,listID,font="Bahnschrift",accent="dodgerblue2"):
        super().__init__(master=master,width=400,height=50,fg_color=("white","gray13"),border_color=("gray","gray15"),\
                         border_width=3,cursor="hand2",corner_radius=10)
        
        # Creates key attributes
        self.mainMenu = mainMenu
        self.listName = listName
        self.font = font
        self.accent = accent
        self.sender = sender
        self.recipient = recipient
        self.listID = listID

        self.widgets()
        self.placeWidgets()
        
    def widgets(self):
        globalFontName = self.font
        self.lblSharedUser = CTkLabel(self,text=f"{self.recipient}",font=(globalFontName,22))

        # Defining binding of attributing for text highlighting
        # Similar to task class - highlighting text when hovering over it.
        self.lblSharedUser.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblSharedUser.bind("<Leave>",lambda event:self.onmouseLeave())

        # Defines two buttons.
        self.listImgs = getListImgs((20,20))
        self.btnDecline = CTkButton(self,image=self.listImgs["Cancel"],text="",width=20,fg_color="grey12",hover_color="red",\
                                  border_color="grey5",border_width=2,command=self.btnDeclineClicked)
        
        
    def placeWidgets(self):
        self.lblSharedUser.place(x=20,y=10)
        self.btnDecline.place(in_=self.lblSharedUser,x=320)
    
    def onmouseEnter(self):
        self.lblSharedUser.configure(text_color=self.accent)
    
    def onmouseLeave(self):
        self.lblSharedUser.configure(text_color=("black","white"))
    
    def btnDeclineClicked(self):
        # Asks again whether user definitely wants to reject request.
        check = messagebox.askyesno("Are you sure?",f"Are you sure you would like to remove list access for {self.recipient}?")

        if check:
            self.mainMenu.revokeAccess(self.recipient)

class SharedListContainer(CTkFrame):
    def __init__(self,master,listName,listOwner,command,commandArgs=None,font="Bahnschrift",accent="dodgerblue2"):
        # Calls super class to create a frame.
        super().__init__(master,width=350,height=80,corner_radius=20,border_width=3,
                         border_color="black",fg_color="grey18",cursor="hand2")
    
        # Defining key attributes 
        self.listName = listName
        self.listOwner = listOwner
        self.command = command
        self.fontName = font
        self.accent = accent

        self.widgets()
        self.placeWidgets()

        # Binds all of the widgets to call the hover procedure when hovered over.
        self.bind("<Enter>",lambda event:self.onHover())
        self.bind("<Leave>",lambda event:self.onHoverExit())
        self.lblListName.bind("<Enter>",lambda event:self.onHover())
        self.lblListName.bind("<Leave>",lambda event:self.onHoverExit())
        self.lblSharedBy.bind("<Enter>",lambda event:self.onHover())
        self.lblSharedBy.bind("<Leave>",lambda event:self.onHoverExit())
        
        # Binds labels to call the command when they are clicked.
        if commandArgs != None:
            self.bind("<Button-1>",lambda event:self.command(**commandArgs))
            self.lblListName.bind("<Button-1>",lambda event:self.command(**commandArgs))
            self.lblSharedBy.bind("<Button-1>",lambda event:self.command(**commandArgs))
        else:
            self.bind("<Button-1>",lambda event:self.command())
            self.lblListName.bind("<Button-1>",lambda event:self.command())
            self.lblSharedBy.bind("<Button-1>",lambda event:self.command())


    def widgets(self):
        # Creates two widgets.
        self.lblListName = CTkLabel(self,text=self.listName,font=(self.fontName,25))
        self.lblSharedBy = CTkLabel(self,text=f"Shared by {self.listOwner}",font=(self.fontName,16))

    def placeWidgets(self):
        # Places label widgets
        self.lblListName.place(x=15,y=10)
        self.lblSharedBy.place(in_=self.lblListName,y=30)
    
    def onHover(self):
        # Changes background colour to a lighter grey.
        self.configure(fg_color="grey24")
    
    def onHoverExit(self):
        # Changes background colour back to the previous colour.
        self.configure(fg_color="grey18")



"""root = CTk()
sharedlist = SharedListContainer(root,"Psych blurts","amoghg75@yahoo.com",None,None,)
sharedlist.pack()

root.mainloop()"""