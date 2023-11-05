# Modul zum Empfangen von Daten über die serielle Schnittstelle, wird als Thread ausgeführt

# Imports
import serial
import time

# Custom Modules
from logger.logger import Logger
from database.database import Database

sensor_data_db = Database("sensor_data")
logger = Logger("Serial")


def send_to_db(data: list) -> None:
    # Datenformat: 
    
    logger.log("Sende Daten an Datenbank")
    
    timestamp = time.time()
    
    db_data = {
        "sensor_id": data[0],
        "sensor_value": data[1],
        "timestamp": timestamp
    }
    
    sensor_data_db.set_value(timestamp, db_data)


def main() -> None:
    logger.log("Starte serielle Schnittstelle")
    # Serielle Schnittstelle öffnen
    ser = serial.Serial('COM1', 1200, timeout=1)
    ser.flush()
    
    # Daten empfangen und bei Empfang an weitergeben
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            logger.log("Received: " + line)
            data = line.split(",")
            send_to_db(data)   

