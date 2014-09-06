#!/usr/bin/env python

import os
import sys
import configparser
from PIL import Image, ImageOps
import shutil
from os import listdir
from os.path import isfile, join

## TODO: Implement these two
# sliderb0.png (or whatever frame you like if there are more than one) -> slider-ball.png
# sliderb0@2x.png (or whatever frame you like if there are more than one) -> slider-ball@2x.png
resizeOsu = [
  "default-0.png",
  "default-0@2x.png",
  "default-1.png",
  "default-1@2x.png",
  "default-2.png",
  "default-2@2x.png",
  "default-3.png",
  "default-3@2x.png",
  "default-4.png",
  "default-4@2x.png",
  "default-5.png",
  "default-5@2x.png",
  "default-6.png",
  "default-6@2x.png",
  "default-7.png",
  "default-7@2x.png",
  "default-8.png",
  "default-8@2x.png",
  "default-9.png",
  "default-9@2x.png",
]

resizeHexis = [
  "object-0.png",
  "object-0@2x.png",
  "object-1.png",
  "object-1@2x.png",
  "object-2.png",
  "object-2@2x.png",
  "object-3.png",
  "object-3@2x.png",
  "object-4.png",
  "object-4@2x.png",
  "object-5.png",
  "object-5@2x.png",
  "object-6.png",
  "object-6@2x.png",
  "object-7.png",
  "object-7@2x.png",
  "object-8.png",
  "object-8@2x.png",
  "object-9.png",
  "object-9@2x.png",
]

moveOsu = [ 
  "scorebar-bg.png",
  "scorebar-bg@2x.png",
  "scorebar-colour.png",
  "scorebar-colour@2x.png",
  "lighting.png",
  "lighting@2x.png",
  "reversearrow.png",
  "reversearrow@2x.png",
  "sliderfollowcircle.png",
  "sliderfollowcircle@2x.png",
  "sliderscorepoint.png",
  "sliderscorepoint@2x.png",
  "spinner-approachcircle.png",
  "spinner-approachcircle@2x.png",
  "spinner-metre.png",
  "spinner-metre@2x.png",
  "spinner-background.png",
  "spinner-background@2x.png",
  "spinner-circle.png",
  "spinner-circle@2x.png",
  "play-warningarrow.png",
  "play-warningarrow@2x.png"
]

moveHexis = [ 
  "healthbar-bg.png",
  "healthbar-bg@2x.png", 
  "healthbar-meter.png",
  "healthbar-meter@2x.png",
  "hitlighting.png",
  "hitlighting@2x.png",
  "slider-reversearrow.png",
  "slider-reversearrow@2x.png",
  "slider-followcircle.png",
  "slider-followcircle@2x.png",
  "slider-tick.png",
  "slider-tick@2x.png",
  "spinner-outline.png",
  "spinner-outline@2x.png",
  "spinner-overlay.png",
  "spinner-overlay@2x.png",
  "spinner-pump.png",
  "spinner-pump@2x.png",
  "spinner.png",
  "spinner@2x.png",
  "warningarrow.png",
  "warningarrow@2x.png"
]

def getini( inipath, section, name ):
  ini = configparser.RawConfigParser()
  ini.read(inipath)
  try:
    return ini.get(section, name)
  except:
    if name ==  "Name":
      return "osu!skin"
    elif name == "Author":
      return "osu!author"
    else:
      return "blank"


def iniToXML( inipath ):
  ini = configparser.RawConfigParser()
  ini.read(inipath)

  comboNames = [ "Combo1", "Combo2", "Combo3", "Combo4", "Combo5", "Combo6", "Combo7" ]
  comboArray = []
  colours = ""

  try:
    # get all combo colours
    for combo in comboNames:
      comboArray.append(ini.get("Colours", combo))
  except:
    pass

    # populate the xml file with them
  for combo in comboArray:
    c = combo.split(',')
    colours += '\t\t\t\t<color r="{color1}" g="{color2}" b="{color3}"></color>\n'.format(color1 = c[0], color2 = c[1], color3 = c[2])

  sliderColorsTemp = ini.get("Colours", "SliderBorder")
  sliderColors = sliderColorsTemp.split(",")

  iniSliderBorder = "<border r=\"{sliderR}\" g=\"{sliderG}\" b=\"{sliderB}\" />".format(sliderR = sliderColors[0], sliderB = sliderColors[1], sliderG = sliderColors[2])
  theme = '''<?xml version="1.0" encoding="UTF-8"?>
<hexis>
    <theme version="1.0">
        <meta>
            <name>{skinName}</name>
            <creator>{skinAuthor}</creator>
        </meta>
        <cursor rotate="{cursorRotate}" expand="{cursorExpand}" color="#FFFFFF">
            <trail length="0" color="#FFFFFF" opacity="50" />
        </cursor>
        <playfield>
            <set>
{colourSet}            </set>
            <slider>
                {sliderSet}
            </slider>
            <font>
                <combo prefix="{scoreFont}" kerning="{scoreKerning}" />
                <score prefix="{scoreFont}" kerning="{scoreKerning}" />
            </font>
        </playfield>
    </theme>
</hexis>'''.format(skinName = getini(inipath, "General", "Name"), skinAuthor = getini(inipath, "General", "Author"), cursorRotate = getini(inipath, "General", "CursorRotate"), cursorExpand = getini(inipath, "General", "CursorExpand"), colourSet = colours, sliderSet = iniSliderBorder, scoreFont = getini(inipath, "Fonts", "ScorePrefix"), scoreKerning = getini(inipath, "Fonts", "ScoreOverlap"))
  if not os.path.exists("Converted"):
    os.makedirs("Converted")
  else:
    shutil.rmtree(os.getcwd() + "/Converted")
    os.makedirs("Converted")
  with open("Converted/theme.xml", "w") as theme_file:
    theme_file.write(theme)

def resizeImage ( path, imagefile, destfile ):
  dest = os.getcwd() + "/Converted/" + destfile
  im = Image.open(path + "/" + imagefile)
  x = im.size[0]
  y = im.size[1]
  resized = int((x * 75) / 100), int((y * 75) / 100)
  im = ImageOps.fit(im, resized, Image.ANTIALIAS)
  im.save(dest)
  print("Resized "+ imagefile + " to "+ destfile)

def moveImage ( path, imagefile ):
  dest = os.getcwd() + "/Converted/" + imagefile
  shutil.copyfile(path + "/" + imagefile, dest)
  print("Copied "+ imagefile +" to "+ imagefile)

def renameImage ( path, imagefile ):
  dest = os.getcwd() + "/Converted/" + imagefile
  shutil.copyfile(path + "/" + imagefile, dest)
  print("Renamed "+ imagefile +" to "+ imagefile)

def checkFile( file ):
  try:
    osuFile = resizeOsu.index(file)
    return 1
  except ValueError:
    return 0

  try:
    osuFile = moveOsu.index(file)
    return 2
  except ValueError:
    return 0
    
def init():
  if len(sys.argv) == 1: # 1 is us
    print("No arguments specified. Usage: convert /path/to/skin.ini")
  elif len(sys.argv) == 2: # skin.ini
    if "skin.ini" in sys.argv[1]:
      inipath = sys.argv[1]
      iniToXML(sys.argv[1])

      path = os.path.dirname(os.path.realpath(sys.argv[1]))

      files = [ f for f in listdir(path) if isfile(join(path,f)) ]
      for file in files:
        checked = checkFile(file)
        if checked == 1:
          osuFile = resizeOsu.index(file)
          resizeImage(path, file, resizeHexis[osuFile])
        elif checked == 2:
          renameImage(path, file)
        else:
          moveImage(path, file)
    else:
      print("No skin.ini found :(")

init()