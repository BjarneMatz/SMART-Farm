from database.database import Database
from time import time
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

def get_all_data() -> dict:
    keys = db.get_keys()
    
    timestamps = []
    air_temperatures = []
    air_humidities = []
    ground_temperatures = []
    ground_humidities = []
    
    for key in keys:
        air_temperatures.append(db.get_value(key)["air_temperature"])
        air_humidities.append(db.get_value(key)["air_humidity"])
        ground_temperatures.append(db.get_value(key)["ground_temperature"])
        ground_humidities.append(db.get_value(key)["ground_humidity"])
        timestamps.append(db.get_value(key)["timestamp"])
        
    return air_temperatures, air_humidities, ground_temperatures, ground_humidities, timestamps

def get_latest_entry_key():
    data = dict(db.get_raw())
    latest_entry = data.keys()
    latest_entry = list(latest_entry)[-1]
    return latest_entry

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def write_data(data: list) -> None:
    # Datenformat: "Luftfeuchtigkeit,Lufttemperatur,Bodentemperatur,Bodenfeuchtigkeit"   
    timestamp = time()
    humidity = data[3]
    humidity = map_range(float(humidity), 0, 1023, 0, 100)
    
    db_data = {
        "air_humidity": data[0],
        "air_temperature": data[1],
        "ground_temperature": data[2],
        "ground_humidity": humidity,
        "timestamp": timestamp
    }
    
    db.set_value(timestamp, db_data)
    