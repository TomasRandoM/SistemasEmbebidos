#include <EEPROM.h>

int peopleCount;
long distance;
int trigPin = 2;
int echoPin = 3;
bool configurated = false;
long wallDistance = 0;
int buzzerPin = 4;
long duration;
void setup() {
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    for (int i = 6; i < 14; i++) {
        pinMode(i, OUTPUT);
    }

    EEPROM.get(0, peopleCount);
    if (peopleCount == -1L) {
        peopleCount = 0;
        EEPROM.put(0, peopleCount);
    }
    else {
        EEPROM.get(0, peopleCount);
    }
}

void loop() {
    if (!configurated) {
        configuration();
    }

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    duration = pulseIn(echoPin, HIGH);

    distance = duration * 0.034 /2;

    if(distance < wallDistance - 5) {
        detectPerson();
        Serial.println(peopleCount);
    }
    
    delay(50);

    if (Serial.available()) {
        String line = Serial.readStringUntil('\n');
        line.trim();

        if (line.startsWith("-3")) {
            peopleCount = 0;
            EEPROM.put(0, peopleCount);
        }
        else {
            if (line.startsWith("-4")) {
                Serial.println(peopleCount);
            }
        }
    }
}


void configuration() {
    int distanceCount = 0;
    int samples = 10;
    long distanceVec[samples];
    for (int i = 0; i < samples; i++) {
        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);
        duration = pulseIn(echoPin, HIGH);
        distance = duration * 0.034 /2;
        distanceVec[i] = distance;
        distanceCount += distance;
        delay(50);
    }

    wallDistance = distanceCount / samples;
    
    long closest = distanceVec[0];
    long actualDiff = abs(distanceVec[0] - wallDistance);
    for (int i = 0; i < samples; i++) {
        long diff = abs(distanceVec[i] - wallDistance);
        if (diff < actualDiff) {
            actualDiff = diff;
            closest = distanceVec[i];
        }
    }
    wallDistance = closest;

    configurated = true;
    
}

void detectPerson() {
    unsigned long startTime = millis();
    bool personDetected = true;
    bool alarmActivated = false;

    while (millis() - startTime < 500) {

        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);
            
        duration = pulseIn(echoPin, HIGH);

        distance = duration * 0.034 / 2;
        if (distance > wallDistance - 5) {
            personDetected = false;
            break;
        }
        delay(50);
    }
    
    if (personDetected) {
        startTime = millis();
        peopleCount += 1;
        EEPROM.put(0, peopleCount);

        for (;;) {
            digitalWrite(trigPin, LOW);
            delayMicroseconds(2);
            digitalWrite(trigPin, HIGH);
            delayMicroseconds(10);
            digitalWrite(trigPin, LOW);
                
            duration = pulseIn(echoPin, HIGH);

            distance = duration * 0.034 / 2;
            if (!alarmActivated) {
                if (millis() - startTime > 1500) {
                    for (int i = 6; i < 14; i++) {
                        digitalWrite(i, HIGH);
                    }
                    digitalWrite(buzzerPin, HIGH);
                    Serial.println("-1");
                    alarmActivated = true;
                }
            }
            if (distance > wallDistance - 5) {
                personDetected = false;
                if (alarmActivated) {
                    for (int i = 6; i < 14; i++) {
                        digitalWrite(i, LOW);
                    }
                    digitalWrite(buzzerPin, LOW);
                    Serial.println("-2");
                }
                break;
            }
            delay(50);
        }
    }
}