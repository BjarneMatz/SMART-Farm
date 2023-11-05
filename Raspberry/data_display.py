# Modul zum Anzeigen der Daten auf dem Display am Raspberry Pi, wird als Thread ausgeführt

# Imports
import tkinter as tk
from tkinter import ttk

# Custom Modules
from logger.logger import Logger
import data_handle as dh

logger = Logger("Data Display")

class DataDisplay:
    def __init__(self) -> None:
        logger.log("Starte Datenanzeige")
        self.root = tk.Tk()
        self.root.title("Datenanzeige")
        #self.root.attributes("-fullscreen", True)
        
        self.create_widgets()
        self.update_data()
        self.root.mainloop()
        
    def create_widgets(self) -> None:
        self.current_data_frame = ttk.Frame(self.root)
        self.current_data_frame.grid(row=0, column=0)
        
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.grid(row=0, column=1)

        self.air_temperature_label = ttk.Label(self.current_data_frame, text="Lufttemperatur: ")
        self.air_temperature_label.grid(row=0, column=0)
        
        self.air_temperature_data_label = ttk.Label(self.current_data_frame, text="0°C")
        self.air_temperature_data_label.grid(row=0, column=1)
        
        self.air_humidity_label = ttk.Label(self.current_data_frame, text="Luftfeuchtigkeit: ")
        self.air_humidity_label.grid(row=1, column=0)
        
        self.air_humidity_data_label = ttk.Label(self.current_data_frame, text="0%")
        self.air_humidity_data_label.grid(row=1, column=1)
        
        self.ground_temperature_label = ttk.Label(self.current_data_frame, text="Bodentemperatur: ")
        self.ground_temperature_label.grid(row=3, column=0)
        
        self.ground_temperature_data_label = ttk.Label(self.current_data_frame, text="0°C")
        self.ground_temperature_data_label.grid(row=3, column=1)
        
        self.ground_humidity_label = ttk.Label(self.current_data_frame, text="Bodenfeuchtigkeit: ")
        self.ground_humidity_label.grid(row=4, column=0)
        
        self.ground_humidity_data_label = ttk.Label(self.current_data_frame, text="0%")
        self.ground_humidity_data_label.grid(row=4, column=1)
        
    
    def update_data(self) -> None:
        logger.log("Aktualisiere Daten")
        data = dict(dh.get_latest_data())
        
        self.air_temperature_data_label.config(text=str(data["air_temperature"]) + "°C")
        self.air_humidity_data_label.config(text=str(data["air_humidity"]) + "%")
        self.ground_temperature_data_label.config(text=str(data["ground_temperature"]) + "°C")
        self.ground_humidity_data_label.config(text=str(data["ground_humidity"]) + "%")
        
        self.root.after(5000, self.update_data)
        
def process_worker() -> None:
    DataDisplay()

if __name__ == "__main__":
    DataDisplay()