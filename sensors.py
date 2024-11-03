import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_scd4x
from adafruit_pm25.i2c import PM25_I2C
import time

class SensorManager:
    def __init__(self):
        self.i2c = board.I2C()
        self.init_sensors()

    def init_sensors(self):
        try:
            # Correct initialization for BME280 using the 'basic' module
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)
        except Exception as e:
            print(f"Erreur lors de l'initialisation du BME280 : {e}")
            self.bme280 = None

        try:
            self.scd4x = adafruit_scd4x.SCD4X(self.i2c)
            self.scd4x.start_periodic_measurement()
        except Exception as e:
            print(f"Erreur lors de l'initialisation du SCD4x : {e}")
            self.scd4x = None

        try:
            reset_pin = None
            self.pm25 = PM25_I2C(busio.I2C(board.SCL, board.SDA, frequency=100000), reset_pin)
        except Exception as e:
            print(f"Erreur lors de l'initialisation du PMSA003I : {e}")
            self.pm25 = None

    def read_temp_humid(self):
        if self.bme280:
            return {
                'temperature': round(self.bme280.temperature, 1),
                'humidity': round(self.bme280.humidity, 1),
                'pressure': round(self.bme280.pressure, 1)
            }
        return None

    def read_co2(self):
        if self.scd4x and self.scd4x.data_ready:
            return {'co2': self.scd4x.CO2}
        return None

    def read_air_quality(self, max_attempts=3):
        if self.pm25:
            attempts = 0
            while attempts < max_attempts:
                try:
                    # Lecture des données du capteur PM2.5
                    aqdata = self.pm25.read()
                    return {
                        'pm10': aqdata["pm10 standard"],
                        'pm25': aqdata["pm25 standard"],
                        'pm100': aqdata["pm100 standard"]
                    }
                except RuntimeError as e:
                    print(f"Erreur lors de la lecture du PMSA003I : {e}. Nouvelle tentative...")
                    attempts += 1
                    time.sleep(1)  # Petite pause avant une nouvelle tentative
            print("Echec de la lecture du capteur PM2.5 après plusieurs tentatives.")
            return None
        return None
