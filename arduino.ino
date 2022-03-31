#include <sensorShieldLib.h>

SensorShield board;

void setup() {
    board.init();
  
    board.addSensor("start", 3, INPUT_PULLUP);
    board.addSensor("record", 4, INPUT_PULLUP);
    board.addSensor("play", 5, INPUT_PULLUP);
    board.addSensor("previous", 6, INPUT_PULLUP);
    board.addSensor("next", 7, INPUT_PULLUP);
    board.addSensor("menu", A0);
    board.setSensorSensitivity("menu", 5);
}

void loop() {
    board.update(); 
}
