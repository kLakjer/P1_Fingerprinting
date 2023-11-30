import pandas as pd

wifiIDs = {
    "6C:31:0E:F3:55:E6": "AAU1",
    "3C:51:0E:13:FD:86": "AAU2",
    "6C:31:0E:BA:0A:A6": "AAU3",
    }

data = pd.read_csv("networks.csv")
df = pd.DataFrame(data)

print(df["SSID"])

