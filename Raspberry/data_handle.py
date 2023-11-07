# Externe Module
import time

# Eigene Module
from logger.logger import Logger
from database.database import Database

logger = Logger("Data Handle")
db = Database("sensor_data")

def get_latest_data() -> dict:
    """Holt die aktuellsten Daten aus der Datenbank."""
    try:
        key = db.get_keys()[-1]
        data = dict(db.get_value(key))
    except:
        data = {
            "air_humidity": 0,
            "air_temperature": 0,
            "ground_temperature": 0,
            "ground_humidity": 0,
            "timestamp": 0
        }
    return data

def get_timed_data(start:int) -> dict:
    """Funktion zum Abrufen von Daten aus der Datenbank, die nach einem bestimmten Zeitpunkt aufgenommen wurden."""
    now = time.time()
    
    timestamps = []
    air_temperatures = []
    air_humidities = []
    ground_temperatures = []
    ground_humidities = []
    
    keys = db.get_keys()
    
    for key in keys:
        if float(key) >= start and float(key) <= now:
            data = dict(db.get_value(key))
            
            ground_hum = map_range(data["ground_humidity"], 0, 1023, 0, 100)
            air_hum = data["air_humidity"]
            ground_temp = data["ground_temperature"]
            air_temp = data["air_temperature"]
            timestamp = convert_timestamp(data["timestamp"])
            
            ground_humidities.append(ground_hum)
            air_humidities.append(air_hum)
            ground_temperatures.append(ground_temp)
            air_temperatures.append(air_temp)
            timestamps.append(timestamp)       
            
    # Ausgabeformat
    data = {
        "timestamps": timestamps,
        "air_temperatures": air_temperatures,
        "air_humidities": air_humidities,
        "ground_temperatures": ground_temperatures,
        "ground_humidities": ground_humidities
    }
    
    return data
    
def convert_timestamp(timestamp: int) -> str:
    """Konvertiert den UNIX-Timestamp in eine Stunden- und Minutenangabe."""
    timestamp = int(timestamp)
    timestamp = time.localtime(timestamp)
    timestamp = time.strftime("%H:%M", timestamp)
    return timestamp

def map_range(x, in_min, in_max, out_min, out_max):
  return (float(x) - float(in_min)) * (float(out_max) - float(out_min)) // (float(in_max) - float(in_min)) + float(out_min)

def write_data(data: list) -> None:
    # Datenformat: "Luftfeuchtigkeit,Lufttemperatur,Bodentemperatur,Bodenfeuchtigkeit"   
    timestamp = time.time()
    
    db_data = {
        "air_humidity": data[0],
        "air_temperature": data[1],
        "ground_temperature": data[2],
        "ground_humidity": data[3],
        "timestamp": timestamp
    }
    try:
        db.set_value(timestamp, db_data)
    except:
        logger.log("Fehler beim Schreiben der Daten in die Datenbank!", 2)