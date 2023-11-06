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

class DiagramHandle:
    def __init__(self) -> None:
        logger.log("Starte Diagramm Erstellung")
        self.create_diagram()
        
    def create_diagram(self) -> None:
        # Daten aus der Datenbank holen
        temperature, air_humidity, ground_temperature, ground_humidity, time = dh.get_all_data()
        
        # Zeit in Datetime Objekte umwandeln
        time = [datetime.datetime.fromtimestamp(ts) for ts in time]
        
        # Plot erstellen
        fig, ax = plt.subplots(3, 1, sharex=True)
        fig.tight_layout(pad=3)
        plt.autoscale(enable=True, axis="x", tight=True)
        
        # Temperatur Plot
        ax[0].plot(time, temperature, color="red")
        ax[0].set_title("Lufttemperatur [°C]")
        ax[0].set_ylim([0, 50])
        ax[0].grid(True)        
        
        # Luftfeuchtigkeit Plot
        ax[1].plot(time, air_humidity, color="blue")
        ax[1].set_title("Luftfeuchtigkeit [%]")
        ax[1].set_ylim([0, 100])
        ax[1].grid(True)
        
        ax[2].plot(time, ground_humidity, color="green")
        ax[2].set_title("Bodenfeuchtigkeit [%]")
        ax[2].set_ylim([0, 100])
        ax[1].grid(True)
        
        
        # X-Achse formatieren
        ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%D:%H:%M"))
        ax[1].xaxis.set_major_locator(mticker.MaxNLocator(10))
        fig.autofmt_xdate()
        
        # Diagramm speichern
        fig.savefig(os.path.join(PATH, "Raspberry", "diagram.png"))
        
        # Diagramm schließen
        plt.close(fig)
        
        # Diagramm anzeigen (debugging)
        #plt.show()
        
        logger.log("Diagramm erstellt")
        
if __name__ == "__main__":
    DiagramHandle()