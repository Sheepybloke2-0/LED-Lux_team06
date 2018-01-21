import serial
import threading
import atexit
from flask import Flask, render_template
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
#App functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rainbow/', endpoint='rainbow')
def rainbow():
    print('Running the rainbow lights!')
    send_mode_change("r")
    return '', 204

@app.route('/mood/', endpoint='mood')
def mood():
    print('Running the mood lights!')
    #add zigbee serial commands
    send_mode_change("m")
    return '', 204

@app.route('/candle/', endpoint='candle')
def candle():
    print('Running the candle lights!')
    #add zigbee serial commands
    send_mode_change("c")
    return '', 204

@app.route('/warmwhite/', endpoint='warmwhite')
def warmwhite():
    print('Running the warm white lights!')
    #add zigbee serial commands
    send_mode_change("w")
    return '', 204

@app.route('/wave/', endpoint='wave')
def wave():
    print('Running the wave lights!')
    #add zigbee serial commands
    send_mode_change("b")
    return '', 204

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
