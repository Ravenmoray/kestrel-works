#!/usr/bin/env bash
# Cron entry point for Kestrel Works' Year One simulation.
#
# Each firing runs one unattended headless `claude -p` turn (see
# simulate-day-prompt.txt) that advances the simulated company calendar by
# one day, has a department produce one real deliverable, logs it, and
# pushes to GitHub. This wrapper's job is purely operational safety:
# - never let two runs overlap
# - never run once the simulation has stopped/completed
# - detect a failed/usage-limited run and self-disable the cron job rather
#   than retrying forever
#
# Uses --dangerously-skip-permissions because there is no human present to
# answer permission prompts. See HISTORY.md / departments/operations for the
# reasoning and the explicit human sign-off on that tradeoff.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STATE_FILE="departments/operations/state/sim-clock.json"
STOP_FILE="departments/operations/state/simulation.stopped"
LOCK_FILE="/tmp/kestrel-works-simulate-day.lock"
LOG_DIR="scripts/logs"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/simday-$TS.log"
mkdir -p "$LOG_DIR"

CRON_MARKER="scripts/simulate-day.sh"

disable_cron() {
  local reason="$1"
  echo "[$TS] Disabling cron job: $reason" | tee -a "$LOG_FILE"
  ( crontab -l 2>/dev/null | grep -vF "$CRON_MARKER" ) | crontab - || true
  echo "$reason" > "$STOP_FILE"
}

# --- overlap protection ---
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[$TS] Previous simulate-day run still in progress, skipping this firing." >> "$LOG_DIR/skipped.log"
  exit 0
fi

# --- stop conditions checked before spending any tokens ---
if [ -f "$STOP_FILE" ]; then
  echo "[$TS] Stop file present ($(cat "$STOP_FILE" 2>/dev/null)), removing cron entry and exiting." | tee -a "$LOG_FILE"
  disable_cron "stop file already present: $(cat "$STOP_FILE" 2>/dev/null)"
  exit 0
fi

STATUS="$(python3 -c "import json,sys; print(json.load(open('$STATE_FILE')).get('status','unknown'))" 2>>"$LOG_FILE" || echo "unreadable")"
if [ "$STATUS" != "running" ]; then
  echo "[$TS] sim-clock status is '$STATUS', not 'running' — stopping." | tee -a "$LOG_FILE"
  disable_cron "sim-clock.json status was '$STATUS' (not running)"
  exit 0
fi

# --- run the turn ---
echo "[$TS] Starting simulate-day turn. Log: $LOG_FILE" >> "$LOG_DIR/runs.log"
PROMPT="$(cat scripts/simulate-day-prompt.txt)"

set +e
timeout 1200 claude -p "$PROMPT" --dangerously-skip-permissions > "$LOG_FILE" 2>&1
EXIT_CODE=$?
set -e 2>/dev/null || true

# --- failure / usage-limit detection ---
if [ $EXIT_CODE -ne 0 ]; then
  echo "[$TS] claude -p exited with code $EXIT_CODE." >> "$LOG_FILE"
  disable_cron "claude -p exited non-zero ($EXIT_CODE) — see $LOG_FILE"
  exit 0
fi

if grep -qiE "usage limit|rate limit|quota exceeded|credit balance is too low|overloaded_error|insufficient_quota|please try again later|resets at" "$LOG_FILE"; then
  echo "[$TS] Usage/rate-limit language detected in output." >> "$LOG_FILE"
  disable_cron "usage/rate-limit indicator detected in $LOG_FILE"
  exit 0
fi

# --- authoritative check: what did the run actually leave in sim-clock.json? ---
STATUS_AFTER="$(python3 -c "import json,sys; print(json.load(open('$STATE_FILE')).get('status','unknown'))" 2>>"$LOG_FILE" || echo "unreadable")"
RESULT_LINE="$(grep -m1 '^SIMDAY_RESULT' "$LOG_FILE" || echo "SIMDAY_RESULT (no result line found)")"
echo "[$TS] $RESULT_LINE (sim-clock status after run: $STATUS_AFTER)" | tee -a "$LOG_DIR/runs.log"

if [ "$STATUS_AFTER" != "running" ]; then
  disable_cron "sim-clock.json status after run was '$STATUS_AFTER'"
fi
