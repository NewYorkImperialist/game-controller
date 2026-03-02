#include <Arduino.h>
#include <Keypad.h>

#define VRX1 35
#define VRY1 34
#define VRX2 2
#define VRY2 4

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {{'1', '2', '3', 'A'},
                         {'4', '5', '6', 'B'},
                         {'7', '8', '9', 'C'},
                         {'*', '0', '#', 'D'}};

byte rowPins[ROWS] = {13, 12, 14, 27};
byte colPins[COLS] = {26, 25, 33, 32};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);
void setup() {
  Serial.begin(115200);
  pinMode(VRX1, INPUT);
  pinMode(VRY1, INPUT);
  pinMode(VRX1, INPUT);
  pinMode(VRY1, INPUT);
}

void loop() {
  uint16_t x1 = analogRead(VRX1);
  uint16_t y1 = analogRead(VRY1);
  uint16_t x2 = analogRead(VRX2);
  uint16_t y2 = analogRead(VRY2);
  Serial.printf("%d, %d, %d, %d\n", x1, y1, x2, y2);
  char key = keypad.getKey();
  if (key) {
    Serial.println(key);
  }
}
