import pyglet
from pyglet import shapes
from pyglet import image
import pyautogui
from ctypes import windll
from pynput import mouse
import pyperclip
from pyglet import app
from pyglet.gl import *

glEnable(GL_DEPTH_TEST)

mainWin = pyglet.window.Window(300, 80)
batch = pyglet.graphics.Batch()
mainWinBgColor = shapes.Rectangle(0, 0, 300, 80, color=(255, 255, 255), batch=batch)

secondWin = pyglet.window.Window(40, 40, style="overlay")
secondWinBgColor = shapes.Rectangle(0, 0, 40, 40, color=(255, 255, 255))

activePicker = image.load("onPicker.png")
unactivePicker = image.load("offPicker.png")

colorCodes = [(255, 255, 255)]
screenCoords = [(0, 0)]
cursorPositionPyglet = [(0, 0)]
suppressOn = True
copyLock = False

@mainWin.event # Close both windows
def on_close():
    secondWin.close()

def getScreenCoordinates():
    coords = pyautogui.position()
    screenCoords[0] = (coords.x, coords.y)

def SecondWinLocation():
    x = screenCoords[0][0]
    y = screenCoords[0][1]
    secondWin.set_location(x + 14, y + 12)

hdc = windll.user32.GetDC(0)
def getColor():
    rgb = windll.gdi32.GetPixel(hdc, screenCoords[0][0], screenCoords[0][1])
    r = rgb & 0xff
    g = (rgb >> 8) & 0xff
    b = (rgb >> 16) & 0xff
    colorCodes.append((r, g, b))

def changeSecWinColor():
    code = colorCodes[-1]
    secondWinBgColor.color = code

def showSecondWin():
    secondWin.set_visible(True)

def hideSecondWin():
    secondWin.set_visible(False)

def CursorOnButton(x, y):
    if x in range(263, 290):
        if y in range(27, 53):
            return True

@mainWin.event # Pyglet mouse clicks
def on_mouse_press(x, y, button, modifiers):
    global suppressOn
    global copyLock

    if button == 1 and CursorOnButton(x, y) == True:
        showSecondWin()
        suppressOn = True
        copyLock = False

@mainWin.event # Pyglet window mouse coordinates
def on_mouse_motion(x, y, dx, dy):
    cursorPositionPyglet[0] = (x, y)

def copyColorCode():
    colorCode = str(colorCodes[-1])
    pyperclip.copy(colorCode)

# --------------------------------------------------------------------
# Pynput

def win32_event_filter(msg, data):
    global suppressOn
    global copyLock

    if copyLock == False and msg == 513 and suppressOn == True:
        copyColorCode()
        copyLock = True
        suppressOn = False
        listener.suppress_event()

listener = mouse.Listener(win32_event_filter=win32_event_filter)
listener.start()

# --------------------------------------------------------------------

@mainWin.event
def on_draw():
    getScreenCoordinates()
    SecondWinLocation()
    batch.draw()

    if copyLock == True and suppressOn == False:
        hideSecondWin()
    if suppressOn == False:
        activePicker.blit(263, 27, -0.5)
    if suppressOn == True:
        unactivePicker.blit(263, 27, 0)
    if copyLock == False:
        getColor()

@secondWin.event
def on_draw():
    secondWinBgColor.draw()
    changeSecWinColor()

app.run()
