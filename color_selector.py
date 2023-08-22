import pyglet
from pyglet import shapes
import pyautogui
import getpixelcolor
import pyperclip

savedRgb = [] # RGB color codes
savedHex = [] # Hex color codes
isLockOn = False # Locks the current color code

window = pyglet.window.Window(500, 500)
window.set_caption("Color Picker")
batch = pyglet.graphics.Batch()

labelText = "Pic a color"
rgbLabel = pyglet.text.Label(labelText,
                        font_name='Times New Roman',
                        font_size=36,
                        x=window.width//2, y=window.height//1.3,
                        anchor_x='center', anchor_y='center')
hexCodeText = ""
hexLabel = pyglet.text.Label(hexCodeText,
                        font_name='Times New Roman',
                        font_size=36,
                        x=window.width//2, y=window.height//2,
                        anchor_x='center', anchor_y='center')

# Gives the color circle a white border
outerCircle = shapes.Circle(250, 100, 82, color=(255, 255, 255), batch=batch)

# Circle which changes color
circleColor = (0, 0, 0)
circle = shapes.Circle(250, 100, 80, color=circleColor, batch=batch)

def createWindow():
    @window.event
    def on_draw():
        global isLockOn
        window.clear()
        batch.draw()
        rgbLabel.draw()
        hexLabel.draw()
        changeRgbLabel()
        changeHexText()
        changeCircleColor()
        rgbToHex()
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
def on_key_press(symbol, modifiers):
    global isLockOn
    print(f"näppäimistön symboli: {symbol} ja modifier: {modifiers}")
    # Key symbol and number:
    # L = 108   Q = 133   1 = 49   2 = 50
    if isLockOn == True and symbol == 108: # Removes color lock
        isLockOn = False
    elif symbol == 108: # Locks color
        isLockOn = True
    if symbol == 113:
        pyglet.app.EventLoop.has_exit = True
    if symbol == 49: # Copy RGB code when you press 1
        rgbCodeCopy = str(savedRgb[-1])
        pyperclip.copy(rgbCodeCopy)
    if symbol == 50: # Copy Hex code when you press 2
        hexCodeCopy = str(savedHex[-1])
        pyperclip.copy(hexCodeCopy)

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
        hexCode = ('#%02x%02x%02x' % savedRgb[-1])
        #print('#%02x%02x%02x' % savedRgb[-1])
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
def changeCircleColor():
    global circleColor
    if savedRgb != []:
        circleColor = savedRgb[-1]
        circle.color = circleColor

def main():
    createWindow()

if __name__=="__main__":
    main()
