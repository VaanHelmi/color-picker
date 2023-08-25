import pyglet
from pyglet import shapes
import pyautogui
import getpixelcolor
import pyperclip
from pyglet import image
from pynput import mouse

# TODO laatikko mikä seuraa hiirtä. Laatikkoon päivittyy väri.
# Hiiren koordinaatit on olemassa def cursorLocation:ssa
# Miten teen "laatikon".
# Miten saan "laatikkoa" liikutettua
# Miten saan "laatikon" seuraamaan ruudulla

# Kaksi windowia joista toisessa näkyy pikselin väri? Tyhmä idea

savedRgb = [] # RGB color codes
savedHex = [] # Hex color codes
currentColors = [(255, 255, 255), (255, 255, 255), (255, 255, 255)] # Displays previous colors
isLockOn = False # Locks the current color code
changeCopyPic = ["notCopied"] # "notCopied", "RgbHover" and "HexHover"
recentColorsHover = [None] # None, "firstBox", "secondBox", "thirdBox"
pygletCursor = [None]
activeColorHover = False

window = pyglet.window.Window(400, 100)
window.set_caption("Color Picker")
batch = pyglet.graphics.Batch()

# --- ALL SHAPES ---

# Makes the background white
backgroundColorBox = shapes.Rectangle(0, 0, 500, 500, color=(255, 255, 255), batch=batch)

# Hover
hoverColorForBox = shapes.Rectangle(9, 27, 362, 28, (0, 0, 0, 255), batch=batch)
# Bordercolor for colorBox
borderColorBox = shapes.Rectangle(10, 28, 360, 26, (0, 0, 0, 255), batch=batch)
# ColorBox that changes color 
colorForBox = (0, 0, 0)
colorBox = shapes.Rectangle(11, 29, 358, 24, color=colorForBox, batch=batch)

# Hover
hoverRecentColor1 = shapes.Rectangle(277, 2, 25, 23, color=(255, 255, 255), batch=batch)
# Bordercolor for Recent color 1
borderRecentColorBox1 = shapes.Rectangle(279, 4, 21, 19, color=(0, 0, 0), batch=batch)
# Recent color 1
recentColorBox1 = (255, 255, 255)
recentColor1 = shapes.Rectangle(280, 5, 19, 17, color=recentColorBox1, batch=batch)

# Hover
hoverRecentColor2 = shapes.Rectangle(312, 2, 25, 23, color=(255, 255, 255), batch=batch)
# Bordercolor for Recent color 2
borderRecentColorBox2 = shapes.Rectangle(314, 4, 21, 19, color=(0, 0, 0), batch=batch)
# Recent color 2
recentColorBox2 = (255, 255, 255)
recentColor2 = shapes.Rectangle(315, 5, 19, 17, color=recentColorBox2, batch=batch)

# Hover
hoverRecentColor3 = shapes.Rectangle(347, 2, 25, 23, color=(255, 255, 255), batch=batch) 
# Bordercolor for Recent color 3
borderRecentColorBox3 = shapes.Rectangle(349, 4, 21, 19, color=(0, 0, 0), batch=batch)
# Recent color 3
recentColorBox3 = (255, 255, 255)
recentColor3 = shapes.Rectangle(350, 5, 19, 17, color=recentColorBox3, batch=batch)


# TESTILAATIKKO
xTesti = 380
yTesti = 5
# variLaatikko = Tähän muuttuva väri
testiLaatikko = shapes.Rectangle(xTesti, yTesti, 20, 20, color=(60, 255, 60), batch=batch)

# --- ALL IMAGES ---

# Copy picture without hover
copyPic = image.load("clip1.png")
imgWidth = 20
imgHeight = 28
copyPic.width = imgWidth
copyPic.height = imgHeight

# Copy picture with hover on 
hoverCopyPic = pyglet.image.load("clip2.png")
hoverCopyPic.width = imgWidth
hoverCopyPic.height = imgHeight

# Closed lock pic
lockPic = pyglet.image.load("lock.png")
lockImgWidth = 15
lockImgHeight = 16
lockPic.width = lockImgWidth
lockPic.height = lockImgHeight

# Open lock pic
unlockPic = pyglet.image.load("unlock.png")
unlockPic.width = lockImgWidth
unlockPic.height = lockImgHeight


# --- ALL TEXTS ---

# Rgb code text
labelText = "Pic a color"
rgbLabel = pyglet.text.Label(labelText,
                        font_name=["Helvetica", "Times New Roman"], color=(0, 0, 0, 255),
                        font_size=12,
                        x=80, y=80,
                        anchor_x='center', anchor_y='center')
# Hex code text
hexCodeText = ""
hexLabel = pyglet.text.Label(hexCodeText,
                        font_name=["Helvetica", "Times New Roman"], color=(0, 0, 0, 255),
                        font_size=12,
                        x=280, y= 80,
                        anchor_x='center', anchor_y='center')

# Help text on the bottom 
helpText = pyglet.text.Label("Press L to lock / unlock color",
                        font_name=["Helvetica", "Times New Roman"], color=(0, 0, 0, 255),
                        font_size=12,
                        x=105, y= 14, 
                        anchor_x='center', anchor_y='center')

def createWindow():
    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        rgbLabel.draw()
        hexLabel.draw()
        helpText.draw()
        changeRgbLabel()
        changeHexText()
        changeBoxColor()
        changeRecentColors()
        rgbToHex()
        lockStatus()
        lockPicture()
        copyPicHover()
        hoverOnRecentColors()
        hoverOnActiveColor()

    pyglet.app.event_loop.run()
    return window, rgbLabel, hexLabel, batch

def lockStatus(): # Is lock on or off
    if isLockOn is False:
        try:
            x_cursor, y_cursor = cursorLocation()
            addDifferentColor(x_cursor, y_cursor)
        except TypeError:
            #print("pyautogui kirjasto toimii vain main screenillä")
            return
    else: # If color lock on, do nothing
        return

def lockPicture(): # Which lock picture to show
    if isLockOn == False:
        unlockPic.blit(x=374, y=35)
    else:
        lockPic.blit(x=374, y=35)

def copyPicHover(): # Checks which picture is being hovered over
    if changeCopyPic[0] == "notCopied": # No hover
        copyPic.blit(x=170, y=62)
        copyPic.blit(x=340, y=62)
    elif changeCopyPic[0] == "RgbHover": # Hover on Rgb code copy
        hoverCopyPic.blit(x=170, y=62)
        copyPic.blit(x=340, y=62)
    elif changeCopyPic[0] == "HexHover": # Hover on Hex code copy
        copyPic.blit(x=170, y=62)
        hoverCopyPic.blit(x=340, y=62)

def hoverOnRecentColors():
    # Recent colors hover
    if recentColorsHover[0] == None:
        hoverRecentColor1.color = (255, 255, 255)
        hoverRecentColor2.color = (255, 255, 255)
        hoverRecentColor3.color = (255, 255, 255)
    elif recentColorsHover[0] == "firstBox":
        hoverRecentColor1.color = (0, 0, 0)
    elif recentColorsHover[0] == "secondBox":
        hoverRecentColor2.color = (0, 0, 0)
    elif recentColorsHover[0] == "thirdBox":
        hoverRecentColor3.color = (0, 0, 0)

def hoverOnActiveColor():
    #print(activeColorHover)
    if activeColorHover == False:
        hoverColorForBox.color = (255, 255, 255)
    else:
        hoverColorForBox.color = (0, 0, 0)

# def screenSize():
#     print(pyautogui.size()) # Prints screen size. Upper left corner (0,0)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global activeColorHover
    #print(x, y)
    pygletCursor[0] = (x, y)
    if x in range(171, 188):
        if y in range(64, 90):
            changeCopyPic[0] = "RgbHover"
            return
    if x in range(341, 358):
        if y in range(64, 90):
            changeCopyPic[0] = "HexHover"
            return
    if x in range(279, 299):
        if y in range(5, 23):
            if recentColorsHover == []:
                recentColorsHover.append("firstBox")
            else:
                recentColorsHover[0] = "firstBox"
            return
    if x in range(314, 335):
        if y in range(5, 23):
            if recentColorsHover == []:
                recentColorsHover.append("secondBox")
            else:
                recentColorsHover[0] = "secondBox"            
            return
    if x in range(349, 370):
        if y in range(5, 23):
            if recentColorsHover == []:
                recentColorsHover.append("thirdBox")
            else:
                recentColorsHover[0] = "thirdBox"
            return
    if y in range(30, 55):
        #print(y)
        if x in range(10, 370):
            #print(x)
            activeColorHover = True
            #print(activeColorHover)
            return
    else:
        changeCopyPic[0] = "notCopied"
        recentColorsHover[0] = None
        activeColorHover = False
        #print(activeColorHover)
        return
    

#-----------------------------------------------------------------------------------
def on_click(x, y, button, pressed): # Gets clicks outside of pyglet screen
    global isLockOn
    if isLockOn == False:
        if pressed == True:
            isLockOn = True
            if x >= 0:
                copyCurrentColor(x, y)
        # if not pressed:
        #     # Stop listener
        #     return False    

listener = mouse.Listener(
    on_click=on_click)
listener.start()

def copyCurrentColor(x, y): # Copies clicked pixels colorcode as RGB
    colorCode = getpixelcolor.pixel(x, y)
    codeToCopy = str(colorCode)
    pyperclip.copy(codeToCopy)
#-----------------------------------------------------------------------------------

@window.event
def on_mouse_press(x, y, buttons, modifiers): # Checks if mouse left click is on copy img and copies
    global isLockOn
    #print(x, y)
    # RGB and Hex code copy
    if x in range(171, 188): # RGB code copy
        if y in range(64, 90):
            rgbCodeCopy = str(savedRgb[-1]).replace("(", "").replace(")", "")
            pyperclip.copy(rgbCodeCopy)
    if x in range(341, 358): # Hex code copy
        if y in range(64, 90):
            hexCodeCopy = str(savedHex[-1])
            pyperclip.copy(hexCodeCopy)
    # Recent colors copy 
    if x in range(279, 299): # First recent color code copy
        if y in range(5, 23):
            color = str(currentColors[0]).replace("(", "").replace(")", "")
            pyperclip.copy(color)
    if x in range(314, 335): # Second recent color code copy
        if y in range(5, 23):
            color = str(currentColors[1]).replace("(", "").replace(")", "")
            pyperclip.copy(color)
    if x in range(349, 370): # Third recent color code copy
        if y in range(5, 23):
            color = str(currentColors[2]).replace("(", "").replace(")", "")
            pyperclip.copy(color)
    # Unlock colors when cliking on lock picture
    if x in range(376, 388):
        if y in range(35, 53):
            isLockOn = False

@window.event
def on_key_press(symbol, modifiers): # Keyboard input
    global isLockOn
    #print(f"näppäimistön symboli: {symbol} ja modifier: {modifiers}")
    # Key symbol and number:
    # L = 108   Q = 133
    if isLockOn == True and symbol == 108: # Removes color lock
        isLockOn = False
    elif symbol == 108: # Locks color
        isLockOn = True
    if symbol == 113:
        pyglet.app.EventLoop.has_exit = True

def cursorLocation():
    position = pyautogui.position()
    x = position[0]
    y = position[1]

    if pyautogui.onScreen(x, y) == True:
        return x, y
    else:
        return

def addDifferentColor(x, y): # Adds color code to list only if previous one was different
    color = getpixelcolor.pixel(x, y)
    if len(savedRgb) == 0:
        savedRgb.append(color)
    elif len(savedRgb) != 0 and savedRgb[-1] != color:
        savedRgb.append(color)

def rgbToHex(): # Changes RGB code to Hex
    if savedRgb != []:
        hexCode = ('%02x%02x%02x' % savedRgb[-1])
        savedHex.append(hexCode)

@window.event
def changeRgbLabel():
    if savedRgb != []:
        rgbLabel.text = f"RGB {str(savedRgb[-1])}"

@window.event
def changeHexText():
    if savedHex != []:
        hexLabel.text = f"Hex #{str(savedHex[-1])}"

@window.event
def changeBoxColor():
    global colorForBox
    if savedRgb != []:
        colorForBox = savedRgb[-1]
        colorBox.color = colorForBox

@window.event
def changeRecentColors():
    if len(savedRgb) >= 2 and savedRgb[-1] != savedRgb[-2]:
        changeColor = savedRgb[-2]
        if changeColor != currentColors[0] and changeColor != currentColors[1] and changeColor != [2]:
            first = currentColors[0]
            second = currentColors[1]

            currentColors[0] = changeColor
            currentColors[1] = first
            currentColors[2] = second

            recentColor1.color = changeColor
            recentColor2.color = currentColors[1]
            recentColor3.color = currentColors[2]
        else:
            return

def main():
    createWindow()

if __name__=="__main__":
    main()
    #screenSize()
