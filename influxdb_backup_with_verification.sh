#!/bin/bash

# Lire les configurations depuis le fichier config.ini
CONFIG_FILE="/home/pi/Desktop/main/config.ini"

# Fonction pour lire une valeur dans le fichier config.ini
function get_config_value() {
    local section=$1
    local key=$2
    local value=$(awk -F '=' -v section="$section" -v key="$key" '$1 ~ "\\["section"\\]" {found=1} found && $1==key {print $2; exit}' "$CONFIG_FILE")
    echo $value | xargs
}

# Configuration
INFLUXDB_HOST=$(get_config_value "INFLUXDB_BACKUP" "HOST")
INFLUXDB_PORT=$(get_config_value "INFLUXDB_BACKUP" "PORT")
DATABASE_NAME=$(get_config_value "INFLUXDB_BACKUP" "DATABASE_NAME")
BACKUP_DIR=$(get_config_value "INFLUXDB_BACKUP" "BACKUP_DIR")
BACKUP_NAME=$(get_config_value "INFLUXDB_BACKUP" "BACKUP_NAME")
MAX_RETRIES=$(get_config_value "INFLUXDB_BACKUP" "MAX_RETRIES")
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

# Fonction pour effectuer une sauvegarde et vérifier l'intégrité
perform_backup() {
    echo "Démarrage de la sauvegarde pour $DATABASE_NAME..."

    # Effectuer une sauvegarde incrémentielle (après la première sauvegarde complète)
    influxd backup -portable -host $INFLUXDB_HOST:$INFLUXDB_PORT "$BACKUP_PATH"

    # Générer un hash SHA-256 pour vérifier l'intégrité du fichier
    sha256sum "$BACKUP_PATH"/* > "$BACKUP_PATH/backup.sha256"

    # Vérification de l'intégrité des fichiers de sauvegarde
    cd "$BACKUP_PATH"
    if sha256sum -c backup.sha256; then
        echo "Sauvegarde réussie et vérifiée pour $DATABASE_NAME."
        return 0  # Succès
    else
        echo "Erreur : la sauvegarde est corrompue. Nouvelle tentative..."
        return 1  # Échec
    fi
}

# Boucle pour réessayer la sauvegarde si la vérification échoue
retry_count=0
while ! perform_backup; do
    retry_count=$((retry_count+1))
    if [ $retry_count -ge $MAX_RETRIES ]; then
        echo "Échec de la sauvegarde après $MAX_RETRIES tentatives."
        exit 1
    fi
    echo "Nouvelle tentative de sauvegarde ($retry_count/$MAX_RETRIES)..."
done

echo "Sauvegarde finalisée avec succès après $retry_count tentatives."
