"""
    Generates a plot of the data of the reference points.

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RF = 1

def getData(a): # Gets the data from the reference point with the number a
    data = pd.read_csv(a)
    data['BSSID'] = data['BSSID'].str.strip().str.replace("'", "")
    data['RSSI'] = data['RSSI'].str.strip().str.replace("'", "")
    return data

def plotBSSID(a): # creates a numpy array with the RSSI values for every BSSID over time
    data = getData(a)
    data['RSSI'] = pd.to_numeric(data['RSSI'], errors='coerce')
    arr = np.zeros((data.groupby('BSSID')['RSSI'].size().max(), data['BSSID'].nunique()))
    
    # fills the numpy array with the RSSI values
    for i in range(data['BSSID'].nunique()):
        list = []
        for j in range(data.groupby('BSSID')['RSSI'].size().max()):
            try:
                list.append(data[data['BSSID'] == data['BSSID'].unique()[i]]['RSSI'].values[j])
            except:
                list.append(np.nan)
        arr[:,i] = list
    return arr

def linePlot(arr): # creates a line plot of the RSSI values for every BSSID over time
        sampleSize = arr.shape[0]
        IDCount = arr.shape[1]
        
        plt.figure(figsize=(14, 10)) # sets the size of the plot

        cumulativeScore = np.cumsum(arr, axis=0) # cumulative sum of the RSSI values

        sampleCount = np.arange(1, sampleSize + 1) # creates an array with the sample numbers

        avgScore = cumulativeScore / sampleCount[:, None] # calculates the average RSSI value for every BSSID over time

        for i in range(IDCount): # plots the average RSSI values for every BSSID over time
            plt.plot(sampleCount, avgScore[:, i], label=f'Sample {i+1}')

        # sets the labels and title of the plot
        plt.xlabel('Sample number')
        plt.ylabel('RSSI')
        plt.title('Average RSSI over time')
        plt.legend()
        plt.show()

def main(): # main function
    plotBSSID(f'RFData/R{RF}.csv')
    linePlot(plotBSSID(f'RFData/R{RF}.csv'))

if __name__ == '__main__':
    main()
