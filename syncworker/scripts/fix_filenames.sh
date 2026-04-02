#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- 📥 Загрузка актуальных данных из SoundCloud... ---"

MAPPING_FILE="/tmp/sc_id_title_mapping.txt"
> "$MAPPING_FILE"

yt-dlp --flat-playlist --dump-single-json "$SOUNDCLOUD_URL" > "$TEMP_LIKES_DATA_FILE"
jq -r '.entries[] | select(.url | contains("/sets/") | not) | "\(.id) \(.title)"' "$TEMP_LIKES_DATA_FILE" >> "$MAPPING_FILE"

jq -r '.entries[] | select(.url | contains("/sets/")) | .url' "$TEMP_LIKES_DATA_FILE" | while read -r playlist_url; do
    echo "📂 Дамп плейлиста: $playlist_url"
    yt-dlp --print "%(id)s %(title)s" "$playlist_url" >> "$MAPPING_FILE"
done

echo "--- 🛠️ Запуск восстановления имен ---"

cd "$MUSIC_DIR" || { echo "❌ Папка не найдена"; exit 1; }

find . -maxdepth 1 -type f -name "*\[*\]*" | while read -r old_path; do
    old_name=$(basename "$old_path")
    track_id=$(echo "$old_name" | grep -o '\[[0-9]\+\]' | tr -d '[]')
    ext="${old_name##*.}"

    [ -z "$track_id" ] && continue

    real_title=$(grep "^$track_id " "$MAPPING_FILE" | head -n 1 | cut -d' ' -f2-)

    if [ -z "$real_title" ]; then
        echo "⚠️ Название для $track_id не найдено в SoundCloud"
        new_name="[$track_id].$ext"
    else
        clean_title=$(echo "$real_title" | tr -d '/\?%*:|"<>\')
        new_name="[$track_id] $clean_title.$ext"
    fi

    if [ "$old_name" != "$new_name" ]; then
        echo "✨ $old_name -> $new_name"
        mv "$old_name" "$new_name"
    fi
done

rm "$TEMP_LIKES_DATA_FILE"
rm "$MAPPING_FILE"

echo "--- ✅ Молимся чтобы не отъебнуло ---"