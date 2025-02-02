from customtkinter import CTkImage
from PIL import Image
from glob import glob

def getListImgs(size:tuple=(35,35)):
    """Returns dictionary with all of the system list images, such as Today, My lists, Starred, Inbox and Leaderboard
    
        NOTE: The keys are stored as the icon name with the first word capitalised.
        e.g. today.png -> 'Today', my lists.png -> 'My lists'"""

    imgs = {}
    #imgNames = ["today","inbox","leaderboard","my lists","starred","tick","toggle theme","add","share","rename","delete","dark mode","light mode","accent colour"]
    imgNames = glob("icons//*.png")
    
    for each in range(len(imgNames)):
        imgNames[each] = imgNames[each].replace("icons\\","")
        imgNames[each] = imgNames[each].replace(".png","")
    
    for each in imgNames:
        img = CTkImage(Image.open(f"icons//{each}.png"),size=size)
        imgs[each.capitalize()] = img
    
    return imgs