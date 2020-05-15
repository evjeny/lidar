#include <Servo.h>

#define PIN_SERVO 2
#define PIN_TRIG 4
#define PIN_ECHO 5

#define num_states 180

Servo rotator;
long duration;
long location[num_states];

void setup() {
  Serial.begin (9600);
  rotator.attach(PIN_SERVO);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
}

long get_cm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(5);
  
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  
  digitalWrite(PIN_TRIG, LOW);
  
  duration = pulseIn(PIN_ECHO, HIGH);
  return (duration / 2) / 29.1;
}

void rotate(int deg) {
  rotator.write(deg);
}

void loop() {
  int command = 0;
  if(Serial.available() > 0) {
    command = Serial.read();
  }

  if(command == 0) {
    return;
  } else if(command == 'e') {
    rotate(num_states / 2);
  } else if(command == 's') {
    for(int pos = 0; pos < num_states; pos++) {
      rotate(pos);
      delay(15);
  
      location[pos] = get_cm();
    }
    for(int pos = num_states-1; pos >= 0; pos--) {
      rotate(pos);
      delay(15);
  
      location[pos] = (location[pos] + get_cm()) / 2;
    }
    
    for(int pos = 0; pos < num_states; pos++) {
      Serial.print(location[pos]);
      if(pos != num_states-1) {
        Serial.print(",");
      } else {
        Serial.println();
      }
    }
  }
  delay(100);
}
