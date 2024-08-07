//ARDUINO CODE TO CONTROL VIA WEBSOCKET 5 SERVOS
//DEV: Maximiliano Mansilla
//GITHUB: https://github.com/maxbot86
//Year: 2024
//================================================
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "XXXXX";
const char* password = "YYYYY";

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

#define SERVOMIN  150 // Valor mínimo del pulso
#define SERVOMAX  600 // Valor máximo del pulso

void moveServo(int servoNum, int angle) {
  uint16_t pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(servoNum, 0, pulse);
}

void onWsEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
  if (type == WS_EVT_DATA) {
    String msg = "";
    for (size_t i = 0; i < len; i++) {
      msg += (char) data[i];
    }
      Serial.println(msg);
    if (msg.startsWith("SERVO1:")) {
      int angle = msg.substring(7).toInt();
      moveServo(0, angle); // Canal 0 para SERVO1
      Serial.println("Servo 01 - MOVE");

    } else if (msg.startsWith("SERVO2:")) {
      int angle = msg.substring(7).toInt();
      moveServo(1, angle); // Canal 1 para SERVO2
      Serial.println("Servo 02 - MOVE");

    }else if (msg.startsWith("SERVO3:")) {
      int angle = msg.substring(7).toInt();
      moveServo(2, angle); // Canal 2 para SERVO3
      Serial.println("Servo 03 - MOVE");

    }else if (msg.startsWith("SERVO4:")) {
      int angle = msg.substring(7).toInt();
      moveServo(3, angle); // Canal 3 para SERVO4
      Serial.println("Servo 04 - MOVE");

    }else if (msg.startsWith("SERVO5:")) {
      int angle = msg.substring(7).toInt();
      moveServo(4, angle); // Canal 4 para SERVO5
      Serial.println("Servo 05 - MOVE");
    }
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.hostname("ROBOTHAND01");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  pwm.begin();
  pwm.setPWMFreq(60);  // Frecuencia para servos

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  server.begin();
}

void loop() {
  ws.cleanupClients();
}
