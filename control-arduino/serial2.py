import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
while True:
    if ser.in_waiting > 0:
        line = ser.read().decode('ascii').rstrip()
        print(line)
        time.sleep(0.05)
    ser.write(input().encode(encoding="ascii"))