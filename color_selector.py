import pyautogui
import getpixelcolor
import pyglet

savedColor = []
isLockOn = False

window = pyglet.window.Window(500, 500)
window.set_caption("Color Picker")
text = "Pic a color"
label = pyglet.text.Label(text,
                        font_name='Times New Roman',
                        font_size=36,
                        x=window.width//2, y=window.height//2,
                        anchor_x='center', anchor_y='center')

# def screenSize():
#     print(pyautogui.size()) # Antaa näytön koon jos tarvitsee

def createWindow():
    @window.event
    def on_draw():
        global isLockOn
        window.clear()
        label.draw()
        changeLabel()
        if isLockOn is False: # Jos värikoodin "lukko" ei ole päällä
            x_cursor, y_cursor = cursorLocation()
            getColor(x_cursor, y_cursor)
        else: # Jos värikoodin "lukko" on päällä, ei haeta cursorin paikkaa ja värejä
            return
    pyglet.app.event_loop.run()
    return window, label

@window.event
def on_key_press(symbol, modifiers):
    global isLockOn
    print(f"näppäimistön symboli: {symbol} ja modifier: {modifiers}")
    # L on 108
    # Q on 113
    if isLockOn == True and symbol == 108:
        isLockOn = False
        print("isLockOn on FALSE")
    elif symbol == 108:
        isLockOn = True
        print("isLockOn on true on key press")
    if symbol == 113:
        pyglet.app.EventLoop.has_exit = True

def cursorLocation():
    position = pyautogui.position()
    #print(position)
    x = position[0]
    y = position[1]
    #print(x, y)

    if pyautogui.onScreen(x, y) == True:
        #print(x, y)
        return x, y
    else:
        print("Kursori ei oo näytöllä")
        return

def getColor(x, y):
    color = getpixelcolor.pixel(x, y)
    savedColor.append(color)
    return color

@window.event
def changeLabel():
    if savedColor != []:
        label.text = str(savedColor[-1])

def main():
    createWindow()

if __name__=="__main__":
    main()
