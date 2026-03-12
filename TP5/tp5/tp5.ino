#include <Arduino_FreeRTOS.h>

int ldr = A3;
int valorLDR = 0;

void setup() {
  Serial.begin(9600);

  xTaskCreate(TaskAnalogRead, "AnalogRead", 128, NULL, 1, NULL);
}

void loop() {
}


void TaskAnalogRead(void *pvParameters) {
  (void) pvParameters;
  for (;;) {

    if (Serial.available()) {
      String line = Serial.readStringUntil('\n');
      line.trim();

      if (line.startsWith("0")) {
        valorLDR = analogRead(ldr);
        Serial.println(valorLDR);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}