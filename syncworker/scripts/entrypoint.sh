#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "----------------------------------------------------"
echo "🌍 Часовой пояс: ${TZ:-UTC}"
echo "🕒 Текущее время: $(date)"

envsubst < /app/crontab.template > /app/crontab

echo "✅ Расписание сформировано:"
cat /app/crontab
echo "----------------------------------------------------"

NSP_FILE="$PLAYLISTS_DIR/favorites.nsp"

if [ ! -f "$NSP_FILE" ]; then
    echo "🎵 Смарт-плейлист не найден. Создаем $NSP_FILE..."
    cat <<EOF > "$NSP_FILE"
{
  "all": [
    {"is": {"loved": true}}
  ],
  "sort": "dateLoved",
  "order": "desc"
}
EOF
    chmod 0644 "$NSP_FILE"
    echo "✅ Плейлист My_Favorites.nsp успешно создан!"
else
    echo "🎵 Смарт-плейлист уже существует, пропускаем."
fi

exec /usr/local/bin/supercronic /app/crontab