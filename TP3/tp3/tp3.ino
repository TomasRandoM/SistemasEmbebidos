#include <EEPROM.h>

long seconds = 0;
int direction;

void setup() {
  pinMode(13, OUTPUT);
  pinMode(11, OUTPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), interruptHandler2,   RISING);
  attachInterrupt(digitalPinToInterrupt(3), interruptHandler3,   RISING);
  EEPROM.get(0, direction);
  if (direction == -1L) {
    digitalWrite(13, HIGH);
    direction = 2;
    EEPROM.put(0, direction);
  }
  else {
    EEPROM.get(0, direction);
  }

}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("0")) {
      int firstComma = line.indexOf(',');
      seconds = atol(line.substring(firstComma + 1).c_str());
    } else if (line.startsWith("1")) {
      long value;
      int pin;
      for (int index = 2; index < direction; index += 6) {
        EEPROM.get(index, value);
        EEPROM.get(index+4, pin);
        Serial.print(value);
        Serial.print("-");
        Serial.print(pin);
        Serial.print(",");
      }
      Serial.println("");
    } else if (line.startsWith("2")) {
      eraseEeprom();
    }
    

  }
  delay(1000);
  seconds++;

  
}

void eraseEeprom() {
  for (int i = 0; i < EEPROM.length(); i++) {
    EEPROM.write(i, 0xFF);
  }
  direction = 2;
  EEPROM.put(0, direction);
}

void interruptHandler2() {
  EEPROM.put(direction, seconds);
  direction += 4;
  EEPROM.put(direction, 2);
  direction += 2;
  EEPROM.put(0, direction);
}

void interruptHandler3() {
  EEPROM.put(direction, seconds);
  direction += 4;
  EEPROM.put(direction, 3);
  direction += 2;
  EEPROM.put(0, direction);
}
