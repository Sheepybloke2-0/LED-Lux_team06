import serial

# Configs for connecting to ZigBee
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# Remote nodes and data
DATA_SEND = "A2"

# Launch class and try to open
xbee = serial.Serial(PORT,BAUD_RATE)

while True:
    try:
        xbee.write(DATA_SEND.encode())
        print(DATA_SEND)
        print(xbee.read(4))
    except KeyboardInterrupt:
        break

xbee.close()
