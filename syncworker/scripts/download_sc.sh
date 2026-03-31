#!/bin/bash
source "$(dirname "$0")/config.sh"

echo "--- Шаг 1: Загрузка новых треков из SoundCloud ---"
yt-dlp -i --download-archive "$ARCHIVE_FILE" \
  --format "bestaudio/best" --extract-audio --audio-quality 0 \
  --embed-metadata --embed-thumbnail \
  --output "$MUSIC_DIR/%(title)s - %(uploader)s [%(id)s].%(ext)s" \
  --restrict-filenames "$SOUNDCLOUD_URL"