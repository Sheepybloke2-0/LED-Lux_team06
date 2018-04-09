import serial
import time
import tty
import sys
import termios

# Configs for connecting to ZigBee
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# Node IDs
NODE_IDS = ['01', '02', '03']

# Launch class and try to open
xbee = serial.Serial(PORT,BAUD_RATE)


class _Getch:
    '''Use Getch for WS inputs'''
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def test_all_on():
    '''Try and set all the lights to on. XBee ID 00 is the avg'''
    command = b'0n\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(5)


def test_all_off():
    '''Try and set all the lights to off. XBee ID 00 is the avg'''
    command = b'0o\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(5)


# def test_all_avg():
#     '''Try and set all the lights to avg. XBee ID 00 is the avg'''
#     command = b'0a\n'
#     xbee.write(command)
#     print(xbee.read(3))
#     # Give it time to change
#     time.sleep(5)


def test_all_plus_warm():
    '''Try and increment the time by one. XBee ID 00 is the avg'''
    command = b'0w\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(1.5)


def test_all_minus_warm():
    '''Try and decrement the time by one. XBee ID 00 is the avg'''
    command = b'0c\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(1.5)


def test_all_minus_bright():
    '''Try and decrement the time by one. XBee ID 00 is the avg'''
    command = b'0v\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(1.5)


def test_all_plus_bright():
    '''Try and decrement the time by one. XBee ID 00 is the avg'''
    command = b'0b\n'
    xbee.write(command)
    print(xbee.read(1).decode('utf-8'))
    # Give it time to change
    time.sleep(1.5)


def test_single_on():
    '''Iterate through each light, and turn each one on'''
    for id in NODE_IDS:
        command = id + 'n\n'
        xbee.write(command)
        print(xbee.read(2)).decode('utf-8')
        # Give it time to change
    time.sleep(5)


def test_single_off():
    '''Iterate through each light, and turn each one off'''
    for id in NODE_IDS:
        command = id + 'f\n'
        xbee.write(command)
        print(xbee.read(3))
        # Give it time to change
    time.sleep(5)


def test_single_avg():
    '''Iterate through each light, and set each one to avg'''
    for id in NODE_IDS:
        command = id + 'a\n'
        xbee.write(command)
        print(xbee.read(3))
        # Give it time to change
    time.sleep(1.5)


def test_single_plus():
    '''Iterate through each light, and set each one to increment by one'''
    for id in NODE_IDS:
        command = id + 'p\n'
        xbee.write(command)
        print(xbee.read(3))
        # Give it time to change
    time.sleep(5)


def test_single_minus():
    '''Iterate through each light, and set each one to decrement by one'''
    for id in NODE_IDS:
        command = id + 'm\n'
        xbee.write(command)
        print(xbee.read(3))
        # Give it time to change
    time.sleep(5)


def wasd():
    '''Use the WASD keys to turn the brightness up or down'''
    print("Use W or S to increase or decrease the brightness!")
    in_key = _Getch()
    id = 0
    while True:
        try:
            while True:
                k = in_key()
                if k != '': break
            if k == 'w':
                command = NODE_IDS[id] + 'p\n'
            elif k == 's':
                command = NODE_IDS[id] + 'm\n'
            elif k == 'a':
                id += 1
            elif k == 'd':
                id -= 1

            if id == -1:
                id = 2
            elif id == 3:
                id = 0
            xbee.write(command)
            print(xbee.read(3))
        except KeyboardInterrupt:
            break

# Run and list the tests here
if __name__ == '__main__':
    print("Waiting for ready")
    xbee.write(b'1\n')
    data = xbee.read(1)
    print(data)
    xbee.write(b'0o\n')
    time.sleep(5)
    test_all_on()
    # test_all_avg()
    print("Adding bright")
    for i in range(0,50):
        test_all_plus_bright()
    print("Adding Warm")
    for i in range(0,50):
        test_all_plus_warm()
    print("Adding Cool")
    for i in range(0,50):
        test_all_minus_warm()
    print("Reducing bright")
    for i in range(0,50):
        test_all_minus_bright()
    test_all_off()
    # test_single_on()
    # test_single_avg()
    # test_single_plus()
    # test_single_minus()
    # test_single_off()
    # wasd()
    xbee.close()
