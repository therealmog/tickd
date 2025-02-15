from customtkinter import *
from PIL import Image
from lib import getWallpaper
from lib.getDetails import getAllDetails
import json
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from lib.genHash import genHash
from tkinter import messagebox

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
        self.origin.setMessage("","white")
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

#register = ResetPassword("no")
        
        
