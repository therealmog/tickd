from customtkinter import *
from lib.getListImgs import getListImgs

class Menu(CTkFrame):

    def __init__(self,master,menuItemsAndLabels:dict,accent="dodgerblue2",origin=None,font="Bahnschrift",topLabel="Welcome,",bottomLabel=None):
        """NOTE: Remember to add in the master as the app's self variable (also called master in menuAndButton). 
        menuItemsAndLabels should be a dictionary of the form {"label":lambda args:labelCommand(args),...}"""

        super().__init__(master,width=300,height=480,border_width=3,border_color="black",corner_radius=20)

        self.menuItems = []
        self.globalFontName = font

        if font == "Cascadia Code":
            lblFont = (self.globalFontName,28)
        else:
            lblFont = (self.globalFontName,32)
            
            # There are two labels available to be displayed.
        self.lblTop = CTkLabel(self,text=topLabel,font=(self.globalFontName,15))

        # Displays clearly if bottom label is empty.
        if bottomLabel == None:
            bottomLabel = "[insert text here]"
        if topLabel == "":
            # Size for bottom label increases if top label is empty.
            size = 30
        else:
            size = 25
        
        if lblFont == "Cascadia Code":
            size -= 10

        self.lblBottom = CTkLabel(self,text=bottomLabel,font=(self.globalFontName,size),wraplength=250,justify="left")

        # Places top label on its own if bottom label empty, or with bottom label if it is there.
        if topLabel == "":
            self.lblBottom.place(x=20,y=25)
        else:
            self.lblTop.place(x=20,y=15)
            self.lblBottom.place(x=20,y=40)

        self.accent = accent

        if origin != None:
            # Represents menuAndButton class, if this menu is attached to a button.
            self.origin = origin
            self.isOrigin = True
        else:
            self.isOrigin = False

        
        self.listImgs = getListImgs((42,42))
        for each in menuItemsAndLabels:
            lblText = " "+each
            try:
                itemImg = self.listImgs[each]
            except:
                print(f"No image found for {each}")
                itemImg = self.listImgs["Tick"]

            itemObj = CTkLabel(self,text=lblText,font=lblFont,image=itemImg,compound="left",cursor="hand2")
            
            self.menuItems.append(itemObj)
            self.bindCommand(itemObj,menuItemsAndLabels[each])
            
            #print(self.menuItems)
        self.placeItems()
    
    def placeItems(self):
        self.menuItems[0].place(x=25,y=110)
        self.bindEventListeners(self.menuItems[0])
        for each in range(1,len(self.menuItems)):
            item = self.menuItems[each]
            item.place(in_=self.menuItems[each-1],y=70)
            self.bindEventListeners(item)

    def bindEventListeners(self,*widgets):
        for widget in widgets:
            widget.bind("<Enter>",lambda event,widget=widget:self.onTextHoverEnter(widget))
            widget.bind("<Leave>",lambda event,widget=widget:self.onTextHoverLeave(widget))

    def onTextHoverEnter(self,widget):
        widget.configure(text_color=self.accent)
    
    def onTextHoverLeave(self,widget):
        widget.configure(text_color=("black","white"))

    def bindCommand(self,widget,command):
        # "command" could be the setFrame procedure in app
        # It may also be another command which launches a window.

        widget.bind("<Button-1>",lambda event,command=command:self.funcToRun(command))
    
    def funcToRun(self,command):
        # Removes menu from view when an item has been pressed.
        self.place_forget()

        # Changes the image for the menu button if it exists.
        if self.isOrigin:
            self.origin.panelMenuClose.place_forget()
            self.origin.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        
        # Runs the specified command procedure.
        command()

