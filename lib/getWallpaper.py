from glob import glob
from customtkinter import *
from random import choice
from PIL import Image

def getRandom(dimensions:tuple):
    darkWallpapers = glob("wallpapers//dark*.png")
    darkPath = choice(darkWallpapers)
    print(darkPath)

    lightWallpapers = glob("wallpapers//light*.png")
    lightPath = choice(lightWallpapers)
    print(lightPath)
    
    darkWallpaperImg = CTkImage(Image.open(darkPath),size=dimensions)
    lightWallpaperImg = CTkImage(Image.open(lightPath),size=dimensions)

    return darkWallpaperImg,lightWallpaperImg,darkPath,lightPath

def getFromPath(path,dimensions:tuple):
    wallpaperImg = CTkImage(Image.open(path),size=dimensions)

    return wallpaperImg

def getFromNum(lightNum="none",darkNum="none",dimensions=(1920,1080)):
    """Both nums should be strings""" 

    if lightNum == "none":
        lightImg = Image.open(f"wallpapers//nonelight.png").resize(dimensions)
    else:
        lightImg = Image.open(f"wallpapers//light{lightNum}.png").resize(dimensions)

    if darkNum == "none":
        darkImg = Image.open(f"wallpapers//nonedark.png").resize(dimensions)
    else:
        darkImg = Image.open(f"wallpapers//dark{darkNum}.png").resize(dimensions)
    

    img = CTkImage(light_image=lightImg,
                   dark_image=darkImg,
                   size=dimensions)

    return img




