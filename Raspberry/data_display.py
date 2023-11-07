# Externe Module
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

# Eigene Module
from logger.logger import Logger

# Projektmodule
import data_handle as dh

PATH = os.getcwd()
logger = Logger("Data Display")

class DataDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Datenanzeige")
        self.root.geometry("800x480")
        #self.root.attributes("-fullscreen", True)
        
        # Schriftart und -größe für alle Widgets
        self.style = ttk.Style()
        self.style.configure(".", font=("Arial", 30))
        
        self.create_widgets()
        self.update_data()
        self.root.mainloop()
        
    def create_widgets(self):        
        self.data_frame = ttk.Frame(self.root)
        self.data_frame.pack(expand=True, anchor="center")
        
        self.temp_frame = ttk.Frame(self.data_frame)
        self.temp_frame.grid(row=0, column=0, sticky="NSEW", padx=20, pady=20)
        
        self.hum_frame = ttk.Frame(self.data_frame)
        self.hum_frame.grid(row=1, column=0, sticky="NSEW", padx=20, pady=20)
        
        #Label am unteren Rand in der Mitte
        self.copyrigth_label = ttk.Label(self.root, text="© 2023 Donnjer Development / Bjarne Matz", font=("Arial", 8))
        self.copyrigth_label.pack(side="bottom", anchor="center")
        
        
        # Temperatur
        self.air_temp_label = ttk.Label(self.temp_frame, text="Lufttemperatur:")
        self.air_temp_label.grid(row=0, column=1, sticky="W")
        self.air_temp_value_label = ttk.Label(self.temp_frame, text="0°C")
        self.air_temp_value_label.grid(row=0, column=2, sticky="W")
        
        self.ground_temp_label = ttk.Label(self.temp_frame, text="Bodentemperatur:")
        self.ground_temp_label.grid(row=1, column=1, sticky="W")
        self.ground_temp_value_label = ttk.Label(self.temp_frame, text="0°C")
        self.ground_temp_value_label.grid(row=1, column=2, sticky="W")
        
        # Icon und Labels für Temperatur
        self.temperature_icon = tk.PhotoImage(file=os.path.join(PATH, "Raspberry", "icons", "temperature.png"))
        self.temperature_icon_label = ttk.Label(self.temp_frame, image=self.temperature_icon)
        self.temperature_icon_label.grid(row=0, column=0, sticky="NSEW", rowspan=2, padx=(0, 20))
        
        
        # Feuchtigkeit
        self.air_hum_label = ttk.Label(self.hum_frame, text="Luftfeuchtigkeit:")
        self.air_hum_label.grid(row=0, column=1, sticky="W")
        self.air_hum_value_label = ttk.Label(self.hum_frame, text="0%")
        self.air_hum_value_label.grid(row=0, column=2, sticky="W")
        
        self.ground_hum_label = ttk.Label(self.hum_frame, text="Bodenfeuchtigkeit:")
        self.ground_hum_label.grid(row=1, column=1, sticky="W")
        self.ground_hum_value_label = ttk.Label(self.hum_frame, text="0%")
        self.ground_hum_value_label.grid(row=1, column=2, sticky="W")
        
        # Feuchtigkeit Icon
        self.humidity_icon = tk.PhotoImage(file=os.path.join(PATH, "Raspberry", "icons", "humidity.png"))
        self.humidity_icon_label = ttk.Label(self.hum_frame, image=self.humidity_icon)
        self.humidity_icon_label.grid(row=0, column=0, sticky="NSEW", rowspan=2, padx=(0, 20))
        
        
    def update_data(self):
        data = dh.get_latest_data()
        
        self.air_temp_value_label.config(text=f"{data['air_temperature']}°C")
        self.air_hum_value_label.config(text=f"{data['air_humidity']}%")
        self.ground_temp_value_label.config(text=f"{data['ground_temperature']}°C")
        self.ground_hum_value_label.config(text=f"{data['ground_humidity']}%")
        
        self.root.after(1000, self.update_data)
        
def process_worker():
    DataDisplay()        

if __name__ == "__main__":
    DataDisplay()