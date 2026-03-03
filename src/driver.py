import serial

ser = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=1)
print("Connected! Waiting for data...")

while True:
    packet = ser.read(11)
    if len(packet) == 11:
        joy1_x = packet[1] | (packet[2] << 8)
        joy1_y = packet[3] | (packet[4] << 8)
        joy2_x = packet[5] | (packet[6] << 8)
        joy2_y = packet[7] | (packet[8] << 8)
        key = packet[9]
        checksum = packet[10]
        print(f"J1: ({joy1_x}, {joy1_y}) J2: ({joy2_x}, {joy2_y}) Key: {key} Checksum: {checksum:02X}")
    else: 
        print("(incomplete packet)")

