# Hauptprogramm für die Steuerung der Anlage
# Startet die unterprogramme als Threads

# Imports
import time
import multiprocessing

# Custom Modules
from logger.logger import Logger

# Multiprocessing Module
import receive_serial
import data_display

logger = Logger("Main")

def main():
    logger.log("Starte Hauptprogramm")
    
    processes = []    
    
    # Serielle Schnittstelle
    processes.append(multiprocessing.Process(target=receive_serial.main))
    
    # Datenanzeige
    processes.append(multiprocessing.Process(target=data_display.process_worker))
    
    # Prozesse starten
    for process in processes:
        process.start()
        
    # Abfrage zum beenden des Programms
    action = ""
    while action != "q":
        action = input("Drücke 'q' zum Beenden\n")
        if action == "q":
            logger.log("Beende Hauptprogramm")
            for process in processes:
                process.terminate()
                process.join()
            exit()
      
if __name__ == "__main__":
    main()
    