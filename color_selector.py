import pyglet
from pyglet import shapes
import pyautogui
import getpixelcolor
import pyperclip
from pyglet import image

savedRgb = [] # RGB color codes
savedHex = [] # Hex color codes
isLockOn = False # Locks the current color code
changeCopyPic = ["notCopied"] # "notCopied", "RgbHover" and "HexHover"

window = pyglet.window.Window(400, 100)
window.set_caption("Color Picker")
batch = pyglet.graphics.Batch()

# Makes the background white
backgroundColorBox = shapes.Rectangle(0, 0, 500, 500, color=(255, 255, 255), batch=batch)

# Copy picture without hover
copyPic = pyglet.image.load("clip1.png")
imgWidth = 20
imgHeight = 28
copyPic.width = imgWidth
copyPic.height = imgHeight

# Copy picture with hover on 
hoverCopyPic = pyglet.image.load("clip2.png")
hoverCopyPic.width = imgWidth
hoverCopyPic.height = imgHeight

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
                        x=200, y= 14,
                        anchor_x='center', anchor_y='center')

# Black bordercolor for colorBox
borderColorBox = shapes.Rectangle(20, 28, 360, 26, (0, 0, 0, 255), batch=batch)
# ColorBox that changes color 
colorForBox = (0, 0, 0)
colorBox = shapes.Rectangle(21, 29, 358, 24, color=colorForBox, batch=batch)

def createWindow():
    @window.event
    def on_draw():
        global isLockOn
        window.clear()
        batch.draw()
        rgbLabel.draw()
        hexLabel.draw()
        helpText.draw()
        changeRgbLabel()
        changeHexText()
        changeBoxColor()
        rgbToHex()
        if changeCopyPic[0] == "notCopied": # No hover on copy pic
            copyPic.blit(x=170, y=62)
            copyPic.blit(x=340, y=62)
        elif changeCopyPic[0] == "RgbHover": # Hover on Rgb code copy pic
            hoverCopyPic.blit(x=170, y=62)
            copyPic.blit(x=340, y=62)
        elif changeCopyPic[0] == "HexHover": # Hover on Hex code copy pic
            copyPic.blit(x=170, y=62)
            hoverCopyPic.blit(x=340, y=62)
        if isLockOn is False: # If color lock not on
            try:
                x_cursor, y_cursor = cursorLocation()
                getColor(x_cursor, y_cursor)
            except TypeError:
                #print("pyautogui kirjasto toimii vain main screenillä")
                return
        else: # If color lock on, do nothing
            return
    pyglet.app.event_loop.run()
    return window, rgbLabel, hexLabel, batch

# def screenSize():
#     print(pyautogui.size()) # Prints screen size. Upper left corner (0,0)

@window.event
def on_mouse_motion(x, y, dx, dy):
    if x in range(171, 188):
        if y in range(64, 90):
            changeCopyPic[0] = "RgbHover"
            return
            #print(x, y)
    if x in range(341, 358):
        if y in range(64, 90):
            changeCopyPic[0] = "HexHover"
            return
            #print(x, y)
    else:
        changeCopyPic[0] = "notCopied"
        return

@window.event
def on_mouse_press(x, y, buttons, modifiers): # Checks if mouse left click is on copy img and copies
    #print(x, y)
    if x in range(171, 188):
        if y in range(64, 90):
            rgbCodeCopy = str(savedRgb[-1]).replace("(", "").replace(")", "")
            pyperclip.copy(rgbCodeCopy)
    if x in range(341, 358):
        if y in range(64, 90):
            hexCodeCopy = str(savedHex[-1])
            pyperclip.copy(hexCodeCopy)

@window.event
def on_key_press(symbol, modifiers): # Keyboard input
    global isLockOn
    print(f"näppäimistön symboli: {symbol} ja modifier: {modifiers}")
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

def getColor(x, y):
    color = getpixelcolor.pixel(x, y)
    savedRgb.append(color)
    return color

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
        hexLabel.text = f"Hex {str(savedHex[-1])}"

@window.event
def changeBoxColor():
    global colorForBox
    if savedRgb != []:
        colorForBox = savedRgb[-1]
        colorBox.color = colorForBox

def main():
    createWindow()

if __name__=="__main__":
    main()
