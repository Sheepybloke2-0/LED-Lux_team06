import serial
import threading
import atexit
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from xbee import XBee

#Global variable that both threads can access
lightMode = ""

#Treat lightMode as a mutex to ensure each thread has exclusive access to the variable
datalock = threading.Lock()
#Thread data struct
serialThread = threading.Thread()
RUN_TIME = 1 #seconds

#Assume that it attaches to USB1. Adjust as nessary by plugging in module and in terminal type dmesg
PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

#Init the Zigbee serial modules
ser = serial.Serial(PORT, BAUDRATE)
xbee = XBee(ser)

app = Flask(__name__)

class SliderForm(Form):
    brightness = IntegerRangeField('brightness', default=0);
    warm = IntegerRangeField('warm', default=0);
    cool = IntegerRangeField('cool', default=0);

#App functions
@app.route('/')
def index():
    slider = SliderForm(csrf_enabled=False)
    return render_template('index.html', form=slider)

@app.route('/L1')
def L1():
    slider = SliderForm(csrf_enabled=False)
    return render_template('L1.html', form=slider)

@app.route('/L2')
def L2():
    slider = SliderForm(csrf_enabled=False)
    return render_template('L2.html', form=slider)

@app.route('/L3')
def L3():
    slider = SliderForm(csrf_enabled=False)
    print slider
    return render_template('L3.html', form=slider)

@app.route('/brightness/')
def brightness():
    if (form.brightness.data == 0):
        send_mode_change("0b0")
    elif (form.brightness.data == 1):
        send_mode_change("0b1")
    elif (form.brightness.data == 2):
        send_mode_change("0b2")
    elif (form.brightness.data == 3):
        send_mode_change("0b3")
    elif (form.brightness.data == 4):
        send_mode_change("0b4")
    elif (form.brightness.data == 5):
        send_mode_change("0b5")
    return '', 204

# master
@app.route('/warm/')
def warm():
    if (form.warm.data == 0):
        send_mode_change("0w0")
    elif (form.warm.data == 1):
        send_mode_change("0w1")
    elif (form.warm.data == 2):
        send_mode_change("0w2")
    elif (form.warm.data == 3):
        send_mode_change("0w3")
    elif (form.warm.data == 4):
        send_mode_change("0w4")
    elif (form.warm.data == 5):
        send_mode_change("0w5")
    return '', 204

@app.route('/cool/')
def cool():
    if (form.cool.data == 0):
        send_mode_change("0c0")
    elif (form.cool.data == 1):
        send_mode_change("0c1")
    elif (form.cool.data == 2):
        send_mode_change("0c2")
    elif (form.cool.data == 3):
        send_mode_change("0c3")
    elif (form.cool.data == 4):
        send_mode_change("0c4")
    elif (form.cool.data == 5):
        send_mode_change("0c5")
    return '', 204

# L1
@app.route('/brightness1/')
def brightness():
    if (form.brightness.data == 0):
        send_mode_change("1b0")
    elif (form.brightness.data == 1):
        send_mode_change("1b1")
    elif (form.brightness.data == 2):
        send_mode_change("1b2")
    elif (form.brightness.data == 3):
        send_mode_change("1b3")
    elif (form.brightness.data == 4):
        send_mode_change("1b4")
    elif (form.brightness.data == 5):
        send_mode_change("1b5")
    return '', 204

@app.route('/warm1/')
def warm():
    if (form.warm.data == 0):
        send_mode_change("1w0")
    elif (form.warm.data == 1):
        send_mode_change("1w1")
    elif (form.warm.data == 2):
        send_mode_change("1w2")
    elif (form.warm.data == 3):
        send_mode_change("1w3")
    elif (form.warm.data == 4):
        send_mode_change("1w4")
    elif (form.warm.data == 5):
        send_mode_change("1w5")
    return '', 204

@app.route('/cool1/')
def cool():
    if (form.cool.data == 0):
        send_mode_change("1c0")
    elif (form.cool.data == 1):
        send_mode_change("1c1")
    elif (form.cool.data == 2):
        send_mode_change("1c2")
    elif (form.cool.data == 3):
        send_mode_change("1c3")
    elif (form.cool.data == 4):
        send_mode_change("1c4")
    elif (form.cool.data == 5):
        send_mode_change("1c5")
    return '', 204

# L2
@app.route('/brightness2/')
def brightness():
    if (form.brightness.data == 0):
        send_mode_change("2b0")
    elif (form.brightness.data == 1):
        send_mode_change("2b1")
    elif (form.brightness.data == 2):
        send_mode_change("2b2")
    elif (form.brightness.data == 3):
        send_mode_change("2b3")
    elif (form.brightness.data == 4):
        send_mode_change("2b4")
    elif (form.brightness.data == 5):
        send_mode_change("2b5")
    return '', 204

@app.route('/warm2/')
def warm():
    if (form.warm.data == 0):
        send_mode_change("2w0")
    elif (form.warm.data == 1):
        send_mode_change("2w1")
    elif (form.warm.data == 2):
        send_mode_change("2w2")
    elif (form.warm.data == 3):
        send_mode_change("2w3")
    elif (form.warm.data == 4):
        send_mode_change("2w4")
    elif (form.warm.data == 5):
        send_mode_change("2w5")
    return '', 204

@app.route('/cool2/')
def cool():
    if (form.cool.data == 0):
        send_mode_change("2c0")
    elif (form.cool.data == 1):
        send_mode_change("2c1")
    elif (form.cool.data == 2):
        send_mode_change("2c2")
    elif (form.cool.data == 3):
        send_mode_change("2c3")
    elif (form.cool.data == 4):
        send_mode_change("2c4")
    elif (form.cool.data == 5):
        send_mode_change("2c5")
    return '', 204

# L3
@app.route('/brightness3/')
def brightness():
    if (form.brightness.data == 0):
        send_mode_change("3b0")
    elif (form.brightness.data == 1):
        send_mode_change("3b1")
    elif (form.brightness.data == 2):
        send_mode_change("3b2")
    elif (form.brightness.data == 3):
        send_mode_change("3b3")
    elif (form.brightness.data == 4):
        send_mode_change("3b4")
    elif (form.brightness.data == 5):
        send_mode_change("3b5")
    return '', 204

@app.route('/warm3/')
def warm():
    if (form.warm.data == 0):
        send_mode_change("3w0")
    elif (form.warm.data == 1):
        send_mode_change("3w1")
    elif (form.warm.data == 2):
        send_mode_change("3w2")
    elif (form.warm.data == 3):
        send_mode_change("3w3")
    elif (form.warm.data == 4):
        send_mode_change("3w4")
    elif (form.warm.data == 5):
        send_mode_change("3w5")
    return '', 204

@app.route('/cool3/')
def cool():
    if (form.cool.data == 0):
        send_mode_change("3c0")
    elif (form.cool.data == 1):
        send_mode_change("3c1")
    elif (form.cool.data == 2):
        send_mode_change("3c2")
    elif (form.cool.data == 3):
        send_mode_change("3c3")
    elif (form.cool.data == 4):
        send_mode_change("3c4")
    elif (form.cool.data == 5):
        send_mode_change("3c5")
    return '', 204






# @app.route('/rainbow/', endpoint='rainbow')
# def rainbow():
#     send_mode_change("r")
#     return '', 204
#
# @app.route('/mood/', endpoint='mood')
# def mood():
#     print('Running the mood lights!')
#     #add zigbee serial commands
#     # send_mode_change("m")
#     return '', 204
#
# @app.route('/candle/', endpoint='candle')
# def candle():
#     print('Running the candle lights!')
#     #add zigbee serial commands
#     # send_mode_change("c")
#     return '', 204
#
# @app.route('/warmwhite/', endpoint='warmwhite')
# def warmwhite():
#     print('Running the warm white lights!')
#     #add zigbee serial commands
#     # send_mode_change("w")
#     return '', 204
#
# @app.route('/wave/', endpoint='wave')
# def wave():
#     print('Running the wave lights!')
#     #add zigbee serial commands
#     # send_mode_change("b")
#     return '', 204

#Starter and shutdown functions
def interrupt():
    global serialThread
    serialThread.cancel()

def send_mode_change( mode ):
    global serialThread
    global lightMode
    #lock the mutex for editting
    with datalock:
        lightMode = mode
    #start thread and run it for 5 seconds. Hopefully this is enough times
    serialThread = threading.Timer(RUN_TIME, serial_send, lightMode)
    serialThread.start()

def serial_send( lightMode ):
    ser.write(lightMode)

if __name__ == '__main__':
    #init zigbee module
    ser.open()
    app = create_app()
