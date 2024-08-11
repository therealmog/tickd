from glob import glob
from customtkinter import *
from random import choice
from PIL import Image

def getRandom(dimensions:tuple):
    wallpapers = glob("wallpapers//*.png")
    path = choice(wallpapers)
    
    wallpaperImg = CTkImage(Image.open(path),size=dimensions)
    return wallpaperImg,path

def getFromPath(path,dimensions:tuple):
    wallpaperImg = CTkImage(Image.open(path),size=dimensions)

    return wallpaperImg





