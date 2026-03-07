import serial
from pynput.keyboard import Controller as Keyboard 
from pynput.mouse import Controller as Mouse

SAMPLES = 150
DEADZONE = 750

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

up_held = down_held = left_held = right_held = False

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
        wasdx = joy2_x - centers[2]
        wasdy = joy2_y - centers[3]

        up = down = left = right = False 
        
        DOMINANCE = 1.5

        if abs(wasdx) > DEADZONE or abs(wasdy) > DEADZONE:
            if abs(wasdx) > abs(wasdy) * DOMINANCE: 
                right = wasdx > 0 
                left = wasdx < 0 
            elif abs(wasdy) > abs(wasdx) * DOMINANCE:
                down = wasdy > 0 
                up = wasdy < 0

        if up and not up_held: 
            print("right")
            keyboard.press("d")
            up_held = True
        if not up and up_held:
            print("released right")
            keyboard.release("d")
            up_held = False
        if down and not down_held: 
            print("left")
            keyboard.press("a")
            down_held = True 
        if not down and down_held:
            print("released left")
            keyboard.release("a")
            down_held = False 
        if left and not left_held: 
            print("up")
            keyboard.press("w")
            left_held = True 
        if not left and left_held:
            print("released up")
            keyboard.release("w")
            left_held = False 
        if right and not right_held: 
            print("down")
            keyboard.press("s")
            right_held = True  
        if not right and right_held:
            print("released down")
            keyboard.release("s")
            right_held = False 
        # UP IS WHAT LEFT USED TO BE 
        # RIGHT IS WHAT UP USED TO BE 
        # DOWN IS WHAT RIGHT USED TO BE 
        # LEFT IS WHAT DOWN USED TO BE  
        dx = joy1_x - centers[0]
        dy = joy1_y - centers[1]
        mx = my = 0 
        if abs(dx) > DEADZONE:
            mx = dx - DEADZONE if dx > 0 else dx + DEADZONE 
        if abs(dy) > DEADZONE:
            my = dy - DEADZONE if dy > 0 else dy + DEADZONE
        if abs(dx) > DEADZONE or abs(dy) > DEADZONE:
            mouse.move(int(mx * 0.01),int(my * 0.01))
            print(f"Mouse moved {int(my)} pixels up/down and {int(mx)} pixels right/left")
    else: 
        print("(incomplete packet)")

