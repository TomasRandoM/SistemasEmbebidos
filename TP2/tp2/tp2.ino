#include <Arduino_FreeRTOS.h>
#include <semphr.h>

SemaphoreHandle_t mutex;
SemaphoreHandle_t activateSemaphore;   
SemaphoreHandle_t deactivateSemaphore; 

volatile bool readActivated = true;
int a3Value;

void TaskAnalogRead(void *pvParameters);
void TaskAnalogWrite(void *pvParameters);
void TaskControlRead(void *pvParameters); 
void BlinkFunction(void *pvParameters);


void setup() {
  Serial.begin(9600);

  mutex = xSemaphoreCreateMutex();
  activateSemaphore   = xSemaphoreCreateBinary();
  deactivateSemaphore = xSemaphoreCreateBinary();

  xTaskCreate(TaskAnalogRead,   "AnalogRead",   128, NULL, 1, NULL);
  xTaskCreate(TaskAnalogWrite,  "AnalogWrite",  128, NULL, 1, NULL);
  xTaskCreate(TaskControlRead,  "ControlRead",  128, NULL, 2, NULL); 
  xTaskCreate(BlinkFunction,  "Blink",  128, NULL, 1, NULL); 
  attachInterrupt(digitalPinToInterrupt(2), interruptHandlerActivate,   RISING);
  attachInterrupt(digitalPinToInterrupt(3), interruptHandlerDeactivate, RISING);
}

void loop() {}

void interruptHandlerActivate() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  xSemaphoreGiveFromISR(activateSemaphore, &xHigherPriorityTaskWoken);
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR(); 
  }
}

void interruptHandlerDeactivate() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  xSemaphoreGiveFromISR(deactivateSemaphore, &xHigherPriorityTaskWoken);
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR(); 
  }
}

void TaskControlRead(void *pvParameters) {
  (void) pvParameters;
  for (;;) {
    if (xSemaphoreTake(activateSemaphore, 30) == pdPASS) {
      readActivated = true;
      Serial.println("-2");
    }

    if (xSemaphoreTake(deactivateSemaphore, 30) == pdPASS) {
      readActivated = false;
      Serial.println("-3");
    }
    vTaskDelay(pdMS_TO_TICKS(20));
  }
}

void TaskAnalogRead(void *pvParameters) {
  (void) pvParameters;
  bool alarmActivated = false;
  pinMode(A3, INPUT);
  pinMode(12, OUTPUT);
  for (;;) {
    if (Serial.available()) {

      String line = Serial.readStringUntil('\n');
      line.trim();

      if (line.startsWith("-2")) {
        readActivated = true;
      }
      else if (line.startsWith("-3")) {
        readActivated = false;
      }
    }

    if (readActivated) {
      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdPASS) {
        a3Value = analogRead(A3);
        if (a3Value > 800) {
          alarmActivated = true;
          Serial.println("-1");
        }
        
        xSemaphoreGive(mutex);
      }
    }
    else {
      if (alarmActivated == true) {
        alarmActivated = false; 
        Serial.println("-4");
      }
      
      
    }
    if(alarmActivated) {
      digitalWrite(12, HIGH);
      vTaskDelay(pdMS_TO_TICKS(100));
      digitalWrite(12, LOW);
      vTaskDelay(pdMS_TO_TICKS(100));
    }
  vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void TaskAnalogWrite(void *pvParameters) {
  (void) pvParameters;
  for (;;) {
    if (readActivated) {
      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdPASS) {
        Serial.println(a3Value);
        xSemaphoreGive(mutex);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(3000));
  }
}


void BlinkFunction(void *pvParameters) {
  (void) pvParameters;
  pinMode(11, OUTPUT);
  for (;;) {
    if (readActivated) {
      digitalWrite(11, HIGH);
      vTaskDelay(pdMS_TO_TICKS(100));
      digitalWrite(11, LOW);
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}


