# Modul um die Histogramme zu erstellen

import data_handle as dh
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
import datetime
import time
from logger.logger import Logger

PATH = os.getcwd()

logger = Logger("Diagram Handle")


def get_x_minutes_ago(x: int) -> int:
    """Funktion zum Abrufen des UNIX-Timestamps für die angegebene Zeitspanne."""
    now = time.time()
    x_minutes_ago = now - (x * 60)
    return x_minutes_ago



class DiagramHandle:
    def __init__(self) -> None:
        logger.log("Starte Diagrammerstellung...")
        self.create_diagram()

    def create_diagram(self):
        # Daten abrufen
        data = dh.get_timed_data(get_x_minutes_ago(10))
        
        air_temp = data["air_temperatures"]
        air_hum = data["air_humidities"]
        ground_temp = data["ground_temperatures"]
        ground_hum = data["ground_humidities"]
        time = data["timestamps"]
        
        
        
        # Diagramm erstellen mit geteilter y-Achse
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False, figsize=(8, 6))
        
        # Tight Layout aktivieren
        plt.tight_layout(pad=3.0)

        # Erste Linie plotten (rote Linie) im oberen Subplot
        ax1.plot(time, air_temp, color='blue', label='Lufttemperatur')
        ax1.plot(time, ground_temp, color='blue', label='Bodentemperatur')  
        ax1.set_xlabel('Zeit')
        ax1.legend()
        ax1.set_title('Temperatur')

        # Zweite Linie plotten (blaue Linie) im unteren Subplot
        ax2.plot(time, air_hum, color='blue', label='Luftfeuchtigkeit')
        ax2.plot(time, ground_hum, color='blue', label='Bodenfeuchtigkeit')
        ax2.set_xlabel('Zeit')
        ax2.legend()
        ax2.set_title('Feuchtigkeit')

        # Diagramm anzeigen
        plt.show()


if __name__ == "__main__":
    DiagramHandle()
