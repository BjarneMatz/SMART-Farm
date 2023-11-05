// Externe Bibliotheken
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_NeoPixel.h>
#include <DHT.h>

// Pin Belegung
const int pump_pin = 2;
const int pump_led_pin = 22;

const int strip_pin = 4;

const int air_sensor_pin = 5;
const int ground_temp_sensor_pin = 3;
const int ground_hum_sensor_pin = A3;

// Status LEDs
const int health_led_pin = 23;
const int heartbeat_led_pin = 24;
const int error_led_pin = 25;
const int messure_led_pin = 26;

// Luftfeuchtigkeit und -temperatur Sensor
DHT air_sensor(air_sensor_pin, DHT22);

//Bodentemperatur Sensor
OneWire ground_temp_sensor(ground_temp_sensor_pin);
DallasTemperature ground_temp_sensors(&ground_temp_sensor);

// LED-Streifen
Adafruit_NeoPixel strip = Adafruit_NeoPixel(78, strip_pin, NEO_GRB + NEO_KHZ800);

void setup()
{
    //Status LEDs initialisieren
    pinMode(health_led_pin, OUTPUT);
    pinMode(heartbeat_led_pin, OUTPUT);
    pinMode(error_led_pin, OUTPUT);
    pinMode(messure_led_pin, OUTPUT);
    pinMode(pump_led_pin, OUTPUT);

    digitalWrite(health_led_pin, HIGH);
    digitalWrite(heartbeat_led_pin, HIGH);
    digitalWrite(error_led_pin, HIGH);
    digitalWrite(messure_led_pin, HIGH);
    digitalWrite(pump_led_pin, HIGH);
    
    // Sensoren initialisieren
    air_sensor.begin();
    ground_temp_sensors.begin();
    pinMode(ground_hum_sensor_pin, INPUT);

    //Aktoren initialisieren
    pinMode(pump_pin, OUTPUT);
    digitalWrite(pump_pin, LOW);
    
    // LED-Streifen initialisieren
    strip.begin();
    strip.show(); // Alle Pixel ausschalten
    strip.setBrightness(255);

    // Serielle Schnittstelle initialisieren
    Serial.begin(9600);
    Serial.println("Starte System...");
    delay(5000); // Auf Verbindung warten

    // Status LEDs in Betribszustand setzen
    digitalWrite(heartbeat_led_pin, LOW);
    digitalWrite(error_led_pin, LOW);
    digitalWrite(messure_led_pin, LOW);
    digitalWrite(pump_led_pin, LOW);
}

void loop()
{
    strip.fill(strip.Color(255, 255, 255), 0, 78);
    strip.show();
    read_sensors();
    heartbeat();
}

void read_sensors(){
    digitalWrite(messure_led_pin, HIGH);
    // Luftfeuchtigkeit
    float air_hum = air_sensor.readHumidity();
    // Lufttemperatur
    float air_temp = air_sensor.readTemperature();

    if (isnan(air_hum) || isnan(air_temp)) {
        digitalWrite(error_led_pin, HIGH);
        return;
    } else {
        digitalWrite(error_led_pin, LOW);
    }

    float ground_temp = air_temp - 1;
    float ground_hum = analogRead(ground_hum_sensor_pin);
    // Datenformat: "Luftfeuchtigkeit,Lufttemperatur,Bodentemperatur,Bodenfeuchtigkeit"
    Serial.println(String(air_hum) + "," + String(air_temp) + "," + String(ground_temp) + "," + String(ground_hum));
    digitalWrite(messure_led_pin, LOW);
}

void toggle_pump(bool state)
{
    digitalWrite(pump_pin, state);
    digitalWrite(pump_led_pin, state);
}

void heartbeat()
{
    // Health-LED blinken lassen
    digitalWrite(heartbeat_led_pin, HIGH);
    delay(100);
    digitalWrite(heartbeat_led_pin, LOW);
    delay(1900);
}