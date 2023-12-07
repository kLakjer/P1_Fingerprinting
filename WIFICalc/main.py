import pandas as pd
import math 
import Test as t

def getRfData(a):
    data = pd.read_csv(f"avgBSSID_{a}.csv")
    return data

def getRtData():
    data = pd.read_csv("rt.csv")
    data['BSSID'] = data['BSSID'].str.strip().str.replace("'", "")
    data['RSSI'] = data['RSSI'].str.strip().str.replace("'", "")
    return data

def checkBestMatch():
    rPoints = [0]
    Rt = getRtData()
    RDiff = {}
    rfPoints = 6

    for j in range(1,rfPoints+1):
        RDiff[j] = 0
        rPoints.append(getRfData(j))
        R = rPoints[j]
        for i in range(len(Rt)):
            if Rt['BSSID'].iloc[i] in R['BSSID'].values:
                BSSID = Rt['BSSID'].iloc[i]
                RDiff[j] += abs(float(R['RSSI'][R['BSSID'] == BSSID].iloc[0]) - float(Rt['RSSI'].iloc[i]))**2
            else:
                RDiff[j] += 100
    
    for i in range(1, len(RDiff)+1):
        RDiff[i] = math.sqrt(RDiff[i])

    winner = min(RDiff, key=RDiff.get)

    return f"Best match: {winner}", RDiff


def main():
    t.main()
    print(checkBestMatch())

if __name__ == '__main__':
    while True:
        main()
