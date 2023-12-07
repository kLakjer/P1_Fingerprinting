import pandas as pd

def getData(a):
    data = pd.read_csv(a)
    data['BSSID'] = data['BSSID'].str.strip().str.replace("'", "")
    data['RSSI'] = data['RSSI'].str.strip().str.replace("'", "")
    return data

def avgBSSID(a):
    data = getData(a)
    data['RSSI'] = pd.to_numeric(data['RSSI'], errors='coerce')
    average_rssi = data.groupby('BSSID')['RSSI'].mean().reset_index()
    return average_rssi

def BSSIDdataSize(a):
    data = getData(a)
    BSSIDSize = data.groupby('BSSID')['RSSI'].size().reset_index()
    return BSSIDSize

def saveToCSV(a):
    avgBSSID(a).to_csv(f'avgBSSID_{rf}.csv', index=False)

rf = 1
referencePoint = f'R{rf}.csv'

print(f"{referencePoint}:")
print(avgBSSID(referencePoint))
print()
print("Antal målinger af BSSID:")
print(BSSIDdataSize(referencePoint))

saveToCSV(referencePoint)
