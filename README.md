
# Système de Surveillance Environnementale

Ce projet est un système de surveillance environnementale basé sur l'IoT, conçu pour fonctionner sur un microcontrôleur ou un Raspberry Pi. Le système collecte des données à partir de divers capteurs, affiche les informations sur un écran LCD et stocke les données dans une base de données InfluxDB. Il prend également en charge la gestion du réseau, y compris la connexion automatique au Wi-Fi ou à l'Ethernet, la synchronisation de l'heure via NTP et les mises à jour RTC.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Matériel Requis](#matériel-requis)
- [Logiciels Requis](#logiciels-requis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Fonctionnalités

- **Collecte de Données Environnementales** : Collecte des données de température, humidité, pression, niveaux de CO2, et particules.
- **Affichage des Données** : Affiche les données environnementales en temps réel sur un écran LCD.
- **Enregistrement des Données** : Enregistre les données environnementales dans une base de données InfluxDB avec une politique de rétention configurable.
- **Gestion du Réseau** : Connexion automatique à un réseau Wi-Fi ou Ethernet et synchronisation de l'heure via NTP.
- **Gestion du Temps** : Synchronisation de l'horloge système avec une RTC (Real-Time Clock) en cas d'échec de la synchronisation réseau.

## Matériel Requis

- **Raspberry Pi** (ou microcontrôleur compatible avec le bus I2C)
- **Capteurs** :
  - BME280 (Température, Humidité, Pression)
  - SCD4x (CO2)
  - PMSA003I (Capteur de Particules)
- **Écran LCD** : Compatible avec la bibliothèque Python `lcddriver`
- **Module RTC** (Optionnel)
- **Connectivité Wi-Fi/Ethernet**

## Logiciels Requis

- **Python 3.x**
- **InfluxDB** : Si InfluxDB n'est pas encore installé, suivez les instructions de la [documentation officielle](https://docs.influxdata.com/influxdb/v1/introduction/install/).

## Installation

### Installation Automatique

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votreutilisateur/systeme-surveillance-environnementale.git
   cd systeme-surveillance-environnementale
   ```

2. **Exécuter le script d'installation** :
   ```bash
   ./install.sh
   ```

   Ce script mettra à jour les paquets système, installera `pip3` s'il n'est pas installé, puis installera toutes les dépendances Python listées dans `requirements.txt`. Il vérifiera également si InfluxDB est installé.

### Installation Manuelle

Si vous préférez installer les dépendances manuellement, vous pouvez simplement exécuter :

```bash
pip3 install -r requirements.txt
```

## Configuration

1. **Modifier le fichier `config.ini`** :
   - Ajouter votre SSID Wi-Fi, mot de passe, détails InfluxDB, et interfaces réseau.
   - Spécifier la politique de rétention pour la base de données InfluxDB.

   Exemple de configuration :
   ```ini
   [WIFI]
   SSID = VotreSSIDWiFi
   PASSWORD = VotreMotDePasseWiFi

   [NETWORK]
   WIFI_INTERFACE = wlan0
   ETHERNET_INTERFACE = eth0

   [INFLUXDB]
   HOST = votre_hote_influxdb
   PORT = 8086
   DATABASE = votre_nom_de_base_de_donnees
   RETENTION_POLICY_NAME = five_years
   RETENTION_POLICY_DURATION = 1825d  # 5 ans
   RETENTION_POLICY_REPLICATION = 1
   ```

## Utilisation

1. **Exécuter le système** :
   ```bash
   python main.py
   ```

2. **Surveiller la sortie** :
   - Le système tentera de se connecter au Wi-Fi ou à l'Ethernet et de synchroniser l'heure.
   - Il commencera ensuite à collecter les données des capteurs, à les afficher sur l'écran LCD et à les enregistrer dans InfluxDB.

3. **Accéder aux données** :
   - Utilisez un client InfluxDB ou Grafana pour visualiser les données enregistrées.

## Structure du Projet

```
systeme-surveillance-environnementale/
│
├── main.py                 # Script de contrôle principal
├── sensors.py              # Gestion des capteurs (BME280, SCD4x, PMSA003I)
├── lcd_display.py          # Gestion de l'affichage sur l'écran LCD
├── data_logger.py          # Enregistrement des données dans InfluxDB avec politique de rétention
├── network.py              # Gestion du réseau et synchronisation du temps
├── config.ini              # Fichier de configuration pour le Wi-Fi, InfluxDB et les paramètres réseau
├── requirements.txt        # Dépendances Python
├── install.sh              # Script d'installation pour automatiser l'installation des dépendances
└── README.md               # Documentation du projet
```

## Contribuer

Les contributions sont les bienvenues ! Si vous avez des suggestions d'amélioration ou de nouvelles fonctionnalités, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
