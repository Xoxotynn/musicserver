#!/bin/bash
set -e

BASE_DIR=$(dirname "$0")

echo "=== ЗАПУСК ПОЛНОЙ СИНХРОНИЗАЦИИ ==="

$BASE_DIR/sync_archive.sh
$BASE_DIR/download_sc.sh
$BASE_DIR/scan_navidrome.sh
$BASE_DIR/sync_sc_structure.sh
$BASE_DIR/scan_navidrome.sh

echo "=== СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА ==="