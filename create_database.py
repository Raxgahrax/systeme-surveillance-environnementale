import configparser
import requests

# Chemin vers le fichier de configuration
CONFIG_FILE = "/home/pi/Desktop/main/config.ini"

# Lire le fichier de configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Fonction pour obtenir la valeur d'une section et d'une clé
def get_config_value(section, key):
    try:
        return config[section][key]
    except KeyError:
        return None

# Configuration InfluxDB (base de données principale)
INFLUXDB_HOST = get_config_value("INFLUXDB", "HOST")
INFLUXDB_PORT = get_config_value("INFLUXDB", "PORT")
DATABASE = get_config_value("INFLUXDB", "DATABASE")
RETENTION_POLICY_NAME = get_config_value("INFLUXDB", "RETENTION_POLICY_NAME")
RETENTION_POLICY_DURATION = get_config_value("INFLUXDB", "RETENTION_POLICY_DURATION")
RETENTION_POLICY_REPLICATION = get_config_value("INFLUXDB", "RETENTION_POLICY_REPLICATION")

# Fonction pour vérifier et créer une base de données si nécessaire
def create_database_if_not_exists(host, port, database_name):
    print(f"Vérification de l'existence de la base de données '{database_name}' sur {host}:{port}...")
    
    # Vérifier si la base de données existe
    response = requests.get(f"http://{host}:{port}/query", params={'q': 'SHOW DATABASES'})
    if response.status_code == 200:
        if database_name not in response.text:
            print(f"La base de données '{database_name}' n'existe pas. Création en cours...")
            requests.post(f"http://{host}:{port}/query", params={'q': f"CREATE DATABASE {database_name}"})
            print(f"Base de données '{database_name}' créée avec succès.")
        else:
            print(f"La base de données '{database_name}' existe déjà.")
    else:
        print(f"Erreur lors de la vérification de la base de données : {response.status_code}")

# Fonction pour créer la politique de rétention si nécessaire
def create_retention_policy():
    print(f"Création de la politique de rétention '{RETENTION_POLICY_NAME}' pour la base de données '{DATABASE}' sur {INFLUXDB_HOST}:{INFLUXDB_PORT}...")
    
    query = f"CREATE RETENTION POLICY \"{RETENTION_POLICY_NAME}\" ON \"{DATABASE}\" DURATION {RETENTION_POLICY_DURATION} REPLICATION {RETENTION_POLICY_REPLICATION} DEFAULT"
    response = requests.post(f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}/query", params={'q': query})
    
    if response.status_code == 200:
        print(f"Politique de rétention '{RETENTION_POLICY_NAME}' créée avec succès.")
    else:
        print(f"Erreur lors de la création de la politique de rétention : {response.status_code}, réponse: {response.text}")

# Créer la base de données principale et la politique de rétention si nécessaire
create_database_if_not_exists(INFLUXDB_HOST, INFLUXDB_PORT, DATABASE)
create_retention_policy()  # Ajout de la création de la politique de rétention
