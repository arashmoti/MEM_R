// Define the digital pin for output
const int outputPin_x = 2;
const int directionPin_x = 5;
const int outputPin_z = 4;
const int directionPin_z = 7;
const bool direction_x = 0;
const bool direction_z = 1;
int step_pulse_time = 255;
int pulse_delay = 5;
int number_of_pulses = 100;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set the output pins as output
  pinMode(outputPin_x, OUTPUT);
  pinMode(directionPin_x, OUTPUT);
  pinMode(outputPin_z, OUTPUT);
  pinMode(directionPin_z, OUTPUT);

  digitalWrite(outputPin_x, LOW);
  digitalWrite(directionPin_x, direction_x);
  digitalWrite(outputPin_z, LOW);
  digitalWrite(directionPin_z, direction_z);
}

void loop() {
  if (Serial.available()) {
    char receivedChar = Serial.read();

    // Check the received character
    if (receivedChar == 'X' || receivedChar == 'x') {
      digitalWrite(directionPin_x, direction_x);
      for (int i = 0 ; i < number_of_pulses; i++) {
        digitalWrite(outputPin_x, HIGH);  // Set the output pin HIGH
        delayMicroseconds(step_pulse_time);
        digitalWrite(outputPin_x, LOW);   // Set the output pin LOW
        delay(pulse_delay);
      }
      Serial.println("ok.");
    }

    else if (receivedChar == 'Z' || receivedChar == 'z') {
      digitalWrite(directionPin_z, direction_z);
      for (int i = 0 ; i < number_of_pulses; i++) {
        digitalWrite(outputPin_z, HIGH);  // Set the output pin HIGH
        delayMicroseconds(step_pulse_time);
        digitalWrite(outputPin_z, LOW);   // Set the output pin LOW
        delay(pulse_delay);
      }
      Serial.println("ok.");
    }

    
  }
}
