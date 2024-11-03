import subprocess
from wifi import Cell, Scheme
from wifi.exceptions import InterfaceError
import configparser

# Lecture des paramètres depuis config.ini
config = configparser.ConfigParser()
config_file_path = '/home/pi/Desktop/main/config.ini'

config.read(config_file_path)

WIFI_SSID = config['WIFI']['SSID']
WIFI_PASSWORD = config['WIFI']['PASSWORD']
WIFI_INTERFACE = config['NETWORK']['WIFI_INTERFACE']
ETHERNET_INTERFACE = config['NETWORK']['ETHERNET_INTERFACE']

def get_current_ssid(interface):
    """Récupère le SSID actuel de l'interface donnée."""
    try:
        result = subprocess.run(['iwgetid', '-r', interface], capture_output=True, text=True)
        current_ssid = result.stdout.strip()
        return current_ssid if current_ssid else None
    except Exception as e:
        print(f"Erreur lors de la récupération du SSID actuel pour {interface} : {e}")
        return None

def connect_to_wifi():
    try:
        # Vérifier si l'interface est déjà connectée au bon réseau
        current_ssid = get_current_ssid(WIFI_INTERFACE)
        if current_ssid == WIFI_SSID:
            print(f"Déjà connecté au réseau Wi-Fi '{WIFI_SSID}' via {WIFI_INTERFACE}.")
            return True

        # Recherche des réseaux Wi-Fi disponibles
        wifi_networks = [network for network in list(Cell.all(WIFI_INTERFACE)) if network.ssid == WIFI_SSID]

        if wifi_networks:
            desired_network = wifi_networks[0]
            interface = WIFI_INTERFACE

            # Vérifier si le schéma existe déjà pour éviter l'assertion
            existing_scheme = Scheme.find(interface, WIFI_SSID)
            if existing_scheme:
                print(f"Le schéma pour '{WIFI_SSID}' existe déjà. Activation en cours...")
                existing_scheme.activate()
            else:
                # Créer et sauvegarder un nouveau schéma de connexion
                scheme = Scheme.for_cell(interface, WIFI_SSID, desired_network, passkey=WIFI_PASSWORD)
                scheme.save()
                scheme.activate()
                print(f"Connecté à {desired_network.ssid} via {interface}")
            return True
        else:
            print("Aucun réseau Wi-Fi disponible. Tentative de connexion via Ethernet.")

            try:
                ethernet_networks = list(Cell.all(ETHERNET_INTERFACE))
            except InterfaceError as e:
                print(f"Erreur lors de la recherche des réseaux Ethernet : {e}")
                ethernet_networks = []

            if ethernet_networks:
                desired_network = ethernet_networks[0]
                interface = ETHERNET_INTERFACE
                # Utilisation du schéma Ethernet si nécessaire (pas souvent requis, mais au cas où)
                scheme = Scheme.for_cell(interface, desired_network.ssid, desired_network)
                scheme.save()
                scheme.activate()
                print(f"Connecté à {desired_network.ssid} via {interface}")
            else:
                print("Aucun réseau Wi-Fi ni Ethernet disponible.")
                return False

    except InterfaceError as e:
        print(f"Erreur lors de la recherche des réseaux WiFi : {e}")
        return False

def synchronize_time():
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'systemd-timesyncd'], check=True)
        print("Synchronisation avec NTP réussie.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la synchronisation avec NTP : {e}")

def sync_rtc_with_system_time():
    try:
        subprocess.run(['sudo', 'hwclock', '--systohc'], check=True)
        print("Synchronisation RTC réussie.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la synchronisation du RTC avec l'heure système : {e}")

def update_system_time_from_rtc():
    try:
        subprocess.run(['sudo', 'hwclock', '--hctosys'], check=True)
        print("Heure système mise à jour depuis le RTC.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la mise à jour de l'heure système depuis le RTC : {e}")

if __name__ == "__main__":
    connect_success = connect_to_wifi()

    if connect_success:
        synchronize_time()
        sync_rtc_with_system_time()
    else:
        print("Aucune connexion réseau. Tentative de mise à jour de l'heure depuis l'horloge RTC.")
        update_system_time_from_rtc()
