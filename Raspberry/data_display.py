# Modul zum Anzeigen der Daten auf dem Display am Raspberry Pi, wird als Thread ausgeführt

# Imports
import tkinter as tk
from tkinter import ttk

# Custom Modules
from logger.logger import Logger
import data_handle as dh
import os
from PIL import Image, ImageTk

PATH = os.getcwd()

logger = Logger("Data Display")

class DataDisplay:
    def __init__(self) -> None:
        logger.log("Starte Datenanzeige")
        self.root = tk.Tk()
        self.root.title("Datenanzeige")
        self.root.geometry("800x480")
        #self.root.attributes("-fullscreen", True)
        
        # Schriftart und -größe für alle Widgets
        self.style = ttk.Style()
        self.style.configure(".", font=("Arial", 12))
        
        # Style für die Labels
        
        self.create_widgets()
        self.update_data()
        self.root.mainloop()
        
    def create_widgets(self) -> None:
        self.create_current_data_frame()
        self.create_diagram_frame()
        self.copyrigth_label = ttk.Label(self.root, text="© 2023 Donnjer Development / Bjarne Matz", font=("Arial", 8))
        self.copyrigth_label.grid(row=1, column=0, columnspan=2, sticky="SEW")
    
    def create_diagram_frame(self) -> None:
        self.diagram_frame = ttk.Frame(self.root)
        self.diagram_frame.grid(row=0, column=0, sticky="NW", padx=(0, 20))
        
        # Diagramm Bild laden und anpassen
        diagram_image = Image.open(os.path.join(PATH, "Raspberry", "diagram.png"))
        
        original_width, original_height = diagram_image.size
        
        # Bild auf die Größe des Displays anpassen, ohne das Seitenverhältnis zu verändern
        resized_image = diagram_image.resize((int(original_width * 0.9), int(original_height * 0.9)))
        self.diagram_image = ImageTk.PhotoImage(resized_image)
        
        # Bild anzeigen
        self.diagram_image_label = ttk.Label(self.diagram_frame, image=self.diagram_image)
        self.diagram_image_label.grid(row=0, column=0, sticky="NSEW")
        
        
        
    def create_current_data_frame(self) -> None:        
        self.current_data_frame = ttk.Frame(self.root)
        self.current_data_frame.grid(row=0, column=1, sticky="NSEW")
        
        self.current_data_label = ttk.Label(self.current_data_frame, text="Aktuelle Daten", font=("Arial", 16))
        self.current_data_label.grid(row=0, column=0, sticky="NSEW")
        
        # Child Frame für Temperatur und Luftfeuchtigkeit
        self.temperature_frame = ttk.Frame(self.current_data_frame)
        self.temperature_frame.grid(row=1, column=0, sticky="NSEW")
        
        self.humidity_frame = ttk.Frame(self.current_data_frame)
        self.humidity_frame.grid(row=2, column=0, sticky="NSEW")

        # Icon und Labels für Temperatur
        self.temperature_icon = tk.PhotoImage(file=os.path.join(PATH, "Raspberry", "icons", "temperature.png"))
        self.temperature_icon_label = ttk.Label(self.temperature_frame, image=self.temperature_icon)
        self.temperature_icon_label.grid(row=0, column=0, sticky="NSEW", rowspan=2)

        self.air_temperature_label = ttk.Label(self.temperature_frame, text="Luft: ")
        self.air_temperature_label.grid(row=0, column=1, sticky="W")
        
        self.air_temperature_data_label = ttk.Label(self.temperature_frame, text="0°C")
        self.air_temperature_data_label.grid(row=0, column=2, sticky="W")
        
        self.ground_temperature_label = ttk.Label(self.temperature_frame, text="Boden: ")
        self.ground_temperature_label.grid(row=1, column=1, sticky="W")
        
        self.ground_temperature_data_label = ttk.Label(self.temperature_frame, text="0°C")
        self.ground_temperature_data_label.grid(row=1, column=2, sticky="W")
        
        # Icon und Labels für Luftfeuchtigkeit
        self.humidity_icon = tk.PhotoImage(file=os.path.join(PATH, "Raspberry", "icons", "humidity.png"))
        self.humidity_icon_label = ttk.Label(self.humidity_frame, image=self.humidity_icon)
        self.humidity_icon_label.grid(row=0, column=0, sticky="NSEW", rowspan=2)
        
        self.air_humidity_label = ttk.Label(self.humidity_frame, text="Luft: ")
        self.air_humidity_label.grid(row=0, column=1, sticky="W")
        
        self.air_humidity_data_label = ttk.Label(self.humidity_frame, text="0%")
        self.air_humidity_data_label.grid(row=0, column=2, sticky="W")
        
        self.ground_humidity_label = ttk.Label(self.humidity_frame, text="Boden: ")
        self.ground_humidity_label.grid(row=1, column=1, sticky="W")
        
        self.ground_humidity_data_label = ttk.Label(self.humidity_frame, text="0%")
        self.ground_humidity_data_label.grid(row=1, column=2, sticky="W")
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