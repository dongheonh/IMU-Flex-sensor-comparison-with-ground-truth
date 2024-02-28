#include <Wire.h> // Wire library for I2C communication
#include <Adafruit_Sensor.h> // Adafruit Unified Sensor Driver
#include <Adafruit_BNO055.h> // Adafruit BNO055 library

Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28); // Sensor instance 1

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  Wire.begin(); // Initialize the I2C communication
  
  if(!bno1.begin()) {
    Serial.println("No BNO055 detected");
    while(1);
  }
}

void loop() {
  sensors_event_t event;
  bno1.getEvent(&event); // Get the orientation data
  // Read accelerometer data
  imu::Vector<3> accel = bno1.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  
  // Calculate the magnitude of the accelerometer vector
  float magnitude = sqrt(accel.x() * accel.x() + accel.y() * accel.y() + accel.z() * accel.z());

  int valueA0 = analogRead(A0);
  
  // Print orientation data (This might be commented out or removed if not needed)
  Serial.print(event.orientation.x, 3);
  Serial.print(", ");
  Serial.print(event.orientation.y, 3);
  Serial.print(", ");
  Serial.print(event.orientation.z, 3);
  Serial.print(",");
  
  Serial.print(valueA0); // Print the analog reading
  Serial.print(", ");
  Serial.println(magnitude, 3); // Print magnitude with 3 decimal places

  delay(200); // Short delay for continuous reading
}