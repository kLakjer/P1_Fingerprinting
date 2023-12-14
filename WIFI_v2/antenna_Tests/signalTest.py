import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def getArr(a):
    data = pd.read_csv(a)
    data['BSSID'] = data['BSSID'].str.strip().str.replace("'", "")
    data['RSSI'] = data['RSSI'].str.strip().str.replace("'", "")
    data['RSSI'] = pd.to_numeric(data['RSSI'], errors='coerce')
    arr = np.zeros((data.groupby('BSSID')['RSSI'].size().max(), data['BSSID'].nunique()))
        
    for i in range(data['BSSID'].nunique()):
        list = []
        for j in range(data.groupby('BSSID')['RSSI'].size().max()):
            try:
                list.append(data[data['BSSID'] == data['BSSID'].unique()[i]]['RSSI'].values[j])
            except:
                list.append(np.nan)
        arr[:,i] = list
    return arr

def linePlot(arr): # Funktionen der laver en graf over spillet hvor inputtet er et numpy array
        sampleSize = arr.shape[0]
        IDCount = arr.shape[1]
        
        plt.figure(figsize=(14, 10))  # sætter størelsen på vinduet

        cumulativeScore = np.cumsum(arr, axis=0) # Laver et numpy array med kumulative wins

        sampleCount = np.arange(1, sampleSize + 1) # Laver et numpy array med antal af spil spillet

        avgScore = cumulativeScore / sampleCount[:, None] # Laver et numpy array med win rates

        for i in range(IDCount): # Plotter win rates for hver spiller
            plt.plot(sampleCount, avgScore[:, i], label=f'Player {i+1}')

        plt.xlabel('Sample number')
        plt.ylabel('RSSI')
        plt.ylim(-70, -50)
        plt.title('Average RSSI over time')
        plt.legend()
        
def getAvg(a):
    arr = getArr(a)
    avg = np.nanmean(arr, axis=0)
    return avg

def main():
    linePlot(getArr('Test1_varierende.csv'))
    print(getAvg('Test1_varierende.csv'))

    linePlot(getArr('Test2_pegmod.csv'))
    print(getAvg('Test2_pegmod.csv'))

    linePlot(getArr('Test3_pegvaek.csv'))
    print(getAvg('Test3_pegvaek.csv'))
    plt.show()

if __name__ == '__main__':
    main()