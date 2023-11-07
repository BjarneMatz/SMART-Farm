# Modul um die Histogramme zu erstellen

# Externe Module
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time

# Eigene Module
from logger.logger import Logger

# Projektmodule
import data_handle as dh

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
        fig, (ax1, ax2) = plt.subplots(2, 1)
        
        # Tight Layout aktivieren
        plt.tight_layout(pad=3.0)

        # Temperatur plotten
        ax1.plot(time, air_temp, color='blue', label='Lufttemperatur')
        ax1_2 = ax1.twinx()
        ax1_2.plot(time, ground_temp, color='red', label='Bodentemperatur')  
        ax1.set_xlabel('Zeit')
        ax1.legend()
        ax1_2.legend()
        ax1.set_title('Temperatur')

        # Abstand zwischen den Labels der y-Achse anpassen
        ax1.yaxis.set_major_locator(mticker.MaxNLocator(8))
        ax1_2.yaxis.set_major_locator(mticker.MaxNLocator(8))
        

        # Feuchtigkeit plotten
        ax2.plot(time, air_hum, color='blue', label='Luftfeuchtigkeit')
        ax2_2 = ax2.twinx()
        ax2_2.plot(time, ground_hum, color='red', label='Bodenfeuchtigkeit')
        ax2.set_xlabel('Zeit')
        ax2.legend()
        ax2_2.legend()
        ax2.set_title('Feuchtigkeit')
        
        # Abstand zwischen den Labels der y-Achse anpassen
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(8))
        ax2_2.yaxis.set_major_locator(mticker.MaxNLocator(8))

        # Diagramm anzeigen (debug)
        #plt.show()
        
        # Diagramm speichern
        fig.savefig(os.path.join(PATH, "Raspberry", "diagram.png"))


if __name__ == "__main__":
    DiagramHandle()
