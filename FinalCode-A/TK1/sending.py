#Python code for sending commands via Zigbee

#Zigbee library?
from xbee import XBee#, ZigBee
import serial

serial_port = serial.Serial('/dev/ttyUSB0') #example device location
xbee = XBee(serial_port) #may need to use ZigBee(serial_port)
#can do XBee(serial_port, callback = ) for asynchronous

while True:
    try:
        print(xbee.wait_read_frame()) #synchronous blocking read
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()

#to send via the XBee
xbee.send("at", frame='A', command="MY") #sends AT frame (marked A) with command to get the address
# aka xbee.at(frame='A', command="MY") and frame = a isnt fully necessary either

#I think this is what we'll want
xbee.tx()

#xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html
# ^ this gives another way of doing it if API library can't be found
