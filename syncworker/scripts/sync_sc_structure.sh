#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- Шаг 3: Синхронизация лайков и создание плейлистов ---"

yt-dlp --flat-playlist --dump-single-json "$SOUNDCLOUD_URL" > "$TEMP_LIKES_DATA_FILE"

rm -f "$PLAYLISTS_DIR"/*.m3u

jq -c '.entries | reverse | .[]' "$TEMP_LIKES_DATA_FILE" | while read -r entry; do
    item_url=$(echo "$entry" | jq -r '.url')
    id=$(echo "$entry" | jq -r '.id')
    raw_title=$(echo "$entry" | jq -r '.title')
    clean_title=$(echo "$raw_title" | tr -d '/\?%*:|"<>')

    if [[ "$item_url" == *"/sets/"* ]]; then
        echo "[Playlist] Создаем: $raw_title"
        M3U_FILE="$PLAYLISTS_DIR/$clean_title.m3u"
        echo "#EXTM3U" > "$M3U_FILE"

        yt-dlp --flat-playlist --get-id "$item_url" | while read -r track_id; do
            filename=$(find "$MUSIC_DIR" -maxdepth 1 -type f | grep -F "[$track_id]" | sed 's|.*/||' | head -n 1)
            [ -n "$filename" ] && echo "../$filename" >> "$M3U_FILE"
        done
    else
        echo "[Like] Обработка трека: $raw_title"

        SEARCH_QUERY=$(echo -n "$raw_title" | jq -sRr @uri)
        SEARCH_RESULT=$(curl -s "${ENDPOINT_SEARCH}&query=${SEARCH_QUERY}")
        TRACK_ID=$(echo "$SEARCH_RESULT" | jq -r '."subsonic-response".searchResult3.song[0].id // empty')

        if [ -n "$TRACK_ID" ] && [ "$TRACK_ID" != "null" ]; then
            curl -s "${ENDPOINT_STAR}&id=${TRACK_ID}" > /dev/null
            echo " ✅ -> Лайк поставлен в Navidrome"
        else
            echo " ❌ -> Трек не найден в библиотеке"
        fi
    fi
done

rm "$TEMP_LIKES_DATA_FILE"