import datetime
import time
from sensors import SensorManager
from lcd_display import DisplayManager
from data_logger import DataLogger
from network import connect_to_wifi, synchronize_time, sync_rtc_with_system_time, update_system_time_from_rtc

# Intervalle de mise à jour de l'écran en secondes
LDC_MaJ = 7

class MainController:
    def __init__(self):
        self.sensors = SensorManager()
        self.display = DisplayManager()
        self.logger = DataLogger()

    def run(self):
        tasks = [
            self.display_and_log_all_data,
        ]
        
        for task in tasks:
            task()
    
    def display_and_log_all_data(self):
        # Récupération des données des capteurs
        temp_humid_data = self.sensors.read_temp_humid() or {}
        co2_data = self.sensors.read_co2() or {}
        air_quality_data = self.sensors.read_air_quality() or {}

        # Regroupement des données
        combined_data = {**temp_humid_data, **co2_data, **air_quality_data}
        combined_data['timestamp'] = datetime.datetime.now().isoformat()

        # Affichage des données
        self.display.clear()
        self.display.show_date_time()
        time.sleep(LDC_MaJ)		
		
        self.display.clear()
        self.display.show_temp_humid(temp_humid_data)
        time.sleep(LDC_MaJ)
        
        self.display.clear()
        self.display.show_co2(co2_data)
        time.sleep(LDC_MaJ)
        
        self.display.clear()
        self.display.show_air_quality(air_quality_data)
        time.sleep(LDC_MaJ)

        # Enregistrement dans InfluxDB
        if combined_data:
            self.logger.log_to_influxdb('environment_data', combined_data)

def initialize_network():
    connect_success = connect_to_wifi()

    if connect_success:
        synchronize_time()
        sync_rtc_with_system_time()
    else:
        print("Aucune connexion réseau. Tentative de mise à jour de l'heure depuis l'horloge RTC.")
        update_system_time_from_rtc()

if __name__ == "__main__":
    # Initialisation du réseau et synchronisation du temps
    initialize_network()
    
    # Initialisation du contrôleur principal
    controller = MainController()

    try:
        # Boucle principale
        while True:
            controller.run()
    except KeyboardInterrupt:
        # Nettoyage lors de l'interruption par l'utilisateur
        controller.display.cleanup()
