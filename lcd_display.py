import lcddriver
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

class DisplayManager:
    def __init__(self):
        self.lcd = lcddriver.lcd()

    def clear(self):
        self.lcd.clear()

    def cleanup(self):
        self.clear()

    def show_date_time(self):
        date_time = datetime.now()
        date_string = date_time.strftime(' %a %d/%m/%y S.%W')
        time_string = date_time.strftime('      %H:%M:%S')

        self.lcd.display_string("   Bienvenue chez", 1)
        self.lcd.display_string(" Votre Magasin", 2)
        self.lcd.display_string(date_string, 3)
        self.lcd.display_string(time_string, 4)

    def show_temp_humid(self, data):
        if data and all(key in data for key in ['temperature', 'humidity', 'pressure']):
            self.lcd.display_string(' Biotope du magasin', 1)
            self.lcd.display_string(f"  Temp.    {data['temperature']} *C", 2)
            self.lcd.display_string(f"  Humid.   {data['humidity']} %", 3)
            self.lcd.display_string(f"  Press.   {data['pressure']} hPa", 4)
        else:
            self.lcd.display_string("  Données manquantes", 2)

    def show_co2(self, data):
        if data and 'co2' in data:
            co2 = data['co2']
            self.lcd.display_string('    Taux de Co2    ', 1)
            self.lcd.display_string(' actuel en magasin', 2)
            self.lcd.display_string(f"   Co2: {co2} ppm", 3)

            if co2 < 250:
                self.lcd.display_string('   Qualite elevee', 4)  # Moins de 250 ppm
            elif 250 <= co2 < 350:
                self.lcd.display_string('   Qualite elevee', 4)  # 250 à 350 ppm
            elif 350 <= co2 < 1000:
                self.lcd.display_string('   Qualite moyenne', 4)  # 350 à 1000 ppm
            elif 1000 <= co2 < 2000:
                self.lcd.display_string('   Qualite moderee', 4)  # 1000 à 2000 ppm
            elif 2000 <= co2 < 5000:
                self.lcd.display_string('   Qualite mediocre', 4)  # 2000 à 5000 ppm
            else:
                self.lcd.display_string('   Qualite dangereuse', 4)  # 5000 ppm et plus

        else:
            self.lcd.display_string('Mesure en cours...', 2)
            self.lcd.display_string('Du taux de Co2...', 3)

    def show_air_quality(self, data):
        if data and all(key in data for key in ['pm10', 'pm25', 'pm100']):
            self.lcd.display_string("  Qualite de l'air", 1)
            self.lcd.display_string(f"PM 1.0: {data['pm10']} mic.g/m3", 2)
            self.lcd.display_string(f"PM 2.5: {data['pm25']} mic.g/m3", 3)
            self.lcd.display_string(f"PM 10: {data['pm100']} mic.g/m3", 4)
        else:
            self.lcd.display_string("  Données manquantes", 2)
