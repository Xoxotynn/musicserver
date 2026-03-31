#!/bin/bash
set -e

echo "=== Подготовка для развертывания Navidrome ==="

echo "[1/4] Установка Git"
sudo apt-get update
sudo apt-get install -y git

if ! command -v docker &> /dev/null; then
    echo "[2/4] Установка Docker"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker установлен."
else
    echo "[2/4] Docker уже установлен"
fi

echo "[3/4] Загрузка репозитория"
REPO_URL="git@github.com:Xoxotynn/musicserver.git"
REPO_NAME=$(basename "$REPO_URL" .git)

if [ ! -d "$REPO_NAME" ]; then
    git clone "$REPO_URL"
else
    echo "Папка $REPO_NAME уже существует"
fi

cd "$REPO_NAME"
chmod +x setup.sh

echo "================================================="
echo "Все установили"
echo "Чтобы развернуть сервер:"
echo "2. Скопируй конфиг: cp .env.example .env"
echo "3. Заполни секреты: nano .env"
echo "4. Запусти сервер: ./setup.sh"
echo "================================================="