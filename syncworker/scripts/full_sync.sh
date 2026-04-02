#!/bin/bash
set -e

BASE_DIR=$(dirname "$0")

RUN_FIX=false

for arg in "$@"; do
  case $arg in
    -f|--fix-filenames)
      RUN_FIX=true
      shift
      ;;
  esac
done

echo "=== ЗАПУСК ПОЛНОЙ СИНХРОНИЗАЦИИ ==="

if [ "$RUN_FIX" = true ]; then
    echo "🛠️ Запуск фикса имен файлов"
    if [ -f "./fix_filenames.sh" ]; then
        $BASE_DIR/fix_filenames.sh
    else
        echo "❌ Скрипт фикса имен файлов fix_filenames.sh не найден"
    fi
else
    echo "ℹ️ Пропускаем фикс имен"
fi

$BASE_DIR/sync_archive.sh
$BASE_DIR/download_sc.sh
$BASE_DIR/scan_navidrome.sh
$BASE_DIR/sync_sc_structure.sh
$BASE_DIR/scan_navidrome.sh

echo "=== СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА ==="