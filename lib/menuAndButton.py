# Collapsible floating menu and button
from customtkinter import *
from PIL import Image
from lib.menu import Menu

class MenuAndButton(CTkFrame):
    def __init__(self,master,menuItemsAndLabels:dict,origin,userName,font="Bahnschrift",accent="dodgerblue2"):
        """By default, this starts as a "button", but is not actually
        a CTkButton, but rather is a CTkFrame instance that can be clicked.
        Once clicked, it will open a CTkFrame below it which is the menu."""

        # Declares super class object (CTkFrame)
        super().__init__(master,width=60,height=60,corner_radius=20,border_width=3,border_color="black",fg_color="grey",cursor="hand2")

        # origin is the variable representing the app's methods and attributes
        self.origin = origin
        # master is the "currentFrame" where the button is being placed.
        self.master = master

        self.globalFontName = font
        self.accent = accent
        self.userName = userName

        # Declares image for open and close
        self.imgMenuOpen = CTkImage(Image.open("icons//menu open.png"),size=(40,40))
        self.panelMenuOpen = CTkLabel(self,text="",image=self.imgMenuOpen)
        self.imgMenuClose = CTkImage(Image.open("icons//menu close.png"),size=(40,40))
        self.panelMenuClose = CTkLabel(self,text="",image=self.imgMenuClose)

        self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        self.bind("<Button-1>",lambda event:self.clicked())
        self.panelMenuOpen.bind("<Button-1>",lambda event: self.clicked())
        self.panelMenuClose.bind("<Button-1>",lambda event: self.clicked())

        # Allows for colour to change when user hovers over button.
        self.bindHoverBGChange([self,self.panelMenuOpen,self.panelMenuClose])
        
        
        self.menuItems = []

        # Declares menu object and flag for menu being open or closed.
        self.menu = Menu(master,menuItemsAndLabels,accent=self.accent,origin=self,font=font,bottomLabel=f"{self.userName}")
        self.menuOpen = False

                
    def bindHoverBGChange(self,widgets:list):
        for each in widgets:
            each.bind("<Enter>",lambda event:self.configure(fg_color="grey24"))
            each.bind("<Leave>",lambda event:self.configure(fg_color="grey"))


    def bindClicks(self,*widgets):
        for widget in widgets:
            widget.bind("<Button-1>",lambda event:self.clicked())

    def onTextHoverEnter(self,widget):
        widget.configure(text_color=self.accent)
    
    def onTextHoverLeave(self,widget):
        widget.configure(text_color=("black","white"))
     


    def clicked(self):
        # Lifts the menu in the stacking order
        self.menu.lift()

        # Closes the menu if it is open.
        if self.menuOpen:
            self.menu.place_forget()
            self.panelMenuClose.place_forget()
            # Displays icon for a closed menu (if you click it opens the menu)
            self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
            self.menuOpen = False
            
        # Opens the menu if it is closed
        else:
            self.menu.place(in_=self,y=60)
            self.panelMenuOpen.place_forget()
            # Displays icon for an open menu (if you click it closes the menu)
            self.panelMenuClose.place(relx=0.5,rely=0.5,anchor="center")
            self.menuOpen = True
            



"""root = CTk()
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
root.mainloop()"""
