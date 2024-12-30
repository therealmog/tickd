from customtkinter import *
from lib.getListImgs import getListImgs

class Menu(CTkFrame):

    def __init__(self,master,menuItemsAndLabels:dict,accent="dodgerblue2",origin=None,font="Bahnschrift",topLabel="Welcome,",bottomLabel=None):
        """NOTE: Remember to add in the master as the app's self variable (also called master in menuAndButton). 
        menuItemsAndLabels should be a dictionary of the form {"label":lambda args:labelCommand(args),...}"""

        super().__init__(master,width=300,height=480,border_width=3,border_color="black")

        self.menuItems = []
        self.globalFontName = font

        lblFont = (self.globalFontName,30)
        
    
        self.lblTop = CTkLabel(self,text=topLabel,font=(self.globalFontName,15))
        
        if bottomLabel == None:
            bottomLabel = "[insert text here]"
        if topLabel == "":
            size = 30
        else:
            size = 25

        self.lblBottom = CTkLabel(self,text=bottomLabel,font=(self.globalFontName,size),wraplength=250,justify="left")

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

        
        #print(self.menuItemsAndLabels)
        self.listImgs = getListImgs((40,40))
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
        self.place_forget()

        if self.isOrigin:
            self.origin.panelMenuClose.place_forget()
            self.origin.panelMenuOpen.place(relx=0.5,rely=0.5,anchor="center")
        
        command()