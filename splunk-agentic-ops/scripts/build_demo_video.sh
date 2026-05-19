#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
OUT="$ROOT/media/agentops-flight-recorder-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

make_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local out="$4"

  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#000000B3" -draw "rectangle 0,840 1920,1080" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+920 "$title" \
    -font "$FONT" -fill white -pointsize 34 -annotate +72+992 "$subtitle" \
    "$out"
}

make_slide "$ROOT/media/flight-recorder-dashboard-full.png" \
  "AgentOps Flight Recorder" \
  "Make AI-agent work searchable, reviewable, and accountable in Splunk." \
  "$TMP_DIR/slide-0.png"

make_slide "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "Operational Evidence Trail" \
  "Capture tool calls, risk, retries, approvals, cost, and handoff points." \
  "$TMP_DIR/slide-1.png"

make_slide "$ROOT/media/flight-recorder-dashboard-full.png" \
  "From Transcript To Timeline" \
  "Teams can reconstruct what the agent did after an incident." \
  "$TMP_DIR/slide-2.png"

ffmpeg -y \
  -loop 1 -t 7 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 7 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 7 -i "$TMP_DIR/slide-2.png" \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -r 30 -movflags +faststart "$OUT"

rm -rf "$TMP_DIR"
echo "$OUT"
