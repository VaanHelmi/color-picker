import pyglet
from pyglet import shapes
import pyautogui
import getpixelcolor
import pyperclip

# python -m IPython .\color_selector.py

savedRgb = [] # RGB muodossa värit. savedRgb[-1] on viimeisin kursorin kohdalla oleva väri
savedHex = [] # Hex muodossa värit
isLockOn = False # ns. lukitsee sen hetkisen värin

window = pyglet.window.Window(500, 500)
window.set_caption("Color Picker")
batch = pyglet.graphics.Batch()

labelText = "Pic a color"
RgbLabel = pyglet.text.Label(labelText,
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

# outerCircle antaa circlelle valkean border colorin.
outerCircle = shapes.Circle(250, 100, 82, color=(255, 255, 255), batch=batch) 

# ympyrä, jossa väri vaihtuu kursorin alla olevan värin mukana
circleColor = (0, 0, 0)
circle = shapes.Circle(250, 100, 80, color=circleColor, batch=batch)

def createWindow():
    @window.event
    def on_draw():
        global isLockOn
        window.clear()
        batch.draw()
        RgbLabel.draw()
        hexLabel.draw()
        changeLabel()
        changeHexText()
        changeCircleColor()
        rgbToHex()
        if isLockOn is False: # Jos värikoodin "lukko" ei ole päällä
            try:
                x_cursor, y_cursor = cursorLocation()
                getColor(x_cursor, y_cursor)
            except TypeError:
                return
                #print("pyautogui kirjasto toimii vain main screenillä")
        else: # Jos värikoodin "lukko" on päällä, ei haeta cursorin paikkaa ja värejä
            return
    pyglet.app.event_loop.run()
    return window, RgbLabel, hexLabel, batch

# def screenSize():
#     print(pyautogui.size()) # Antaa näytön koon jos tarvitsee. Vasen ylänurkka on (0,0)

@window.event
def on_key_press(symbol, modifiers):
    global isLockOn
    print(f"näppäimistön symboli: {symbol} ja modifier: {modifiers}")
    # Symboli ja numero:
    # L = 108   Q = 133   1 = 49   2 = 50
    if isLockOn == True and symbol == 108: # Poistaa värikoodin lukon
        isLockOn = False
    elif symbol == 108: # Lukitsee värikoodin
        isLockOn = True
    if symbol == 113:
        pyglet.app.EventLoop.has_exit = True
    if symbol == 49: # Kopioi RGB koodin kun painaa näppäintä 1
        rgbCodeCopy = str(savedRgb[-1])
        pyperclip.copy(rgbCodeCopy)
    if symbol == 50: # Kopioi HEX koodin kun painaa näppäintä 2
        hexCodeCopy = str(savedHex[-1])
        pyperclip.copy(hexCodeCopy)

def cursorLocation():
    position = pyautogui.position()
    x = position[0]
    y = position[1]
    #print(x, y)

    if pyautogui.onScreen(x, y) == True:
        return x, y
    else:
        return

def getColor(x, y):
    color = getpixelcolor.pixel(x, y)
    savedRgb.append(color)
    return color

def rgbToHex(): # Muuntaa RGB värikoodin Hex muotoon
    if savedRgb != []:
        hexCode = ('#%02x%02x%02x' % savedRgb[-1])
        #print('#%02x%02x%02x' % savedRgb[-1])
        savedHex.append(hexCode)

@window.event
def changeLabel():
    if savedRgb != []:
        RgbLabel.text = f"RGB {str(savedRgb[-1])}"

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
