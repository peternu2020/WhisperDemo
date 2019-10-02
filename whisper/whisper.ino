#include <ESP8266WiFi.h>

// Network Credentials
const char* ssid = "Device-Northwestern";


int status = WL_IDLE_STATUS;
IPAddress server(129,105,10,218); 

// Define the Pin Numbers
#define TRIGGER_PIN 5
#define ECHO_PIN 4

WiFiClient client;

void setup() {
 Serial.begin(115200); Serial.println();
 pinMode(TRIGGER_PIN, OUTPUT); // Set trigger pin as output
 pinMode(ECHO_PIN, INPUT); // Set echo pin as input
 // pinMode(BUILTIN_LED, OUTPUT);

 wifiConnect();
}

void loop() {
  long duration, distance;

  // Clear the trigger pin
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);

  // Sets the trigger pin on high for 10 microseconds
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  // Reads the trigger pin and returns the sound wave travel time in microseconds
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = (duration/2) / 29.1; // Speed of sound in air is 29.1 microseconds per centimeter
  String payload = "{ \"d\" : {\"distance\":";
  payload += distance;
  payload += "}}";
  Serial.println(payload);
    // if you get a connection, report back via serial:
  if (client.connect(server, 65432)) {
    Serial.println("connected");
    // Make a HTTP request:
    client.println(payload);
  }
  delay(100);
}

void wifiConnect() {
 Serial.print("Connecting to "); Serial.print(ssid);
 WiFi.begin(ssid);
 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.println(".");
 }
 Serial.print("WiFi connected, IP address: "); Serial.println(WiFi.localIP());
}
