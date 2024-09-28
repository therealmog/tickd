from glob import glob
from customtkinter import *
from random import choice
from PIL import Image

def getRandom(dimensions:tuple):
    darkWallpapers = glob("wallpapers//dark*.png")
    darkPath = choice(darkWallpapers)

    lightWallpapers = glob("wallpapers//light*.png")
    lightPath = choice(lightWallpapers)
    
    darkWallpaperImg = CTkImage(Image.open(darkPath),size=dimensions)
    lightWallpaperImg = CTkImage(Image.open(lightPath),size=dimensions)

    return darkWallpaperImg,lightWallpaperImg,darkPath,lightPath

def getFromPath(path,dimensions:tuple):
    wallpaperImg = CTkImage(Image.open(path),size=dimensions)

    return wallpaperImg





