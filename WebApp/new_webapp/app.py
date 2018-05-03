import serial
import threading
import atexit
import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
# from xbee import XBee

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
# xbee = XBee(ser)

app = Flask(__name__)

# def sliderUpdate(form)

class SliderForm(Form):
    brightness = IntegerRangeField('brightness', default=2);
    warm = IntegerRangeField('warm', default=0);
    cool = IntegerRangeField('cool', default=0);

#App functions
@app.route('/')
def index():
    slider = SliderForm(request.form)
    print(slider.brightness.data)
    # ser.write("0f0")
    # print("0f0")
    return render_template('index.html', form=slider)

@app.route('/L1')
def L1():
    # slider = SliderForm(csrf_enabled=False)
    return render_template('L1.html', form=slider)

@app.route('/L2')
def L2():
    # slider = SliderForm(csrf_enabled=False)
    return render_template('L2.html', form=slider)

@app.route('/L3')
def L3():
    # slider = SliderForm(csrf_enabled=False)
    # print slider
    return render_template('L3.html', form=slider)

@app.route('/brightness', methods=['POST'], endpoint='brightness')
def brightness():
    if request.method == "POST":
        print(request)
    print("brightness")
    data = int(request.form['value'])

    if data == 0:
        print("writing 0")
        ser.write("0b0")
    elif (data == 1):
        print("writing 1")
        ser.write("0b1")
    elif (data == 2):
        print("writing 2")
        ser.write("0b2")
    elif (data == 3):
        print("writing 3")
        ser.write("0b3")
    elif (data == 4):
        print("writing 4")
        ser.write("0b4")
    elif (data == 5):
        print("writing 5")
        ser.write("0b5")
    return '', 204

# master
@app.route('/warm/', endpoint='warm')
def warm():
    print("warm")
    if (form.warm.data == 0):
        ser.write("0w0")
    elif (form.warm.data == 1):
        ser.write("0w1")
    elif (form.warm.data == 2):
        ser.write("0w2")
    elif (form.warm.data == 3):
        ser.write("0w3")
    elif (form.warm.data == 4):
        ser.write("0w4")
    elif (form.warm.data == 5):
        ser.write("0w5")
    return '', 204

@app.route('/cool/', endpoint='cool')
def cool():
    if (form.cool.data == 0):
        ser.write("0c0")
    elif (form.cool.data == 1):
        ser.write("0c1")
    elif (form.cool.data == 2):
        ser.write("0c2")
    elif (form.cool.data == 3):
        ser.write("0c3")
    elif (form.cool.data == 4):
        ser.write("0c4")
    elif (form.cool.data == 5):
        ser.write("0c5")
    return '', 204

# L1
@app.route('/brightness1/', endpoint='brightness1')
def brightness1():
    if (form.brightness.data == 0):
        ser.write("1b0")
    elif (form.brightness.data == 1):
        ser.write("1b1")
    elif (form.brightness.data == 2):
        ser.write("1b2")
    elif (form.brightness.data == 3):
        ser.write("1b3")
    elif (form.brightness.data == 4):
        ser.write("1b4")
    elif (form.brightness.data == 5):
        ser.write("1b5")
    return '', 204

@app.route('/warm1/', endpoint='warm1')
def warm1():
    if (form.warm.data == 0):
        ser.write("1w0")
    elif (form.warm.data == 1):
        ser.write("1w1")
    elif (form.warm.data == 2):
        ser.write("1w2")
    elif (form.warm.data == 3):
        ser.write("1w3")
    elif (form.warm.data == 4):
        ser.write("1w4")
    elif (form.warm.data == 5):
        ser.write("1w5")
    return '', 204

@app.route('/cool1/', endpoint='cool1')
def cool1():
    if (form.cool.data == 0):
        ser.write("1c0")
    elif (form.cool.data == 1):
        ser.write("1c1")
    elif (form.cool.data == 2):
        ser.write("1c2")
    elif (form.cool.data == 3):
        ser.write("1c3")
    elif (form.cool.data == 4):
        ser.write("1c4")
    elif (form.cool.data == 5):
        ser.write("1c5")
    return '', 204

# L2
@app.route('/brightness2/', endpoint='brightness2')
def brightness2():
    if (form.brightness.data == 0):
        ser.write("2b0")
    elif (form.brightness.data == 1):
        ser.write("2b1")
    elif (form.brightness.data == 2):
        ser.write("2b2")
    elif (form.brightness.data == 3):
        ser.write("2b3")
    elif (form.brightness.data == 4):
        ser.write("2b4")
    elif (form.brightness.data == 5):
        ser.write("2b5")
    return '', 204

@app.route('/warm2/', endpoint='warm2')
def warm2():
    if (form.warm.data == 0):
        ser.write("2w0")
    elif (form.warm.data == 1):
        ser.write("2w1")
    elif (form.warm.data == 2):
        ser.write("2w2")
    elif (form.warm.data == 3):
        ser.write("2w3")
    elif (form.warm.data == 4):
        ser.write("2w4")
    elif (form.warm.data == 5):
        ser.write("2w5")
    return '', 204

@app.route('/cool2/', endpoint='cool2')
def cool2():
    if (form.cool.data == 0):
        ser.write("2c0")
    elif (form.cool.data == 1):
        ser.write("2c1")
    elif (form.cool.data == 2):
        ser.write("2c2")
    elif (form.cool.data == 3):
        ser.write("2c3")
    elif (form.cool.data == 4):
        ser.write("2c4")
    elif (form.cool.data == 5):
        ser.write("2c5")
    return '', 204

# L3
@app.route('/brightness3/', endpoint='brightness3')
def brightness3():
    if (form.brightness.data == 0):
        ser.write("3b0")
    elif (form.brightness.data == 1):
        ser.write("3b1")
    elif (form.brightness.data == 2):
        ser.write("3b2")
    elif (form.brightness.data == 3):
        ser.write("3b3")
    elif (form.brightness.data == 4):
        ser.write("3b4")
    elif (form.brightness.data == 5):
        ser.write("3b5")
    return '', 204

@app.route('/warm3/', endpoint='warm3')
def warm3():
    if (form.warm.data == 0):
        ser.write("3w0")
    elif (form.warm.data == 1):
        ser.write("3w1")
    elif (form.warm.data == 2):
        ser.write("3w2")
    elif (form.warm.data == 3):
        ser.write("3w3")
    elif (form.warm.data == 4):
        ser.write("3w4")
    elif (form.warm.data == 5):
        ser.write("3w5")
    return '', 204

@app.route('/cool3/', endpoint='cool3')
def cool3():
    if (form.cool.data == 0):
        ser.write("3c0")
    elif (form.cool.data == 1):
        ser.write("3c1")
    elif (form.cool.data == 2):
        ser.write("3c2")
    elif (form.cool.data == 3):
        ser.write("3c3")
    elif (form.cool.data == 4):
        ser.write("3c4")
    elif (form.cool.data == 5):
        ser.write("3c5")
    return '', 204

#Starter and shutdown functions
def interrupt():
    global serialThread
    serialThread.cancel()

# def send_mode_change( mode ):
#     global serialThread
#     global lightMode
#     #lock the mutex for editting
#     with datalock:
#         lightMode = mode
#     #start thread and run it for 5 seconds. Hopefully this is enough times
#     for letter in lightMode:
#         serialThread = threading.Timer(RUN_TIME, serial_send, letter)
#         serialThread.start()
#         print(letter)

# def serial_send( lightMode ):
#     ser.write(lightMode)

if __name__ == '__main__':
    #init zigbee module
    ser.open()
    app = create_app()
