from flask import Flask, render_template
from xbee import XBee
import serial

#Assume that it attaches to USB0. Adjust as nessary by plugging in module and in terminal type dmesg
PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

ser = serial.Serial(PORT, BAUDRATE)
xbee = XBee(ser)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rainbow/', endpoint='rainbow')
def rainbow():
    print('Running the rainbow lights!')
    #add zigbee serial commands
    ser.write("r")
    return '', 204

@app.route('/mood/', endpoint='mood')
def rainbow():
    print('Running the mood lights!')
    #add zigbee serial commands
    ser.write("r")
    return '', 204

@app.route('/candle/', endpoint='candle')
def rainbow():
    print('Running the candle lights!')
    #add zigbee serial commands
    ser.write("r")
    return '', 204

@app.route('/warmwhite/', endpoint='warmwhite')
def rainbow():
    print('Running the warm white lights!')
    #add zigbee serial commands
    ser.write("r")
    return '', 204

if __name__ == '__main__':
    #init zigbee module
    ser.open()
    app.run()
