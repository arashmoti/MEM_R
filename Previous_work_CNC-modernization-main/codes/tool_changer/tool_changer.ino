#define PWM1 9
#define AIN1 10
#define AIN2 11

int motor_speed;
bool motor_direction;
bool tool_change = false;
int incomingNumber;
unsigned long startTime;
bool cw = false;
bool ccw = false;
int Tool = 1;

void setup() {
  Serial.begin(9600);
  pinMode(PWM1, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  motor_speed = 255;
  motor_direction = false;

}

void loop() {
  if (Serial.available() > 0) {
    incomingNumber = Serial.parseInt();
    incomingNumber = ((incomingNumber - Tool) % 6 + 6) % 6;
    // Serial.println(incomingNumber);
    if (incomingNumber && tool_change == false) {
      tool_change = true;
      cw = true;
      ccw = false;
      motor_direction = true;
      startTime = millis();
    }
  }
  if (millis() - startTime >= 2000 && tool_change && cw) {
    cw = false;
    ccw = true;
    motor_direction = false;
    startTime = millis();
  }
  if (millis() - startTime >= 500 && tool_change && ccw) {
    cw = true;
    ccw = false;
    motor_direction = true;
    incomingNumber -= 1;
    Tool = (Tool + 1) % 6;
    Serial.print("Tool Number:");
    Serial.println(Tool);
    if (incomingNumber == 0) {
      tool_change = false;
      motor_direction = false;
      cw = false;
      ccw = false;
    } else {
      startTime = millis();
    }
  }

  if (motor_direction) {
    digitalWrite(AIN1, HIGH); //Motor A Rotate Clockwise
    digitalWrite(AIN2, LOW);
  }
  else {
    digitalWrite(AIN1, LOW); //Motor A Rotate CounterClockwise
    digitalWrite(AIN2, HIGH);
  }

  analogWrite(PWM1, motor_speed); //Speed control of Motor A

}
