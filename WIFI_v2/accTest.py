"""
    Used to test the accuracy of the RP's

    Start the measurement with startMeasurement() and commpare the result with the current position of the ESP32.

    Writes a CSV file with the results of the measurement. (bool: if the measurement was correct, data: the measured data)
"""

import main
from DataCollector import DataCollector
import pandas as pd
import time

def startMeasurement(): # starts the measurement and returns if the measurement was correct and the measured data
    while True:
        _, _, winner = main.checkBestMatch() # starts the measurement and returns the winner
        if (winner == 4): # if the winner is the correct one
            return True, winner # return True and the winner
        else:
            return False, winner # return False and the winner

def writeToCsv(RPNr, dataSize): # writes the results of the measurement to a CSV file
    with open(f'accuracy_Tests/Test_{RPNr}.csv', 'w') as file:
        file.write(f'bool,data\n')
        for i in range(dataSize): # do the measurement dataSize (amount of samples) times
            bool, data = startMeasurement() # start the measurement and get the results
            file.write(f'{bool},{data}\n') # write the results to the CSV file
            time.sleep(0.5) 
            print(f'{i+1} / {dataSize} done') # print the progress in the terminal

def getaccuracy(a): # calculates the accuracy of the RP with the number a
    data = pd.read_csv(f"accuracy_Tests/Test_{a}.csv") # read the CSV file

    # convert the data to numeric values
    data['bool'] = pd.to_numeric(data['bool'], errors='coerce') 
    data['data'] = pd.to_numeric(data['data'], errors='coerce') 

    # calculate the accuracy
    accuracy = data['bool'].sum()/len(data['bool'])
    print(f'Accuracy of RP_{a}: {accuracy}')


if __name__ == '__main__':
    #writeToCsv(10, 2)
    getaccuracy(1)
    getaccuracy(3)
    getaccuracy(4)
