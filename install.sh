#!/bin/bash

# Récupérer le nom d'hôte et l'adresse IP
hostname=$(hostname)
ip_address=$(hostname -I | awk '{print $1}')  # Récupérer la première adresse IP

# Mettre à jour le système et installer pip si nécessaire
echo "Mise à jour du système..."
sudo apt-get update

# Modifier le fichier /etc/modules pour ajouter i2c-bcm2708, i2c-dev et rtc-ds1307
echo "Modification du fichier /etc/modules..."
if ! grep -q "i2c-bcm2708" /etc/modules; then
    echo "i2c-bcm2708" | sudo tee -a /etc/modules
fi

if grep -q "i2c-dev" /etc/modules; then
    echo "Suppression du doublon de i2c-dev"
    sudo sed -i '/i2c-dev/d' /etc/modules
fi
echo "i2c-dev" | sudo tee -a /etc/modules

if ! grep -q "rtc-ds1307" /etc/modules; then
    echo "rtc-ds1307" | sudo tee -a /etc/modules
fi

# Modifier le fichier /etc/rc.local pour ajouter le périphérique DS1307 avant 'exit 0'
echo "Modification du fichier /etc/rc.local..."
if ! grep -q "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device" /etc/rc.local; then
    sudo sed -i -e '$i echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device\n' /etc/rc.local
fi

# Vérifier si pip3 est installé, sinon l'installer
if ! command -v pip3 &> /dev/null
then
    echo "pip3 n'est pas installé. Installation en cours..."
    sudo apt-get install python3-pip -y
fi

# Vérifier si python-smbus & i2c-tools sont installés, sinon les installer
if ! dpkg -l | grep -q python-smbus
then
    echo "python-smbus n'est pas installé. Installation en cours..."
    sudo apt-get install python-smbus -y
fi

if ! dpkg -l | grep -q i2c-tools
then
    echo "i2c-tools n'est pas installé. Installation en cours..."
    sudo apt-get install i2c-tools -y
fi

# Installation des dépendances Python via pip3
echo "Installation des dépendances Python via pip3..."
sudo pip3 install -r requirements.txt

# Vérifier l'installation de Grafana si nécessaire (Optionnel)
if ! command -v grafana &> /dev/null
then
    echo "Grafana n'est pas installé. Installation en cours..."
    sudo mkdir -p /etc/apt/keyrings/
    wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
    sudo apt-get update
    sudo apt-get install -y grafana
    sudo /bin/systemctl enable grafana-server
    echo "Lancement de Grafana en cours..."
    sudo /bin/systemctl start grafana-server
    echo "Grafana disponible sur cette adresse: http://$ip_address:3000/"
else
    echo "Grafana est déjà installé et disponible sur cette adresse: http://$ip_address:3000/."
fi

# Vérifier l'installation d'InfluxDB si nécessaire (Optionnel)
if ! command -v influx &> /dev/null
then
    echo "InfluxDB n'est pas installé. Veuillez installer InfluxDB séparément."
    echo "Référez-vous à la documentation pour l'installation d'InfluxDB suivant votre OS."
    echo "https://docs.influxdata.com/influxdb/"
else
    echo "InfluxDB est déjà installé."
fi

echo "Installation terminée."
