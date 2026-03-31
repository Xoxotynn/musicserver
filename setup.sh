#!/bin/bash
set -e

echo "=== Поехали ==="

if [ ! -f .env ]; then
    echo "Файл .env не найден. Копирую из .env.example"
    cp .env.example .env
    echo "заполни файл .env своими данными (пароли, ссылки) и запусти скрипт снова, чепушила"
    exit 1
fi

echo "Создание директорий"
mkdir -p data music
sudo chown -R 1000:1000 data music

echo "Сборка и запуск контейнеров"
docker compose up -d --build

echo "Развернулись, врубай темного принца"
echo "Для ручного запуска синхронизации:"
echo "docker compose exec sync-worker /app/scripts/full_sync.sh"