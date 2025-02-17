# Amogh NG
# All login screen classes (auth window, reset password window, register window.)

from customtkinter import *
from PIL import Image
import json
from lib.checkbox_customTk import Checkbox
from lib.getDetails import getAllDetails
from lib.checkWithPepper import checkWithPepper
from tkinter import messagebox
from lib.uploadTask import uploadTask
from lib.createUserFolder import createUserFolder
from lib.genHash import genHash
from datetime import date
import lib.getWallpaper as getWallpaper
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint


class Auth(CTk):
    globalFontName = "Bahnschrift"
    buttonFont = (globalFontName,25)
    emojiFont = ("Segoe UI Emoji",30)
    accent = "crimson"

    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.minsize(600,400)
        self.maxsize(600,400)
        self.title("Log in - Tickd")
        self.iconbitmap("logo//tickd.ico")

        self.loggedIn = False


        set_appearance_mode("dark")
        self.theme = "dark"
        
        
        self.widgets()
        self.placeWidgets()
        

        self.bind("<Return>",lambda event:self.signInClicked())

        self.registerWinOpen = False
        self.resetWinOpen = False
        
        self.checkRememberMe()

        self.mainloop()
        
        

    def widgets(self):
        globalFontName = self.globalFontName
        emojiFont = self.emojiFont
        buttonFont = self.buttonFont

        # Creates frame for the actual content.
        self.frameLogin = CTkFrame(self,width=560,height=370,corner_radius=20,border_color=("gray","gray7"),border_width=5,fg_color=("white","#171616"))
        
        # Defines light/dark mode button.
        self.imgMode = CTkImage(light_image=Image.open("logo//moon.png"),dark_image=Image.open("logo//sun.png"),size=(35,35))
        self.btnMode = CTkButton(self.frameLogin,image=self.imgMode,text="",command=self.changeMode,width=1,fg_color="#252425",
                                 hover_color=self.accent,corner_radius=50)
        
        # Defines logo image object and logo panel.
        self.logo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(282,90)) #Ratio 330x105
        self.logoPanel = CTkLabel(self.frameLogin,text="",image=self.logo)
        
        # Creates email and password entries and labels.
        self.entryEmail = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameLogin,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameLogin,font=emojiFont,text="🔒")
        
        # Creates images for the show and hide password button (actually two separate identical buttons apart from the image.)
        self.imgShowPassword = CTkImage(Image.open("icons//eyeIcon.png"),size=(32,24))
        self.btnShowPassword = CTkButton(self.frameLogin,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("icons//eyeIconOff.png"),size=(32,24))
        self.btnHidePassword = CTkButton(self.frameLogin,image=self.imgHidePassword,text="",
                                         width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.btnRegister = CTkButton(self.frameLogin,text="register",font=buttonFont,corner_radius=15,text_color="white",
                                     border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.createRegisterWindow)
        

        self.btnSignIn = CTkButton(self.frameLogin,text="sign in",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color="white",
                                   border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        


        # Creates Remember me checkbox and label, and forgot password label.
        self.checkboxRememberMe = Checkbox(self.frameLogin,x=0,y=50,size=(35,35),relWidget=self.entryPassword)

        self.lblRememberMe = CTkLabel(self.frameLogin,text="remember me",font=(globalFontName,25),text_color=("black","white"),cursor="hand2")
        self.lblRememberMe.bind("<Button-1>",lambda event: self.checkboxRememberMe.boxClicked(event))

        self.lblForgotPassword = CTkLabel(self.frameLogin,font=(globalFontName,22),text="forgot your password?",cursor="hand2")
        self.lblForgotPassword.bind("<Enter>",lambda event: self.forgotLblEnter())
        self.lblForgotPassword.bind("<Leave>",lambda event: self.forgotLblLeave())
        self.lblForgotPassword.bind("<Button-1>",lambda event: self.createResetWindow())

        self.imgTick = CTkImage(Image.open("logo//tick.png"),size=(35,35))
        self.lblLoggingIn = CTkLabel(self.frameLogin,font=(globalFontName,22),text=" Logging in.",text_color="limegreen",image=self.imgTick,compound="left")
        
        self.elements = {
            "lblEmail":self.lblEmail,
            "lblPassword":self.lblPassword,
            "entryEmail":self.entryEmail,
            "entryPassword":self.entryPassword,
            "btnRegister":self.btnRegister,
            "btnSignIn":self.btnSignIn,
            "btnShowPassword":self.btnShowPassword,
            "btnHidePassword":self.btnHidePassword,
            }
        

    def placeWidgets(self):
        #self.panelImgBG.place(x=0,y=0)
        self.frameLogin.place(relx=0.5,rely=0.5,anchor="center")
        self.logoPanel.place(relx=0.25,rely=0.05)
        self.btnMode.place(in_=self.logoPanel,x=330,y=-5)
        self.entryEmail.place(in_=self.logoPanel,x=-60,y=105)
        self.entryPassword.place(in_=self.entryEmail,y=50)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-5)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-5)
        self.btnShowPassword.place(in_=self.entryPassword,x=405,y=1)
        self.btnRegister.place(in_=self.entryPassword,x=50,y=100)
        self.btnSignIn.place(in_=self.btnRegister,x=150)
        self.checkboxRememberMe.placeWidget()
        self.lblRememberMe.place(in_=self.entryPassword,x=40,y=52)
        self.lblForgotPassword.place(in_=self.btnRegister,x=50,y=50)
        
        
    def changeMode(self):
        if get_appearance_mode() == "Light":
            self.theme = "dark"
            set_appearance_mode("Dark")

            # Sets button to a dark colour (dark-greyish)
            self.btnMode.configure(fg_color="#252425")
        else:
            self.theme = "light"
            set_appearance_mode("Light")

            # Sets button to a light colour
            self.btnMode.configure(fg_color="#eaeaeb")
    
    def forgotLblEnter(self):
        self.hoverOriginalFont = self.lblForgotPassword._font
        newFont = (self.hoverOriginalFont[0],self.hoverOriginalFont[1],"underline")
        self.lblForgotPassword.configure(font=newFont,text_color=self.accent)
    
    def forgotLblLeave(self):
        self.lblForgotPassword.configure(font=self.hoverOriginalFont,text_color=("black","white"))

    def createResetWindow(self):
        if self.resetWinOpen:
            messagebox.showinfo("Window already active","Reset password window already active.")
            #self.setMessage("Reset password window already active.")
        else:
            self.resetWinOpen = True
            # Replace "no" with self.imgBGPath
            self.resetWin = ResetPassword("no",self.accent,origin=self)

    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=405,y=1)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=405,y=1)
            self.entryPassword.configure(show="*")


    def checkDetailsFound(self,email,details):
        found = False
        for each in details: # Selects each sublist in the large overall list of details.
            if each[0] == email: # Uses format [email,password,username] so each[0] means the email.
                userDetails = each
                found = True
        if found == False:
            print("No details found.")
            userDetails = []    

        return found, userDetails
    
    def checkEmpty(self,email,password):
        emailEmpty = False
        passwordEmpty = False

        email = email.strip() # Removes any unnecessary whitespace in the entry boxes.

        if email == "" and password == "":
            emailEmpty = True
            passwordEmpty = True
        elif email == "":
            messagebox.showerror("Can't sign in to Tickd.","Please enter your email.")
            emailEmpty = True
        elif password == "":
            passwordEmpty = True
        
        return emailEmpty, passwordEmpty

    def checkEmail(self,email):
        if "@" in email:
            splitEmail = email.split("@")
            # Splits the email into two parts, e.g. john@gmail.com -> ["john","gmail.com"]
            if "." in splitEmail[1]:
                return True
            else:
                return False
        else: # The entered email contains no "@" symbol.
            return False 

    def setMessage(self,message,colour="white"):
        lblMessage = self.lblMessage
        btnRegister = self.btnRegister
        fontSize = 20

        if colour == "white" or colour == "black":
            colour = ("black","white")

        if "\n" in message:
            splitMsg = message.split("\n")
            msgRef = min(splitMsg)
        else:
            msgRef = message
        
        increment = 50-len(msgRef)

        x = increment * 6

        
        lblMessage.place(x=x,rely=0.8)


        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)

    """def setMessage(self,message,colour):
        length = len(message)
        lblMessage = self.lblMessage
        btnRegister = self.btnRegister

        print(repr(message))
        
        increment=0 # Used to increase the distance the widget is placed to the right. Used for larger messages.
        if length>=45 and not "\n" in message:
            increment=20
        elif length > 45:
            increment = 150
        elif length>35:
            increment = 50 
        
        fontSize = 25
        x=160+increment-(7*length)
        lblMessage.place(in_=btnRegister,x=x,y=70)
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)"""

    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEmail.focus_set()


    def signInClicked(self):
        email = self.entryEmail.get().lower()
        passwordTxt = self.entryPassword.get()
        
        details,_ = getAllDetails()
        
        emailEmpty, passwordEmpty = self.checkEmpty(email, passwordTxt)
        emailValid = self.checkEmail(email)
        found,self.userDetails = self.checkDetailsFound(email,details)
        

        if emailEmpty and passwordEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your details.")
        elif emailEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your email.")
            self.resetEntry(["entryPassword"])
        elif passwordEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your password.")
        else:
            if emailValid and not found:
                messagebox.showerror("Details not found.","These details have not been found.\n\
                                     Please click 'register' if you do not already have an account.")
            elif not emailValid:
                messagebox.showerror("Can't sign in to Tickd.","Please enter a valid email.")
                self.resetEntry(["entryPassword","entryEmail"])
            else:
                correctPasswordTxt = self.userDetails[1]
                correctPWSplit = correctPasswordTxt.split("$")
                passwordWithSalt = correctPWSplit[0]+passwordTxt
                correct = checkWithPepper(passwordWithSalt,correctPWSplit[1])             

                if correct:
                    self.resetEntry(["entryEmail","entryPassword"])
                    
                    self.userLoginSequence()
                    self.signIn(self.userDetails)
                    self.lblForgotPassword.place_forget()
                    self.lblLoggingIn.place(in_=self.btnRegister,x=65,y=50)
                    self.after(1500,self.destroy)
                else:
                    messagebox.showerror("Can't sign in to Tickd.","Incorrect password.")
                    #self.setMessage("Incorrect password.","red")
                    self.resetEntry(["entryPassword"])
                    self.entryPassword.focus()

    def clickablesOnOff(self):
        clickables = []
        elements = self.elements
        for each in elements:
            if "entry" in each or "btn" in each:
                clickables.append(elements[each])
        
        for clickable in clickables:
            try:
                if clickable.cget("state") == "normal":
                    clickable.configure(state="disabled")
                else:
                    clickable.configure(state="normal")
            except:
                pass

    

    def rememberMeConfirmClicked(self):
        self.loggedInEmail = self.rememberedEmail
        self.userPath = f"users//{self.loggedInEmail}"

        self.loggedIn = True
        self.after(1000,self.destroy)
    
    def signIn(self,userDetails):
        # Uses email that has been verified.
        self.rememberedEmail = userDetails[0]
        
        if not self.loggedIn:
            # Message box returns either True or False if yes or no clicked.
            rememberMeInput = messagebox.askyesno("Automatic sign-in",f"Login automatically as\n{self.rememberedEmail}?")
            
            if rememberMeInput:
                self.rememberMeConfirmClicked()

        else:
            self.loggedInEmail = self.rememberedEmail
            self.userPath = f"users//{self.loggedInEmail}"


    def createRegisterWindow(self):
        if self.registerWinOpen:
            messagebox.showinfo("Window already active","Register window already active.")
        else:
            self.registerWinOpen = True
            self.registerWindow = Register()
            self.imgBGPath = None
            self.registerWindow.initialise(self.imgBGPath,self.accent,origin=self)
        
    def userLoginSequence(self):
        # Takes value from checkbox using public getter
        rememberMeVal = self.checkboxRememberMe.getValue()
        
        # Retrieves all auth details from JSON file using pre-written function (from lib)
        # Second underscore is for old remember me index, which is not needed.
        details,_ = getAllDetails()
        
        
        if rememberMeVal:
            newRememberMeIndex = details.index(self.userDetails)
        else:
            newRememberMeIndex = "False"

        newAuthDetails = {"details":details,"rememberMe":newRememberMeIndex}
        # Rewrites auth details dictionary using new Remember me index.
        
        with open("authDetails.json","w") as f:
            json.dump(newAuthDetails,f,indent=4)
            # Writes JSON object to file with indenting to make it look readable. 
        
        self.loggedIn = True
        # Allows user to sign into main app.
    
    def checkRememberMe(self):
        print("hello")
        details,rememberMeIndex = getAllDetails()
        if rememberMeIndex != "False":
            userDetails = details[rememberMeIndex]
            self.signIn(userDetails)

class Register(CTkToplevel):
    # This class doesn't have an __init__ function, to allow it to be stored in the Auth window.
    def initialise(self,imgBGPath=None,accent="dodgerblue2",origin=None):
        super().__init__()
        self.geometry("620x400")
        self.maxdims = [620,400]
        self.imagedims = [1280,1080]
        self.minsize(self.maxdims[0],self.maxdims[1])
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Register - Tickd")
        
        # This is to access the attributes of the Auth window class.
        self.origin = origin
        
        # Sets custom function to run when close window (x) button clicked.
        self.protocol("WM_DELETE_WINDOW",lambda:self.close_window())

        set_appearance_mode("dark")

        if imgBGPath == None:
            pass
        else:
            self.imgBGPath = imgBGPath

        self.accent = accent

        self.iconbitmap("logo//tickd.ico")
        
        self.widgets()
        self.placeWidgets()

        """
        """
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

        

        self.elements = {"entryEmail":self.entryEmail,
                         "entryPassword":self.entryPassword,
                         "entryUsername":self.entryUsername}
        

        self.mainloop()

    def close_window(self):
        # Sets flag back to False.
        self.origin.registerWinOpen = False

        # Kills window.
        self.destroy()

    def widgets(self):
        globalFontName = "Bahnschrift"
        emojiFont = ("Segoe UI Emoji",30)

        """if self.imgBGPath == None:
            self.imgBG,_ = getWallpaper.getRandom((self.imagedims[0],self.imagedims[1]))
        else:
            self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.imagedims[0],self.imagedims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)
"""
        self.frameRegister = CTkFrame(self,width=575,height=380,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.logoImg = CTkImage(dark_image=Image.open("logo//blackBGLogo.png"),light_image=Image.open("logo//whiteBGLogo.png"),size=(140,45))
        self.panelLogo = CTkLabel(self.frameRegister,text="",image=self.logoImg)
        self.registerLbl = CTkLabel(self.frameRegister,font=(globalFontName,35),text="Create your account.")

        self.entryEmail = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameRegister,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameRegister,font=emojiFont,text="🔒")
        self.entryUsername = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="username",corner_radius=15)
        self.lblUsername = CTkLabel(self.frameRegister,font=emojiFont,text="🧑")

        self.imgShowPassword = CTkImage(Image.open("icons//eyeIcon.png"),size=(33,24))
        self.btnShowPassword = CTkButton(self.frameRegister,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("icons//eyeIconOff.png"),size=(33,24))
        self.btnHidePassword = CTkButton(self.frameRegister,image=self.imgHidePassword,text="",width=0,command=self.showHide,corner_radius=15,fg_color=self.accent)

        self.btnRegister = CTkButton(self.frameRegister,text="register",font=(globalFontName,30),corner_radius=15,text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.registerClicked)
        self.messageVar = StringVar()
        self.messageVar.set("hello")
        self.lblMessage = CTkLabel(self.frameRegister,textvariable=self.messageVar,font=(globalFontName,25))

        self.btnCancel = CTkButton(self.frameRegister,text="cancel",font=(globalFontName,30),corner_radius=15,hover_color="red",text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.close_window)

    def placeWidgets(self):
        #self.panelImgBG.place(x=0,y=0)
        self.frameRegister.place(relx=0.5,rely=0.5,anchor="center")
        self.panelLogo.place(relx=0.35,y=20)
        self.registerLbl.place(in_=self.panelLogo,x=-85,y=45)

        self.entryEmail.place(x=95,y=120)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-3)

        # Previously, y gaps between entries were around 70.
        self.entryPassword.place(in_=self.entryEmail,y=55) # Changed to 55
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-3)
        self.entryUsername.place(in_=self.entryPassword,y=55) # Also changed to 55
        self.lblUsername.place(in_=self.entryUsername,x=-50,y=-3)

        self.btnShowPassword.place(in_=self.entryPassword,x=405,y=2)
        self.btnRegister.place(in_=self.entryUsername,x=45,y=70)
        self.btnCancel.place(in_=self.btnRegister,x=145)

        
    def createSampleTask(self):
        welcomeTaskDict = {"title":"Welcome to Tickd!",
                               "date":f"{date.today().strftime('%d/%m/%Y')}",
                               "description":"Welcome to a simpler life with Tickd.\nSimply add tasks with the 'Add a task' box at the top, and use keywords such as 'today' and 'tomorrow' in the date, or for other dates simply add the date using the DD/MM/YY format.\ne.g. for the 31st December 2025, you would put 31/12/25.",
                               "completed":"False",
                               "time":"",
                               "priority":"",
                               "taskID":"welcome",
                               "listName":"inbox"}
        uploadTask(self.userPath,welcomeTaskDict,"inbox")
    
    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=405,y=2)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=405,y=2)
            self.entryPassword.configure(show="*")
    
    def grabWin(self):
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

    def registerClicked(self):
        print("Hello")

        email = self.entryEmail.get().lower()
        password = self.entryPassword.get()
        username = self.entryUsername.get()
        
        details,rememberMeIndex = getAllDetails()
        
        empty = self.checkEmpty()
        
        if not empty:
            emailValid = self.checkEmail(email)
            found,self.userDetails = self.checkDetailsFound(email,details)
            if emailValid and found:
                # Message box used instead of calling setMessage procedure
                messagebox.showinfo("Cannot create new account","An account already exists with this email.")
                self.grabWin()
                self.resetEntry(["entryEmail"])
            elif not emailValid:
                # Message box also used here
                messagebox.showinfo("Cannot create new account","Please enter a valid email.")
                self.grabWin()
                self.entryEmail.focus_set()
                self.resetEntry(["entryEmail"])
            else:
                passwordToStore = genHash(password)
                newDetails = [email,passwordToStore,username]

                
                details.append(newDetails)
                newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

                print(newAuthDetails)
                
                with open("authDetails.json","w") as f:
                    json.dump(newAuthDetails,f,indent=4)
                
                with open("preferences.json","r") as f:
                    prefs = json.load(f)
                    prefs[email] = {"accent":"dodgerblue2"}

                with open("preferences.json","w") as f:
                    json.dump(prefs,f,indent=4)


                self.resetEntry(["entryEmail","entryPassword"])
                self.userPath = f"users//{email}"
                createUserFolder(self.userPath) # Creates new folder for the new user with one "inbox.json" list
                self.createSampleTask()

                messagebox.showinfo("Account created successfully.","Your account has been created.\nPlease log in using your details.")
                self.origin.registerWinOpen = False
                self.origin.entryEmail.insert(0,email)
                self.origin.entryPassword.focus()
                self.destroy()
 
    #-------# Entry validation funcs #-------#

    def checkDetailsFound(self,email,details):
        found = False
        for each in details:
            if each[0] == email:
                userDetails = each
                found = True
        if found == False:
            print("No details found.")
            userDetails = []

        return found, userDetails
    
    def checkEmpty(self):        
        userEntryTexts = [self.entryEmail.get(),self.entryPassword.get(),self.entryUsername.get()]
        for each in userEntryTexts:
            if each.strip() == "":
                messagebox.showinfo("Cannot create new account","Please fill out all fields.")
                self.grabWin()
                return True
        return False
    

    def checkEmail(self,email):
        if "@" in email:
            splitEmail = email.split("@")
            if "." in splitEmail[1]:
                return True
            else:
                return False
        else:
            #self.setMessage("Invalid email entered.","red")
            messagebox.showinfo("Cannot create new account","Invalid email entered. Please try again.")
            self.grabWin()
            return False
    
    def setMessage(self,message,colour = "white"):
        length = len(message)
        lblMessage = self.lblMessage
        lblUsername = self.lblUsername

        lblMessage.place(in_=lblUsername,x=25,y=60)
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(text_color=colour)
        self.messageVar.set(message)
    
    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEmail.focus_set()

class ResetPassword(CTkToplevel):
    def __init__(self,imgBGPath=None,accent="dodgerblue2",origin=None):
        super().__init__()
        self.geometry("610x270")
        self.maxdims = [610,270]
        self.imagedims = [1280,1080]
        self.minsize(self.maxdims[0],self.maxdims[1])
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Reset your password - Tickd")
        self.iconbitmap("logo//tickd.ico")
        
        self.origin = origin
        # This is to access the attributes of the Auth window class.

        self.protocol("WM_DELETE_WINDOW",lambda:self.close_window())

        set_appearance_mode("dark")

        if imgBGPath != None:
            self.imgBGPath = imgBGPath
        self.accent = accent

        
        self.widgets()
        self.placeWidgets()

        """
        """
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

        

        self.elements = {"entryEmail":self.entryEmail,
                         "entryCode":self.entryCode,
                         "entryPassword":self.entryPassword}
      

        self.mainloop()

    def close_window(self):
        self.origin.resetWinOpen = False
        self.destroy()

    def widgets(self):
        globalFontName = "Bahnschrift"
        emojiFont = ("Segoe UI Emoji",30)

        if self.imgBGPath == None:
            self.darkImgBG,self.lightImgBG,_,_ = getWallpaper.getRandom((self.imagedims[0],self.imagedims[1]))
            if get_appearance_mode() == "dark":
                self.imgBG = self.darkImgBG
            else:
                self.imgBG = self.lightImgBG
        elif self.imgBGPath == "no":
            pass
        else:
            self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.imagedims[0],self.imagedims[1]))
        #self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)

        self.frameRegister = CTkFrame(self,width=565,height=240,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.logoImg = CTkImage(dark_image=Image.open("logo//blackBGLogo.png"),light_image=Image.open("logo//whiteBGLogo.png"),size=(140,45))
        self.panelLogo = CTkLabel(self.frameRegister,text="",image=self.logoImg)
        self.lblTitle = CTkLabel(self.frameRegister,font=(globalFontName,35),text="Reset your password.")

        self.entryEmail = CTkEntry(self.frameRegister,font=(globalFontName,25),width=375,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameRegister,font=(globalFontName,25),width=375,placeholder_text="new password",show="*",corner_radius=15)
        self.entryCode = CTkEntry(self.frameRegister,font=(globalFontName,25),width=150,placeholder_text="code",corner_radius=15)
        self.lblEntry = CTkLabel(self.frameRegister,font=emojiFont,text="✉️")

        self.imgShowPassword = CTkImage(Image.open("icons//eyeIcon.png"),size=(33,24))
        self.btnShowPassword = CTkButton(self.frameRegister,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("icons//eyeIconOff.png"),size=(33,24))
        self.btnHidePassword = CTkButton(self.frameRegister,image=self.imgHidePassword,text="",width=0,command=self.showHide,corner_radius=15,fg_color=self.accent)
        
        self.btnVerify = CTkButton(self.frameRegister,text="verify",width=55,corner_radius=15,fg_color=self.accent,font=(globalFontName,25),command=self.checkEmailFormat)

        self.btnReset = CTkButton(self.frameRegister,text="reset",font=(globalFontName,30),corner_radius=15,text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.resetClicked)

        #self.btnCancel = CTkButton(self.frameRegister,text="cancel",font=(globalFontName,30),corner_radius=15,hover_color="red",text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.close_window)

    def placeWidgets(self):
        #self.panelImgBG.place(x=0,y=0)
        self.frameRegister.place(relx=0.5,rely=0.5,anchor="center")
        self.panelLogo.place(relx=0.35,y=20)
        self.lblTitle.place(in_=self.panelLogo,x=-85,y=45)

        self.entryEmail.place(x=80,y=125)
        self.lblEntry.place(in_=self.entryEmail,x=-50,y=-3)
        """self.entryPassword.place(in_=self.entryEmail,y=70)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-3)"""

        self.btnVerify.place(in_=self.entryEmail,x=380)
        #self.btnRegister.place(in_=self.entryEmail,x=45,y=100)
        #self.btnCancel.place(in_=self.btnRegister,x=145)

        
    def sendEmail(self,receiverEmail):

        # Create SSL context for secure connection
        context = ssl.create_default_context()
        tickdEmail = "tickd.todolist@gmail.com"

        # Create message object
        message = MIMEMultipart()

        # Define message components
        message["From"] = "Tickd. <tickd.todolist@gmail.com>"
        message["To"] = receiverEmail
        message["Subject"] = "Your Tickd security code."
        # Defining message using HTML to add images and text formatting.
        msgText = f"<html><body><img src='https://tickd-todo.s3.eu-west-2.amazonaws.com/blackBGLogo.png' width=300>\
                    <h2>Your security code.</h2><p>Someone or you tried to reset your Tickd password.<br><br>\
                    Your security code is</p><h2>{self.code}</h2><br><br><p>Thanks,</p><h3>The Tickd security team.</h3></body></html>"
        msgObj = MIMEText(msgText,"html")
        message.attach(msgObj)

        # Send message using smtplib and the SSL context defined earlier. 
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
            server.login(tickdEmail,"daxn vysr plkb blnv")
            server.sendmail(tickdEmail,receiverEmail,message.as_string())
            print("Message sent!")
        
    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=385,y=2)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=385,y=2)
            self.entryPassword.configure(show="*")
    
    def grabWin(self):
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

    def resetClicked(self):
        newPasswordTxt = self.entryPassword.get().strip()
        
        details,rememberMeIndex = getAllDetails()
        
        if newPasswordTxt == "":
            messagebox.showerror("Can't reset password.","Your password cannot be blank.")
        else:
            newPasswordHashed = genHash(newPasswordTxt)
            
            detailsSet = ""
            index = 0
            found = False
            while not found:
                if details[index][0] == self.email:
                    detailsSet = details[index]
                    details.pop(index)
                    found = True
                else:
                    index += 1

            detailsSet[1] = newPasswordHashed
            details.append(detailsSet)
            newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

            print(newAuthDetails)
            
            with open("authDetails.json","w") as f:
                json.dump(newAuthDetails,f,indent=4)
            
            self.resetEntry(["entryPassword"])
            messagebox.showinfo("Reset successful.","Password successfully reset. Please log in.")
            self.after(500,self.close_window)
        
  #-------# Entry validation funcs #-------#

    def checkDetailsFound(self,email,details):
        found = False
        for each in details:
            if each[0] == email:
                userDetails = each
                found = True
        if found == False:
            print("No details found.")
            userDetails = []

        return found, userDetails

    def genCode(self):
        code = ""
        for each in range(6):
            digit = str(randint(0,9))
            code+=digit
        return code

    def checkEmailFormat(self):
        self.email = self.entryEmail.get()
        if "@" in self.email:
            splitEmail = self.email.split("@")
            if "." in splitEmail[1]:
                emailRegistered = self.checkEmailRegistered(self.email)

                if emailRegistered:
                    self.lblEntry.configure(text="🔑")
                    self.entryEmail.place_forget()
                    self.entryCode.place(x=170,y=150)
                    self.lblEntry.place(in_=self.entryCode,x=-50,y=-3)
                    self.btnVerify.configure(command=self.checkCode)
                    self.btnVerify.place(in_=self.entryCode,x=155)
                    self.code = self.genCode()
                    self.sendEmail(self.email)
                    messagebox.showinfo("Code sent.","Please check your email and enter the code.")
                    


                else:
                    messagebox.showerror("Can't reset password.","Email not registered.")
            else:
                messagebox.showerror("Can't reset password.","Invalid email entered.")
        else:
            messagebox.showerror("Can't reset password.","Invalid email entered.")
            return False
    
    def checkEmailRegistered(self,emailToCheck):
        details,_ = getAllDetails()
        for detailSet in details:
            if detailSet[0] == emailToCheck:
                return True
        return False

    def checkCode(self):
        codeInput = self.entryCode.get()

        if codeInput == self.code:
            messagebox.showinfo("Verification successful.","Your identity has been verified.\nPlease enter your new password.")

            # Sets up password entry: removes verify btn and code entry, adds lock symbol, entry and reset btn. 
            self.btnVerify.place_forget()
            self.lblEntry.configure(text="🔒")
            self.entryCode.place_forget()
            self.entryPassword.place(x=95,y=150)
            self.lblEntry.place(in_=self.entryPassword,x=-50,y=-3)
            self.btnReset.place(in_=self.entryPassword,x=125,y=50)
            self.btnShowPassword.place(in_=self.entryPassword,x=385,y=2)
        else:
            # Shows error if entered code is incorrect.
            messagebox.showerror("Can't reset password.","Invalid code entered.")
    
    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEntry.focus_set()

    

#auth = Auth()
