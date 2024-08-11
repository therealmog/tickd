# Amogh NG
# To do list

from tkinter import *
import json
try:
    from import_packages import import_packages
    import_packages(['pillow',])
except:
    pass
from PIL import Image, ImageTk

root = Tk()
root.geometry("900x600")
root.minsize(900,600)

#----------------# Fonts #--------------------#
globalFontName = "Bahnschrift"
buttonFont = (globalFontName,20)
emojiFont = ("Segoe UI Emoji",20)





#----------------# Widgets #-----------------#


def changeTheme(theme):
    if theme == "light":
        theme = "dark"
        fontColour = "white"
    else:
        theme = "light"
        fontColour = "black"


entryEmail = Entry(root,font=buttonFont,width=30,fg="gray",relief="flat")
entryEmail.insert(0,"email")


entryPassword = Entry(root, font=buttonFont,width=30,fg="gray",relief="flat")
entryPassword.insert(0,"password")

lblTitle = Label(root,font=(globalFontName,28),text="To-do list")
lblEmail = Label(root,font=emojiFont,text="✉",fg="gray")
lblPassword = Label(root,font=emojiFont,text="🔒",fg="gray")

messageVar = StringVar()
lblMessage = Label(root,font=(globalFontName,30),fg="black",textvariable=messageVar)


btnSignIn = Button(root,text="sign in",font=buttonFont)
btnRegister = Button(root,text="register",font=buttonFont,relief="raised")
btnRegisterConfirm = Button(root,text="confirm",font=buttonFont,relief="raised")

rememberUserVar = IntVar()
checkbtnRememberUser = Checkbutton(root,variable=rememberUserVar, onvalue=1,offvalue=0)
rememberUserVar.set(1)

photoLogoBlack = ImageTk.PhotoImage(Image.open("logo//whiteBGLogo.png").resize((280,70)))
panelLogoBlack = Label(root,image=photoLogoBlack)

imgEyeShow = ImageTk.PhotoImage(Image.open("eyeIcon.png").resize((27,30)))
panelImgEyeShow = Label(root,image=imgEyeShow)

imgEyeHide = ImageTk.PhotoImage(Image.open("eyeIconOff.png").resize((27,30)))
panelImgEyeHide = Label(root,image=imgEyeHide)



def showPasswordToggle(eyeShow):
    if eyeShow:
        print("hi")
        elements["btnShowPassword"].place_forget()
        elements["btnHidePassword"].place(in_=entryPassword,x=460,y=-2)
        entryPassword.config(show="")
    else:
        print("no")
        if entryPassword.get() == "password":
            entryPassword.config(show="")
        else:
            entryPassword.config(show="*")
        
        elements["btnHidePassword"].place_forget()
        elements["btnShowPassword"].place(in_=entryPassword,x=460,y=-2)    

btnShowPassword = Button(root,image=imgEyeShow)
btnHidePassword = Button(root,image=imgEyeHide)

btnShowPassword.bind("<Button-1>",lambda event,eyeShow=True:showPasswordToggle(eyeShow))
btnHidePassword.bind("<Button-1>",lambda event,eyeShow=False:showPasswordToggle(eyeShow))

elements = {
    "lblEmail":lblEmail,
    "lblPassword":lblPassword,
    "entryEmail":entryEmail,
    "entryPassword":entryPassword,
    "btnRegister":btnRegister,
    "btnSignIn":btnSignIn,
    #"tickBoxRememberUser":tickBoxRememberUser,
    "btnShowPassword":btnShowPassword,
    "btnHidePassword":btnHidePassword

}


specialElements = {

}







#-------------------------------------------------


def setMessage(message,colour):
    length = len(message)
    if length<20:
        fontSize = 30
        lblMessage.place(in_=btnRegister,x=-10,y=80)
    elif length>30 and length<47:
        fontSize = 25
        lblMessage.place(in_=btnRegister,x=-160,y=85)
    elif length>30:
        fontSize = 20
        lblMessage.place(in_=btnRegister,x=-175,y=85)
    else:
        fontSize = 30
        lblMessage.place(in_=btnRegister,x=-80,y=80)
    
    
    lblMessage.config(font=(globalFontName,fontSize),fg=colour)
    messageVar.set(message)


def getDetails():
    with open("authDetails.json","r") as f:
        details = json.load(f)

    return details

def auth():
    entryEmail.grid(row=1,column=0,padx=220,pady=(150,0),sticky="")
    entryPassword.grid(row=2,column=0, sticky="",padx=220,pady=(20,0))
    lblEmail.place(in_=entryEmail,x=-50,y=-5)
    lblPassword.place(in_=entryPassword,x=-52,y=-5)
    btnShowPassword.place(in_=entryPassword,x=460,y=-2)
    btnRegister.place(in_=lblPassword,x=110,y=120)
    btnSignIn.place(in_=lblPassword,x=270,y=120)
    
    checkbtnRememberUser.place(in_=entryPassword,y=50)
    lblMessage.place(in_=btnRegister,x=-75,y=80)
    panelLogoBlack.grid(row=3,column=0)
    panelLogoBlack.place(in_=entryEmail,x=80,y=-100)
    
def checkDetailsFound(email,details):
    found = False
    for each in details:
        if each[0] == email:
            userDetails = each
            found = True
    if found == False:
        print("No details found.")
        userDetails = []

    return found, userDetails

def checkEmpty(email,password):
    emailEmpty = False
    passwordEmpty = False

    if email == "email" and password == "password":
        emailEmpty = True
        passwordEmpty = True
    elif email == "email" or email == "":
        setMessage("Please enter your email.","black")
        emailEmpty = True
    elif password == "password" or password == "":
        passwordEmpty = True
    
    return emailEmpty, passwordEmpty
    

def registerClicked():
    btnRegisterConfirm.place_forget()
    newEmail = entryEmail.get()
    newPassword = entryPassword.get()
    found,_ = checkDetailsFound(newEmail,details=getDetails())
    emailEmpty,passwordEmpty = checkEmpty(newEmail,newPassword)
    emailValid = checkEmail(newEmail)

    if found:
        setMessage("Email already registered with another account","black")
    elif emailEmpty:
        setMessage("Please enter the email you would like to register with.","black")
    elif passwordEmpty:
        setMessage("Please enter a password to use with this account.","black")
    elif not emailValid:
        setMessage("Please enter a valid email.","black")
    else:
        setMessage("Would you like to register a new account with these details?","black")
        btnRegisterConfirm.place(in_=btnRegister,x=75,y=150)


btnRegister.config(command=registerClicked)

def resetEntry(entries:list):
    for each in entries:
        element = elements[each]
        element.config(fg="gray",show="")
        element.delete(0,END)
    
    if "entryEmail" in entries:
        entryEmail.insert(0,"email")
    if "entryPassword" in entries:
        entryPassword.insert(0,"password")
    lblEmail.focus_set()

def checkEmail(email):
    if "@" in email:
        splitEmail = email.split("@")
        if "." in splitEmail[1]:
            return True
        else:
            return False
    else:
        return False
    

        setMessage("Invalid email entered.","red")
        return False

def signInClicked():
    btnRegisterConfirm.place_forget()

    email = entryEmail.get()
    password = entryPassword.get()
    
    details = getDetails()
    
    emailEmpty, passwordEmpty = checkEmpty(email, password)
    emailValid = checkEmail(email)
    found,userDetails = checkDetailsFound(email,details)
    
    
    

    if emailEmpty and passwordEmpty:
        setMessage("Please enter your details.","black")
    elif emailEmpty:
        setMessage("Please enter your email.","black")
        resetEntry(["entryPassword"])
    elif passwordEmpty:
        setMessage("Please enter your password.","black")
    else:
        if emailValid and not found:
            setMessage("Details not found.\nPlease click 'register' to make a new account.","red")
        elif not emailValid:
            setMessage("Please enter a valid email.","black")
            resetEntry(["entryPassword","entryEmail"])
        else:
            correctPassword = userDetails[1]
        
            if password == correctPassword:
                resetEntry(["entryEmail","entryPassword"])
                setMessage("Login successful.","green")
                return True
            else:
                setMessage("Incorrect password.","red")
                resetEntry(["entryPassword"])

    
btnSignIn.config(command=signInClicked)
    
def registerConfirmClicked():
    btnRegisterConfirm.place_forget()
    newEmail = entryEmail.get()
    newPassword = entryPassword.get()

    newDetails = [newEmail,newPassword]

    with open("authDetails.json","r") as f:
        details = json.load(f)
        print(details)
        details.append(newDetails)
        print(details)
    
    with open("authDetails.json","w") as f:
        f.write(json.dumps(details))

    
    resetEntry(["entryEmail","entryPassword"])
    setMessage("Account successfully created. Please log in.","green")


btnRegisterConfirm.config(command=registerConfirmClicked)

def emailFocusIn(_):
    if entryEmail.get() == "email":
        entryEmail.delete(0,"end")
    entryEmail.config(fg="black",relief="solid")
    lblEmail.config(fg="black")

entryEmail.bind("<FocusIn>",emailFocusIn)

def emailFocusOut(_):
    if entryEmail.get() == "":
        entryEmail.insert(0,"email")
        entryEmail.config(fg="gray")
    entryEmail.config(relief="flat")
    lblEmail.config(fg="gray")
entryEmail.bind("<FocusOut>",emailFocusOut)

def passwordFocusIn(_):
    if entryPassword.get() == "password":
        entryPassword.delete(0,"end")
        entryPassword.config(show="*")
    entryPassword.config(fg="black",relief="solid")
    lblPassword.config(fg="black")

    if btnHidePassword.winfo_ismapped():
        entryPassword.config(show="")
entryPassword.bind("<FocusIn>",passwordFocusIn)

def passwordFocusOut(_):
    if entryPassword.get() == "":
        entryPassword.insert(0,"password")
        entryPassword.config(fg="gray",show="")
    entryPassword.config(relief="flat")
    lblPassword.config(fg="gray")
entryPassword.bind("<FocusOut>",passwordFocusOut)


def btnRegisterFocusOut(_):
    btnRegister.config(relief="raised")
btnRegister.bind("<Leave>",btnRegisterFocusOut)

def btnSignInFocusOut(_):
    btnSignIn.config(relief="raised")
btnSignIn.bind("<Leave>",btnSignInFocusOut)

def elementMouseEnter(element):
    if "btn" in element or "entry" in element:
        elements[element].config(relief="solid")
    else:
        elements[element].config(fg="black")
    


def elementMouseLeave(element):
    if "btn" in element:
        elements[element].config(relief="raised")
    elif "entry" in element:
        elements[element].config(relief="flat")
    # rewrite
    else:
        elements[element].config(fg="gray")
    

# Note: Binding using lambda function must take into account 'event' parameter given by bind function

def bindingEventListeners():
    for each in elements:
        elements[each].bind("<Enter>",lambda event,element=each:elementMouseEnter(element))
        elements[each].bind("<Leave>",lambda event,element=each:elementMouseLeave(element))

def main():
    loggedIn = auth()
    if loggedIn:
        print("Logged in.")
    bindingEventListeners()
main()

root.mainloop()
