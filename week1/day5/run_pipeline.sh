#!/usr/bin/env bash

set -e

BASE_DIR="$HOME/training/week1/day5"
LOG_FILE="$BASE_DIR/logs/cron.log"

echo "=== Cron run started at $(date) ===" >> "$LOG_FILE"

cd "$BASE_DIR"

# Run validation
./validate.sh >> "$LOG_FILE" 2>&1

# Create build artifact
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BUILD_FILE="artifacts/build-$TIMESTAMP.tgz"

tar -czf "$BUILD_FILE" src config.json logs

# Generate checksum
sha256sum "$BUILD_FILE" > "$BUILD_FILE.sha256"

echo "Build created: $BUILD_FILE" >> "$LOG_FILE"
echo "=== Cron run finished at $(date) ===" >> "$LOG_FILE"
