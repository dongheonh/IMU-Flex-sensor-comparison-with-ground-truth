// Include necessary libraries for I2C communication and sensor interfacing
#include <Wire.h> // Wire library for I2C communication
#include <Adafruit_Sensor.h> // Adafruit Unified Sensor Driver
#include <Adafruit_BNO055.h> // Adafruit BNO055 library

// Define the I2C address for the TCA9548A multiplexer
#define TCAADDR 0x70

// Create instances of the BNO055 sensor, all with the same I2C address
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28); // Sensor instance 1
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28); // Sensor instance 2
Adafruit_BNO055 bno3 = Adafruit_BNO055(55, 0x28); // Sensor instance 3

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  Wire.begin(); // Initialize the I2C communication
  
  // BNO detection
  initializeSensor(bno1, 0); // Initialize the first sensor
  initializeSensor(bno2, 1); // Initialize the second sensor
  initializeSensor(bno3, 2); // Initialize the third sensor
}

void loop() {
    sensors_event_t event;

    // Read Flex sensor's voltage
    // Read analog values from pins A0, A1, and A2
    int valueA0 = analogRead(A0);
    int valueA1 = analogRead(A1);
    int valueA2 = analogRead(A2);

    // THIS CODE ONLY READ THE YAW ORIENTATIONS
    tcaselect(0); // Select the first BNO055 sensor
    bno1.getEvent(&event); // Get the orientation data
    Serial.print(event.orientation.x, 3);
    Serial.print(", ");

    tcaselect(1); // Repeat for the second BNO055 sensor
    bno2.getEvent(&event);
    Serial.print(event.orientation.x, 3);
    Serial.print(", ");

    tcaselect(2); // Repeat for the third BNO055 sensor
    bno3.getEvent(&event);
    Serial.print(event.orientation.x, 3);
    Serial.print(",");

    // Print analog input values in CSV format (values from the flex sensors)
    Serial.print(valueA0);
    Serial.print(",");
    Serial.print(valueA1);
    Serial.print(",");
    Serial.println(valueA2); // 'println' adds a new line after printing valueA2
    delay(200); // Delay for 3 seconds before the next reading
}

// I2C 
void tcaselect(uint8_t i) {
  if (i > 7) return; // If channel number is out of range, do nothing
  Wire.beginTransmission(TCAADDR); // Begin I2C transmission to the TCA9548A
  Wire.write(1 << i); // Select the appropriate channel (0 to 7)
  Wire.endTransmission(); // End the I2C transmission
}

void initializeSensor(Adafruit_BNO055& bno, uint8_t channel) {
  tcaselect(channel); // Select the appropriate channel on the multiplexer
  if (!bno.begin()) { // Begin communication with the BNO055 sensor
    Serial.println("Failed to initialize BNO055 on channel " + String(channel)); // Print error message if initialization fails
    while (1); // Infinite loop to halt further execution
  }
  
  delay(10); // Wait for a short time after initialization
  bno.setExtCrystalUse(true); // Use the external crystal for more accuracy
}