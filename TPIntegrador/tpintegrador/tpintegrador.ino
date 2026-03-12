#include "SevSeg.h"
#include <IRremote.hpp>
#include <EEPROM.h>

SevSeg sevseg;

#define IR_PIN A0

int totalChannels;
int actualChannel;
String channel;
void setup(){
  Serial.begin(9600);

  byte numDigits = 4;
  byte digitPins[] = {10, 11, 12, A1};
  byte segmentPins[] = {9, 2, 3, 5, 6, 8, 7, 4};

  bool resistorsOnSegments = true; 
  bool updateWithDelaysIn = false;
  byte hardwareConfig = COMMON_CATHODE; 

  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);

  IrReceiver.begin(IR_PIN, DISABLE_LED_FEEDBACK);

  EEPROM.get(2, actualChannel);
  if (actualChannel == -1L) {
    actualChannel = 1;
    totalChannels = 1;
    EEPROM.put(2, actualChannel);
    EEPROM.put(0, totalChannels);
  }
  else {
    EEPROM.get(2, actualChannel);
    EEPROM.get(0, totalChannels);
  }
}

void loop(){

  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("0")) {
      Serial.println(actualChannel);
    } else if (line.startsWith("-3")) {
      int firstComma = line.indexOf(',');
      totalChannels = line.substring(firstComma + 1).toInt();
      EEPROM.put(0, totalChannels);
    } else {
      actualChannel = line.toInt();
      EEPROM.put(2, actualChannel);
    }
  }

  if (IrReceiver.decode()) {
    if (!IrReceiver.decodedIRData.flags) { 
      if(IrReceiver.decodedIRData.command == 69) {
        actualChannel -= 1;
        if (actualChannel < 1) {
          actualChannel = totalChannels;
        }
        Serial.println("-2");
      } else if(IrReceiver.decodedIRData.command == 70) {
        actualChannel += 1;
        if (actualChannel > totalChannels) {
          actualChannel = 1;
        }
        Serial.println("Actual channel" + String(actualChannel));
        Serial.println("Total channel" + String(totalChannels));
        Serial.println("-1");
      }
    }
    EEPROM.put(2, actualChannel);

    IrReceiver.resume();
  }

  if (actualChannel < 10) {
    channel = "0" + String(actualChannel); 
  }
  else {
    channel = String(actualChannel);
  }
  sevseg.setChars(("CH" + channel).c_str());
  sevseg.refreshDisplay();
}