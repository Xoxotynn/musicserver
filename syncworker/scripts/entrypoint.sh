#!/bin/bash

echo "----------------------------------------------------"
echo "🌍 Часовой пояс: ${TZ:-UTC}"
echo "🕒 Текущее время: $(date)"

envsubst < /app/crontab.template > /app/crontab

echo "✅ Расписание сформировано:"
cat /app/crontab
echo "----------------------------------------------------"

exec /usr/local/bin/supercronic /app/crontab