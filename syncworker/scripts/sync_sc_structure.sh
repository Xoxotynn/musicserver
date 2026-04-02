#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- Шаг 3: Синхронизация лайков и создание плейлистов ---"

yt-dlp --flat-playlist --dump-single-json "$SOUNDCLOUD_URL" > "$TEMP_LIKES_DATA_FILE"

VALID_IDS_FILE="/tmp/valid_sc_ids.txt"
> "$VALID_IDS_FILE"

echo "Добавление новых лайков"

rm -f "$PLAYLISTS_DIR"/*.m3u

jq -c '.entries | reverse | .[]' "$TEMP_LIKES_DATA_FILE" | while read -r entry; do
    item_url=$(echo "$entry" | jq -r '.url')
    id=$(echo "$entry" | jq -r '.id')
    raw_title=$(echo "$entry" | jq -r '.title')
    clean_title=$(echo "$raw_title" | tr -d '/\?%*:|"<>' | sed 's/^[.-]*//')
    [ -z "$clean_title" ] && clean_title="unnamed_playlist_${id}"

    if [[ "$item_url" == *"/sets/"* ]]; then
        echo "[Playlist] Создаем: $raw_title"
        M3U_FILE="$PLAYLISTS_DIR/$clean_title.m3u"
        echo "#EXTM3U" > "$M3U_FILE"

        yt-dlp --flat-playlist --get-id "$item_url" | while read -r track_id; do
            echo "$track_id" >> "$VALID_IDS_FILE"

            filename=$(find "$MUSIC_DIR" -maxdepth 1 -type f | grep -F "[$track_id]" | sed 's|.*/||' | head -n 1)
            [ -n "$filename" ] && echo "../$filename" >> "$M3U_FILE"
        done
    else
        echo "[Like] Обработка трека: $raw_title"

        echo "$id" >> "$VALID_IDS_FILE"

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

echo "Очистка удаленных лайков"

find "$MUSIC_DIR" -maxdepth 1 -type f -name "*\[*\].*" | while read -r file; do
    track_id=$(echo "$file" | grep -o '\[[0-9]\+\]' | tr -d '[]')
    
    if ! grep -qw "$track_id" "$VALID_IDS_FILE"; then
        echo "Удаляем: $file"
        rm -f "$file"
        sed -i "/^soundcloud $track_id$/d" "$ARCHIVE_FILE"
    fi
done

rm -f "$TEMP_LIKES_DATA_FILE"
rm -f "$VALID_IDS_FILE"