"""
    Generate new reference points to be used in the main program.

    The program will generate a new csv file with the name R{rfPoint}.csv
"""

from DataCollector import DataCollector
import pandas as pd

rfPoint = 9 # the number of the reference point
count = 50 # the amount of samples to be taken

def startMeasurement(rfPoint, count): # starts the measurement

    # get the data from the ESP32 using the DataCollector class
    collector = DataCollector('COM4', 115200, f'RFData/R{rfPoint}.csv')
    collector.clearData()

    # get the data from the ESP32 a number of times
    for _ in range(count):
        collector.getData()

def avgRSSI(rfPoint): # calculates the average RSSI value for every BSSID

    # read the data from the CSV file into a pandas dataframe
    data = pd.read_csv(f"RFData/R{rfPoint}.csv")
    data['BSSID'] = data['BSSID'].str.strip().str.replace("'", "")
    data['RSSI'] = data['RSSI'].str.strip().str.replace("'", "")
    data['RSSI'] = pd.to_numeric(data['RSSI'], errors='coerce')

    # remove the BSSID's that are not in at least 75% of the samples
    maxbssid = data.groupby('BSSID')['RSSI'].size().max()
    data = data.groupby('BSSID').filter(lambda x: len(x) >= maxbssid*0.75)

    # calculate the average RSSI value for every BSSID
    average_rssi = data.groupby('BSSID')['RSSI'].mean().reset_index()
    average_rssi.to_csv(f'avgRF/avgRSSI_{rfPoint}.csv', index=False)

def main(): # main function
    startMeasurement(rfPoint, count) # start the measurement 
    avgRSSI(rfPoint) # calculate the average RSSI value for every BSSID

if __name__ == '__main__':
    main()