#!/bin/bash
# Self-Healing Linux Server
# Monitors one configured systemd service and restarts it if it is inactive.
# Run with appropriate privileges on a Linux server.

SERVICE="${SERVICE:-nginx}"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$BASE_DIR/logs/self_healing.log"
CHECK_INTERVAL="${CHECK_INTERVAL:-10}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Self-healing monitor started for service: $SERVICE"

while true; do
  if systemctl is-active --quiet "$SERVICE"; then
    log "$SERVICE is healthy."
  else
    log "ALERT: $SERVICE is inactive. Attempting automatic recovery..."
    systemctl restart "$SERVICE"
    sleep 2

    if systemctl is-active --quiet "$SERVICE"; then
      log "RECOVERY SUCCESS: $SERVICE restarted successfully."
    else
      log "RECOVERY FAILED: $SERVICE could not be restored."
    fi
  fi
  sleep "$CHECK_INTERVAL"
done
