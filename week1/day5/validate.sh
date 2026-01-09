#!/bin/bash

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/validate.log"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Validation started"

# Check src directory
if [ ! -d "src" ]; then
  log "ERROR: src directory missing"
  echo "❌ src directory not found"
  exit 1
fi
log "src directory exists"

# Check config.json
if [ ! -f "config.json" ]; then
  log "ERROR: config.json missing"
  echo "❌ config.json not found"
  exit 1
fi

# Validate JSON
if ! jq empty config.json > /dev/null 2>&1; then
  log "ERROR: Invalid config.json"
  echo "❌ config.json is invalid JSON"
  exit 1
fi
log "config.json is valid"

log "Validation completed successfully"
echo "✅ Validation passed"
exit 0
