#include <Arduino.h>
#include <Keypad.h>

#define VRX1 35
#define VRY1 34
#define VRX2 2
#define VRY2 4
#define START_BYTE 0xAA

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {{'1', '2', '3', 'A'},
                         {'4', '5', '6', 'B'},
                         {'7', '8', '9', 'C'},
                         {'*', '0', '#', 'D'}};

byte rowPins[ROWS] = {13, 12, 14, 27};
byte colPins[COLS] = {26, 25, 33, 32};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);
// __attribute__(()) -> [[]]
struct [[gnu::packed]] Packet {
  uint16_t joy1_x;
  uint16_t joy1_y;
  uint16_t joy2_x;
  uint16_t joy2_y;
  uint8_t key;
};
// u16 u16 u16 u16 u8 u8 u16

Packet p;

void setup() {
  Serial.begin(115200);
  pinMode(VRX1, INPUT);
  pinMode(VRY1, INPUT);
  pinMode(VRX2, INPUT);
  pinMode(VRY2, INPUT);
}

void loop() {
  p.joy1_x = analogRead(VRX1);
  p.joy1_y = analogRead(VRY1);
  p.joy2_x = analogRead(VRX2);
  p.joy2_y = analogRead(VRY2);
  char k = keypad.getKey();
  if (k == NO_KEY)
    p.key = 16; // NO_KEY
  else if (k >= '0' && k <= '9')
    p.key = k - '0'; // 0-9
  else if (k == 'A')
    p.key = 10;
  else if (k == 'B')
    p.key = 11;
  else if (k == 'C')
    p.key = 12;
  else if (k == 'D')
    p.key = 13;
  else if (k == '*')
    p.key = 14;
  else if (k == '#')
    p.key = 15;
  uint8_t buffer[10];
  buffer[0] = START_BYTE;
  buffer[1] = p.joy1_x & 0xFF;        // splits low end
  buffer[2] = (p.joy1_x >> 8) & 0xFF; // splits high end
  buffer[3] = p.joy1_y & 0xFF;
  buffer[4] = (p.joy1_y >> 8) & 0xFF;
  buffer[5] = p.joy2_x & 0xFF;
  buffer[6] = (p.joy2_x >> 8) & 0xFF;
  buffer[7] = p.joy2_y & 0xFF;
  buffer[8] = (p.joy2_y >> 8) & 0xFF;
  buffer[9] = p.key;
  uint8_t checksum = 0;
  for (int i = 1; i < 10; i++)
    checksum += buffer[i];
  Serial.write(buffer, 10);
  Serial.write(checksum);
  delay(5);
}
