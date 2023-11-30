import serial
import time
import csv

# Define the serial port and baud rate
ser = serial.Serial('COM4', 115200)  # Replace 'COMx' with your ESP32's serial port

wifiIDs = {
    "6C:31:0E:F3:55:E6": "AAU1",
    "3C:51:0E:13:FD:86": "AAU2",
    "6C:31:0E:BA:0A:A6": "AAU3",
    }

def clearData():
    with open('networks.csv', 'w') as file:
        file.write("time,SSID,RSSI,BSSID\n")

# Open a file to write the received data
def getData():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # Read a line of data from the serial port
            if data:
                with open('networks.csv', 'a') as file:
                    currentTime = str(time.strftime("%H:%M:%S", time.localtime()))
                    data = data.split(",")[0:-1]
                    for i in range(int((len(data))/3)):
                        file.write(f"{currentTime},{str(data[(i*3):((i+1)*3)])[1:-1]}\n")
                    break

# This is a test

def main():
    clearData()
    for i in range(1):
        getData()

if __name__ == '__main__':
    main()
