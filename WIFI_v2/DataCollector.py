"""
    This file contains the DataCollector class, which is used to collect data from the ESP32.
    
"""

import serial
import time
import csv
import serial
import time


class DataCollector:
    def __init__(self, port, baudrate, filename):
        self.ser = serial.Serial(port, baudrate) # open the serial connection
        self.filename = filename # set the filename

    def clearData(self): # clears the data in the CSV file and writes the header
        with open(self.filename, 'w') as file:
            file.write('time,SSID,RSSI,BSSID\n')

    def getData(self): # gets the data from the ESP32 and writes it to the CSV file
        while True: # loop until the ESP32 sends data
            if self.ser.in_waiting > 0: # if there is data in the serial buffer
                data = self.ser.readline().decode('utf-8').strip() # read the data from the serial buffer
                if data: # if the data is not empty

                    # conver the data to a CSV format and write it to the CSV file
                    with open(self.filename, 'a') as file: 
                        currentTime = str(time.strftime('%H:%M:%S', time.localtime()))
                        data = data.split(',')[0:-1]
                        for i in range(int((len(data))/3)): 
                            file.write(f'{currentTime},{str(data[(i*3):((i+1)*3)])[1:-1]}\n')
                        break