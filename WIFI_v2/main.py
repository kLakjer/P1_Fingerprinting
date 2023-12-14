"""
    This is the main file of the project. It is used to run the program.

    The program will compare the data from the reference points with the data from the real time data.

"""

import pandas as pd
import math
from DataCollector import DataCollector
import time

def getRfData(a): # returns the data from the reference point with the number a
    filename = f'avgRF/avgRSSI_{a}.csv'
    df = pd.read_csv(filename)
    return df

def getRtData(): # returns the data from the ESP32 in real-time
    # get the data from the ESP32 using the DataCollector class
    collector = DataCollector('COM4', 115200, 'Rt.csv')
    collector.clearData()
    collector.getData()

    # read the data from the CSV file into a pandas dataframe
    df = pd.read_csv('Rt.csv')
    df['BSSID'] = df['BSSID'].str.strip().str.replace("'", "")
    df['RSSI'] = df['RSSI'].str.strip().str.replace("'", "")

    return df

def checkBestMatch(): # compares the data from the reference points with the real-time data

    # get the data from the reference points and the real-time data
    rPoints = [0]
    Rt = getRtData()
    RDiff = {}
    rfPoints = 9

    # calculate the difference between the reference points and the real-time data
    for j in range(1,rfPoints+1): # for every reference point
        RDiff[j] = 0
        rPoints.append(getRfData(j))
        R = rPoints[j]

        # calculate the difference between the reference point and the real-time data
        for i in range(len(Rt)): # for every BSSID in the real-time data
            if Rt['BSSID'].iloc[i] in R['BSSID'].values: # if the BSSID is in the reference point data
                BSSID = Rt['BSSID'].iloc[i]
                RDiff[j] += abs(float(R['RSSI'][R['BSSID'] == BSSID].iloc[0]) - float(Rt['RSSI'].iloc[i])) ** 2
            else:
                RDiff[j] += (100 - abs(float(Rt['RSSI'].iloc[i]))) ** 2
        
        # calculate the difference between the reference point and the real-time data
        for i in range(len(R['BSSID'])): # for every BSSID in the reference point data
            if R['BSSID'].iloc[i] not in Rt['BSSID'].values: # if the BSSID is not in the real-time data
                RDiff[j] += (100 - abs(float(R['RSSI'].iloc[i]))) ** 2

    # calculate the square root of the difference for every reference point
    for i in range(1, len(RDiff) + 1):
        RDiff[i] = math.sqrt(RDiff[i])

    # get the reference point with the lowest difference
    winner = min(RDiff, key=RDiff.get)
    if len(Rt) < 3:
        winnerStr = f"{winner} (uncertain data)"
    else:
        winnerStr = winner
    
    # return the reference point with the lowest difference, the RDiff dictionary and the winner
    return f'Best match: {winnerStr}', RDiff, winner

def main(): # main function
    result, RDiff, winner = checkBestMatch() # get the results of the comparison
    print(result, RDiff) # print the results in the terminal

if __name__ == '__main__':

    # run the main function until the program is stopped
    while True:
        main()
        time.sleep(0.5)