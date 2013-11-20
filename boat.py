import pyglet
import serial
import struct
from jaraco.input import Joystick
from pyglet.window import key, Window


arial = pyglet.font.load('Arial', 14, bold=True, italic=False)

window = Window()
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
fps_display = pyglet.clock.ClockDisplay()
string_display = pyglet.text.Label('NULL', y=128)

joysticks = Joystick.enumerate_devices()
xbox = joysticks[0]
print xbox

xbox_axes = {}

@xbox.event
def on_axis(axis, value):
    xbox_axes[axis] = value
    print(axis, value)

xbee = serial.Serial('COM6', baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE)

prop = 7
rudder = 7

def squash(x):
    if abs(x) < 0.1:
        return 0
    if x < 0:
        return -(abs(x)**0.5)
    return x**0.5

@window.event
def on_draw():
    window.clear()
    fps_display.draw()

    xbox.dispatch_events()

    if keyboard[key.UP]:
        prop = 14
    elif keyboard[key.DOWN]:
        prop = 0
    else:
        prop = 7 + int(squash(xbox_axes.get('l_thumb_y', 0)) * 7)

    if keyboard[key.LEFT]:
        rudder = 0
    elif keyboard[key.RIGHT]:
        rudder = 14
    else:
        rudder = 7 + int(squash(xbox_axes.get('r_thumb_x', 0)) * 7)

    data = struct.pack("BBBBBBBBBBB",
            91,
            7 + 65,
            rudder + 65,
            prop + 65,
            1 + 65,
            65, 65, 65, 65, 65,
            93
            )
    string_display.text = data
    string_display.draw()

    xbee.write(data)

pyglet.app.run()
