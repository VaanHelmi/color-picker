import pyglet
from pyglet import shapes
import random

# 4 pitkulaista laatikkoa vierekkäin
# laatikkoihin arvotaan eri värit

window = pyglet.window.Window(400, 500)
window.set_caption("ASD")
batch = pyglet.graphics.Batch()

boxColors = {
    "box1": [255, 10, 10],
    "box2": [10, 225, 10],
    "box3": [10, 10, 225],
    "box4": [200, 200, 200]
}



box1Color = tuple(boxColors["box1"])
box2Color = tuple(boxColors["box2"])
box3Color = tuple(boxColors["box3"])
box4Color = tuple(boxColors["box4"])

box1 = shapes.Rectangle(20, 80, 80, 220, color=box1Color, batch=batch)
box2 = shapes.Rectangle(113, 80, 80, 220, color=box2Color, batch=batch)
box3 = shapes.Rectangle(207, 80, 80, 220, color=box3Color, batch=batch)
box4 = shapes.Rectangle(301, 80, 80, 220, color=box4Color, batch=batch)

labelText = "Press R"
label = pyglet.text.Label(labelText,
                        font_name='Times New Roman',
                        font_size=36,
                        x=window.width//2, y=window.height//1.2,
                        anchor_x='center', anchor_y='center')

box1RgbText = str(box1Color)
box1TextForRgb = pyglet.text.Label(box1RgbText,
                        font_name='Times New Roman',
                        font_size=10,
                        x=56, y=40,
                        anchor_x='center', anchor_y='center')

box1HexText = "f1f1f1f1"
box1TextForHex = pyglet.text.Label(box1HexText,
                        font_name='Times New Roman',
                        font_size=12,
                        x=56, y=20,
                        anchor_x='center', anchor_y='center')

box2RgbText = str(box2Color)
box2TextForRgb = pyglet.text.Label(box2RgbText,
                        font_name='Times New Roman',
                        font_size=10,
                        x=148, y=40,
                        anchor_x='center', anchor_y='center')

box2HexText = "f2f2f2f2"
box2TextForHex = pyglet.text.Label(box2HexText,
                        font_name='Times New Roman',
                        font_size=12,
                        x=148, y=20,
                        anchor_x='center', anchor_y='center')

box3RgbText = str(box3Color)
box3TextForRgb = pyglet.text.Label(box3RgbText,
                        font_name='Times New Roman',
                        font_size=10,
                        x=244, y=40,
                        anchor_x='center', anchor_y='center')

box3HexText = "f3f3f3f3"
box3TextForHex = pyglet.text.Label(box3HexText,
                        font_name='Times New Roman',
                        font_size=12,
                        x=244, y=20,
                        anchor_x='center', anchor_y='center')

box4RgbText = str(box4Color)
box4TextForRgb = pyglet.text.Label(box4RgbText,
                        font_name='Times New Roman',
                        font_size=10,
                        x=342, y=40,
                        anchor_x='center', anchor_y='center')

box4HexText = "f4f4f4f4"
box4TextForHex = pyglet.text.Label(box4HexText,
                        font_name='Times New Roman',
                        font_size=12,
                        x=342, y=20,
                        anchor_x='center', anchor_y='center')

def createWindow():
    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        label.draw()
        box1TextForRgb.draw()
        box2TextForRgb.draw()
        box3TextForRgb.draw()
        box4TextForRgb.draw()
        box1TextForHex.draw()
        box2TextForHex.draw()
        box3TextForHex.draw()
        box4TextForHex.draw()
        rgbCodeToHex()

    pyglet.app.event_loop.run()
    return window

# ----------------------------------

@window.event
def on_key_press(symbol, modifiers):
    # Symbol and number
    # Q = 113   R = 114
    print(symbol)
    if symbol == 113:
        pyglet.app.event_loop.exit()
    if symbol == 114:
        randomColor()
    # if symbol == 49:
    #     first = True
    #     randomColor(first)

def randomColor():
    for box in boxColors.items():
        number1 = random.randrange(0, 226) # Random number between 0 - 255
        number2 = random.randrange(0, 226)
        number3 = random.randrange(0, 226)
        box[1][0] = number1
        box[1][1] = number2
        box[1][2] = number3
    # Each box gets new color code from boxColors
    box1.color = tuple(boxColors["box1"])
    box2.color = tuple(boxColors["box2"])
    box3.color = tuple(boxColors["box3"])
    box4.color = tuple(boxColors["box4"])
    #print("boxColors sisältö: ", boxColors)

def rgbCodeToHex():
    for code in boxColors.items():
        #print(code)
        #print(type(code))
        rgbAsList = code[1]
        rgbTuple = tuple(rgbAsList)
        #print(rgbTuple)
        hex = '#%02x%02x%02x' % rgbTuple
        print(hex)
        # TODO korjaa! Hex väri vaihtuu (kun painaa R) mutta rgb pysyy samana.
        box1TextForHex.text = hex
        # print -> '#%02x%02x%02x' % rgb eli (1,2,3) tuple
    pass

def main():
    createWindow()

if __name__=="__main__":
    main()
