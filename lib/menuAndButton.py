# Collapsible floating menu and button
from customtkinter import *
from PIL import Image

class Menu(CTkFrame):
    def __init__(self,master,menuItemsAndLabels:dict,origin,userName,font="Bahnschrift",accent="dodgerblue2"):
        """By default, this starts as a "button", but is not actually
        a CTkButton, but rather is a CTkFrame instance that can be clicked.
        Once clicked, it will open a CTkFrame below it which is the menu."""

        super().__init__(master,width=50,height=50,corner_radius=20,border_width=3,border_color="black",fg_color="grey")
        self.origin = origin
        self.master = master
        self.menuItemsAndLabels = menuItemsAndLabels
        self.globalFontName = font
        self.accent = accent
        self.userName = userName

        self.imgMenuClosed = CTkImage(Image.open("menu closed.png"),size=(30,30))
        self.panelMenuClosed = CTkLabel(self,text="",image=self.imgMenuClosed)
        self.imgMenuOpen = CTkImage(Image.open("menu open.png"),size=(30,30))
        self.panelMenuOpen = CTkLabel(self,text="",image=self.imgMenuOpen)

        self.panelMenuClosed.place(relx=0.5,rely=0.5,anchor="center")
        self.bind("<Button-1>",lambda event:self.clicked())
        self.panelMenuClosed.bind("<Button-1>",lambda event: self.clicked())
        self.panelMenuOpen.bind("<Button-1>",lambda event: self.clicked())
        
        self.menuItems = []
        self.createMenu()

    def createMenu(self):
        """Frame can't be placed inside the first frame/button, so it has to
        be placed inside the actual window itself."""
        lblFont = (self.globalFontName,30)

        self.menuFrame = CTkFrame(self.master,width=300,height=480,border_width=3,border_color="black")
        self.lblWelcome = CTkLabel(self.menuFrame,text="Welcome,",font=(self.globalFontName,15))
        self.lblUsername = CTkLabel(self.menuFrame,text=self.userName,font=(self.globalFontName,25),wraplength=250,justify="left")

        self.lblWelcome.place(x=20,y=15)
        self.lblUsername.place(x=20,y=40)
        
        print(self.menuItemsAndLabels)
        for each in self.menuItemsAndLabels:
            lblText = " "+each
            try:
                name = each.lower()
                itemImg = CTkImage(Image.open(f"{name}.png"),size=(40,40))
            except:
                print(f"No image found for {each}")

            itemObj = CTkLabel(self.menuFrame,text=lblText,font=lblFont,image=itemImg,compound="left",cursor="hand2")
            
            self.menuItems.append(itemObj)
            self.bindCommand(itemObj,self.menuItemsAndLabels[each])
            
            #print(self.menuItems)
        self.placeItems()
    
    def placeItems(self):
        self.menuItems[0].place(x=25,y=110)
        self.bindEventListeners(self.menuItems[0])
        for each in range(1,len(self.menuItems)):
            item = self.menuItems[each]
            item.place(in_=self.menuItems[each-1],y=70)
            self.bindEventListeners(item)
            

    def bindEventListeners(self,widget):
        widget.bind("<Enter>",lambda event,widget=widget:self.onTextHoverEnter(widget))
        widget.bind("<Leave>",lambda event,widget=widget:self.onTextHoverLeave(widget))

    def bindCommand(self,widget,command):
        widget.bind("<Button-1>",lambda event:command())

    def onTextHoverEnter(self,widget):
        widget.configure(text_color=self.accent)
    
    def onTextHoverLeave(self,widget):
        widget.configure(text_color="white")

    def clicked(self):
        if not self.menuFrame.winfo_ismapped():
            self.menuFrame.place(in_=self,y=50)
        else:
            self.menuFrame.place_forget()
        if self.panelMenuClosed.winfo_ismapped():
            self.panelMenuClosed.place_forget()
            self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        else:
            self.panelMenuOpen.place_forget()
            self.panelMenuClosed.place(relx=0.5,rely=0.5,anchor="center")



root = CTk()
root.geometry("300x300")
def hello():
    print("Hello!!")
def goodbye():
    print("Goodbye!")

menu = Menu(master=root,menuItemsAndLabels={"Inbox":hello,
                                            "My lists":goodbye,
                                            "Today":"ajsdoasd",
                                            "Leaderboard":"asjodoas",
                                            "Starred":hello},userName="TickdAdmin",origin="")
menu.pack()
root.mainloop()