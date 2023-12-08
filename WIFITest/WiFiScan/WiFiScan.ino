#include "WiFi.h"

void setup() {
    Serial.begin(115200);

    // Set WiFi to station mode and disconnect from an AP if it was previously connected.
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);

    Serial.println("Setup done");
}

void loop() {
    int n = WiFi.scanNetworks();
    if (n == 0) {
        Serial.println("no networks found");
    } else {
        for (int i = 0; i < n; ++i) {

            if ((WiFi.SSID(i) == "AAU") or (WiFi.SSID(i) == "dlink")) {
              Serial.print(WiFi.SSID(i));
              Serial.print(",");
              Serial.print(WiFi.RSSI(i));
              Serial.print(",");
              Serial.print(WiFi.BSSIDstr(i));
              Serial.print(",");
            }
            delay(10);
        }
    }

    Serial.println("");
    WiFi.scanDelete();
    delay(150);
}
