#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- Синхронизация архива скачивания и файлов ---"

TEMP_ARCHIVE=$(mktemp)

FIXED_COUNT=0

while read -r line; do
    track_id=$(echo "$line" | awk '{print $2}')
    
    if ls "$MUSIC_DIR"/*"[$track_id]"* > /dev/null 2>&1; then
        echo "$line" >> "$TEMP_ARCHIVE"
    else
        echo "⚠️ Файл для ID $track_id не найден. Запись будет удалена из архива"
        ((FIXED_COUNT++))
    fi
done < "$ARCHIVE_FILE"

mv "$TEMP_ARCHIVE" "$ARCHIVE_FILE"

echo "Синхронизация архива завершена. Исправлено записей: $FIXED_COUNT"