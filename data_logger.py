import configparser
import datetime
from influxdb import InfluxDBClient

class DataLogger:
    def __init__(self):
        # Lecture des paramètres depuis config.ini
        config = configparser.ConfigParser()
        config_file_path = '/home/pi/Desktop/main/config.ini'

        config.read(config_file_path)

        influx_host = config['INFLUXDB']['HOST']
        influx_port = int(config['INFLUXDB']['PORT'])
        influx_db = config['INFLUXDB']['DATABASE']

        retention_policy_name = config['INFLUXDB']['RETENTION_POLICY_NAME']
        retention_policy_duration = config['INFLUXDB']['RETENTION_POLICY_DURATION']
        retention_policy_replication = config['INFLUXDB']['RETENTION_POLICY_REPLICATION']

        try:
            self.client = InfluxDBClient(host=influx_host, port=influx_port)
            self.client.switch_database(influx_db)
            self.influxdb_installed = True

            # Création ou mise à jour de la Retention Policy en fonction du fichier config.ini
            self.client.query(f"""
                CREATE RETENTION POLICY "{retention_policy_name}" ON "{influx_db}" 
                DURATION {retention_policy_duration} 
                REPLICATION {retention_policy_replication} 
                DEFAULT
            """)

        except Exception as e:
            print(f"Erreur lors de la connexion à InfluxDB : {e}")
            self.influxdb_installed = False

    def log_to_influxdb(self, measurement, fields):
        if not self.influxdb_installed:
            print("InfluxDB non installé ou non connecté. Impossible de journaliser les données.")
            return

        # Liste des champs obligatoires
        required_fields = ['co2', 'humidity', 'pm10', 'pm25', 'pm100', 'pressure', 'temperature']

        # Vérifier si des champs manquent ou si des valeurs sont None
        missing_fields = [field for field in required_fields if field not in fields or fields[field] is None]
        if missing_fields:
            current_time = datetime.datetime.now().strftime("%d/%m/%y - %H:%M:%S")
            print(f"[{current_time}] Champs manquants ou données nulles détectés : {missing_fields}. Le point ne sera pas enregistré.")
            return

        # Si toutes les données sont présentes, procéder à l'enregistrement
        json_body = [
            {
                "measurement": measurement,
                "fields": fields,
                "time": fields.pop('timestamp')  # Utilisation du timestamp pour l'heure du point
            }
        ]
		
        # Les données seront écrites avec la Retention Policy par défaut (définie dans config.ini)
        try:
            self.client.write_points(json_body)
            #print(f"Point ajouté à InfluxDB : {json_body}")
        except Exception as e:
            print(f"Erreur lors de l'écriture dans InfluxDB : {e}")
