#include <Adafruit_NeoPixel.h>

#include <DHT.h>

// Pin Belegung
const int health_led_pin = 12;
const int heartbeat_led_pin = 11;
const int error_led_pin = 10;
const int strip_pin = 6;
const int ground_temp_pin = 3;
const int ground_hum_pin = A3;

#define DHTPIN 2
#define DHTTYPE DHT22

// Temperatursensor
DHT air_sensor(DHTPIN, DHTTYPE);

// LED-Streifen
Adafruit_NeoPixel strip = Adafruit_NeoPixel(78, strip_pin, NEO_GRB + NEO_KHZ800);

void setup()
{
    // Pins initialisieren
    pinMode(health_led_pin, OUTPUT);
    pinMode(heartbeat_led_pin, OUTPUT);
    pinMode(strip_pin, OUTPUT);
    pinMode(ground_temp_pin, INPUT);
    pinMode(ground_hum_pin, INPUT);

    air_sensor.begin();

    // LED-Streifen initialisieren
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'


    Serial.begin(9600);
}

void loop()
{
    for (int i = 0; i < 78; i++)
    {
    
        strip.setPixelColor(i, 255, 0, 0);
        strip.setPixelColor(i-1, 0, 0, 0);
        strip.show();
        delay(100);

    }
    
}

void read_sensors(){
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


    Serial.print("Luftfeuchtigkeit: ");
    Serial.println(air_hum);
    Serial.print("Lufttemperatur: ");
    Serial.println(air_temp);
    Serial.println();

}

void pulse_health_led()
{
    // Health-LED blinken lassen
    digitalWrite(health_led_pin, HIGH);
    delay(100);
    digitalWrite(health_led_pin, LOW);
    delay(1900);
}