import serial

ser = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=1)
print("Connected! Waiting for data...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)
    else: 
        print("(no data)")

