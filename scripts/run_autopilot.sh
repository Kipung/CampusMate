#!/usr/bin/env bash
set -euo pipefail

ROADMAP="docs/roadmap.md"
LOGDIR="logs/$(date +%Y-%m-%d)"
mkdir -p "$LOGDIR"

while true; do
  gemini autopilot --roadmap "$ROADMAP" --hours 6 --log-dir "$LOGDIR"
  echo "[$(date)] ✅ 6-hour autopilot run complete." | tee -a "$LOGDIR/summary.log"

  # Optional: notify yourself on Mac
  # osascript -e 'display notification "Gemini run finished" with title "CampusMate"'

  # Sleep 2 minutes, then loop so it keeps working overnight
  sleep 120
done
