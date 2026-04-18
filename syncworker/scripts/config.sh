#!/bin/bash
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Paths
export MUSIC_DIR="/music"
export PLAYLISTS_DIR="$MUSIC_DIR/playlists"
export ARCHIVE_FILE="$MUSIC_DIR/archive.txt"
export TEMP_LIKES_DATA_FILE="/tmp/likes_data.json"

# Navidrome API
export NAV_URL="http://127.0.0.1:${ND_PORT}/rest"
export NAV_USER="${ND_USER}"
export NAV_PASS="${ND_PASS}"
export NAV_SALT="${ND_SALT}"

# Token gen
TOKEN=$(echo -n "${NAV_PASS}${NAV_SALT}" | md5sum | awk '{print $1}')
export API_PARAMS="u=${NAV_USER}&t=${TOKEN}&s=${NAV_SALT}&v=1.16.1&c=sync_script&f=json"

export ENDPOINT_SCAN="${NAV_URL}/startScan.view?${API_PARAMS}"
export ENDPOINT_STATUS="${NAV_URL}/getScanStatus.view?${API_PARAMS}"
export ENDPOINT_SEARCH="${NAV_URL}/search3.view?${API_PARAMS}"
export ENDPOINT_STAR="${NAV_URL}/star.view?${API_PARAMS}"
export ENDPOINT_UNSTAR="${NAV_URL}/unstar.view?${API_PARAMS}"
export ENDPOINT_GET_STARRED="${NAV_URL}/getStarred.view?${API_PARAMS}"

mkdir -p "$PLAYLISTS_DIR"
