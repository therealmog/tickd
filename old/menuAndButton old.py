# Collapsible floating menu and button
# Old version - both menu and button in one class, so not separated.

from customtkinter import *
from PIL import Image
from lib.getListImgs import getListImgs

class MenuAndButton(CTkFrame):
    def __init__(self,master,menuItemsAndLabels:dict,origin,userName,font="Bahnschrift",accent="dodgerblue2"):
        """By default, this starts as a "button", but is not actually
        a CTkButton, but rather is a CTkFrame instance that can be clicked.
        Once clicked, it will open a CTkFrame below it which is the menu."""

        super().__init__(master,width=60,height=60,corner_radius=20,border_width=3,border_color="black",fg_color="grey",cursor="hand2")
        self.origin = origin
        self.master = master
        self.menuItemsAndLabels = menuItemsAndLabels
        self.globalFontName = font
        self.accent = accent
        self.userName = userName

        self.imgMenuOpen = CTkImage(Image.open("icons//menu open.png"),size=(40,40))
        self.panelMenuOpen = CTkLabel(self,text="",image=self.imgMenuOpen)
        self.imgMenuClose = CTkImage(Image.open("icons//menu close.png"),size=(40,40))
        self.panelMenuClose = CTkLabel(self,text="",image=self.imgMenuClose)

        self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        self.bind("<Button-1>",lambda event:self.clicked())
        self.panelMenuOpen.bind("<Button-1>",lambda event: self.clicked())
        self.panelMenuClose.bind("<Button-1>",lambda event: self.clicked())

        self.bindHoverBGChange([self,self.panelMenuOpen,self.panelMenuClose])
        
        
        self.menuItems = []
        self.createMenu()

    def createMenu(self):
        """Frame can't be placed inside the first frame/button, so it has to
        be placed inside the actual window itself."""
        lblFont = (self.globalFontName,30)

        self.menuFrame = CTkFrame(self.master,width=300,height=0,border_width=3,border_color="black")
        self.lblWelcome = CTkLabel(self.menuFrame,text="Welcome,",font=(self.globalFontName,15))
        self.lblUsername = CTkLabel(self.menuFrame,text=self.userName,font=(self.globalFontName,25),wraplength=250,justify="left")

        self.lblWelcome.place(x=20,y=15)
        self.lblUsername.place(x=20,y=40)
        
        print(self.menuItemsAndLabels)
        self.listImgs = getListImgs((40,40))
        for each in self.menuItemsAndLabels:
            lblText = " "+each
            try:
                itemImg = self.listImgs[each]
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
            
    def bindHoverBGChange(self,widgets:list):
        for each in widgets:
            each.bind("<Enter>",lambda event:self.configure(fg_color="grey24"))
            each.bind("<Leave>",lambda event:self.configure(fg_color="grey"))

    def bindEventListeners(self,*widgets):
        for widget in widgets:
            widget.bind("<Enter>",lambda event,widget=widget:self.onTextHoverEnter(widget))
            widget.bind("<Leave>",lambda event,widget=widget:self.onTextHoverLeave(widget))

    def bindCommand(self,widget,command):
        widget.bind("<Button-1>",lambda event,command=command:self.funcToRun(command))
    
    def funcToRun(self,command):
        self.menuFrame.place_forget()
        self.panelMenuClose.place_forget()
        self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        command()

    def bindClicks(self,*widgets):
        for widget in widgets:
            widget.bind("<Button-1>",lambda event:self.clicked())

    def onTextHoverEnter(self,widget):
        widget.configure(text_color=self.accent)
    
    def onTextHoverLeave(self,widget):
        widget.configure(text_color=("black","white"))

    def increaseFrameHeight(self,finalHeight):
        self.menuFrame.configure(height=finalHeight)
        """currentHeight = self.menuFrame._current_height
        self.unbind("<Button-1>")
        self.panelMenuClose.unbind("<Button-1>")

        if currentHeight==finalHeight:
            self.menuFrame.configure(height=0)        
        if currentHeight > finalHeight:
            print("Final height reached.")
            self.bindClicks(self,self.panelMenuClose)

        else:
            self.menuFrame.configure(height=currentHeight+20)
            self.after(1,lambda finalHeight=finalHeight:self.increaseFrameHeight(finalHeight))"""
    
    def decreaseFrameHeight(self):
        self.menuFrame.place_forget()
        """currentHeight = self.menuFrame._current_height
        self.unbind("<Button-1>")
        self.panelMenuOpen.unbind("<Button-1>")

        if currentHeight<=1:
            print("Height is 0")
            self.menuFrame.place_forget()
            self.bindClicks(self,self.panelMenuOpen)
        else:
            self.menuFrame.configure(height=currentHeight-20)
            self.after(1,lambda:self.decreaseFrameHeight())"""
        


    def clicked(self):
        self.menuFrame.lift()
        
        if self.menuFrame.winfo_ismapped():
            self.decreaseFrameHeight()
        else:
            self.menuFrame.place(in_=self,y=60)
            self.increaseFrameHeight(finalHeight=480)

        if self.panelMenuOpen.winfo_ismapped():
            self.panelMenuOpen.place_forget()
            self.panelMenuClose.place(relx=0.5,rely=0.5,anchor="center")
        else:
            self.panelMenuClose.place_forget()
            self.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")



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