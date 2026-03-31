#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- Запуск сканирования Navidrome ---"
curl -s "$ENDPOINT_SCAN" > /dev/null

while true; do
    STATUS=$(curl -s "$ENDPOINT_STATUS")
    IS_SCANNING=$(echo "$STATUS" | jq -r '."subsonic-response".scanStatus.scanning')

    if [ "$IS_SCANNING" == "false" ]; then
        echo "Сканирование завершено"
        break
    fi
    sleep 2
done