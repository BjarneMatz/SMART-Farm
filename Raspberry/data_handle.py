from database.database import Database
import time
import diagram_handle
db = Database("sensor_data")

def get_latest_data() -> dict:
    try:
        key = get_latest_entry_key()
        data = dict(db.get_value(key))
        return data
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
    keys = db.get_keys()
    
    timestamps = []
    air_temperatures = []
    air_humidities = []
    ground_temperatures = []
    ground_humidities = []
    
    for key in keys:
        if float(key) >= start and float(key) <= now:
            data = dict(db.get_value(key))
            timestamps.append(convert_timestamp(data["timestamp"]))
            air_temperatures.append(data["air_temperature"])
            air_humidities.append(data["air_humidity"])
            ground_temperatures.append(data["ground_temperature"])
            ground_humidities.append(map_range(data["ground_humidity"], 0, 1023, 0, 100))
            
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

def get_latest_entry_key():
    data = dict(db.get_raw())
    latest_entry = data.keys()
    latest_entry = list(latest_entry)[-1]
    return latest_entry

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
    
    db.set_value(timestamp, db_data)
    
def build_diagram() -> None:
    diagram_handle.DiagramHandle()