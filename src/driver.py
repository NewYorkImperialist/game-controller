from re import template
import serial
from pynput.keyboard import Controller as Mouse 
from pynput.mouse import Controller as Keyboard 

SAMPLES = 50
DEADZONE = 500

keyboard = Keyboard()
mouse = Mouse()

ser = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=1)
print("Connected! Waiting for data...")

centers = [0, 0, 0, 0]
for _ in range(SAMPLES):
    packet = ser.read(11)
    if len(packet) == 11:
        centers[0] += packet[1] | (packet[2] << 8)
        centers[1] += packet[3] | (packet[4] << 8)
        centers[2] += packet[5] | (packet[6] << 8)
        centers[3] += packet[7] | (packet[8] << 8)
    else:
        print("(incomplete packet)")
centers = [i / SAMPLES for i in centers]

while True:
    packet = ser.read(11)
    if len(packet) == 11:
        joy1_x = packet[1] | (packet[2] << 8)
        joy1_y = packet[3] | (packet[4] << 8)
        joy2_x = packet[5] | (packet[6] << 8)
        joy2_y = packet[7] | (packet[8] << 8)
        key = packet[9]
        checksum = packet[10]
        #print(f"J1: ({joy1_x}, {joy1_y}) J2: ({joy2_x}, {joy2_y}) Key: {key} Checksum: {checksum:02X}")
        if (joy2_y - centers[1] > DEADZONE):
            down = True
        else: down = False
        if (centers[1] - joy2_y > DEADZONE):
            up = True
        else: up = False
        if (joy2_x - centers[0] > DEADZONE):
            right = True
        else: right = False
        if (centers[0] - joy2_x > DEADZONE):
            left = True
        else: left = False 
        if up: print("up")
        if down: print("down")
        if left: print("left")
        if right: print("right")
        # UP IS WHAT LEFT USED TO BE 
        # RIGHT IS WHAT UP USED TO BE 
        # DOWN IS WHAT RIGHT USED TO BE 
        
    else: 
        print("(incomplete packet)")

