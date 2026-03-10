#include "SevSeg.h"
#include <IRremote.hpp>

SevSeg sevseg;

#define IR_PIN A0

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
}

void loop(){

  if (IrReceiver.decode()) {
    Serial.print("Command: ");
    Serial.println(IrReceiver.decodedIRData.command);
    IrReceiver.resume();
  }

  sevseg.setNumber(5921,3);
  sevseg.refreshDisplay();
}