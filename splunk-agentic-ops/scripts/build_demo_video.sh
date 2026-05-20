#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
EDGE_TTS_PYTHON="${EDGE_TTS_PYTHON:-python3.11}"
EDGE_TTS_VOICE="${EDGE_TTS_VOICE:-en-US-AvaNeural}"
EDGE_TTS_RATE="${EDGE_TTS_RATE:--7%}"
OUT="$ROOT/media/agentops-flight-recorder-demo.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

make_screenshot_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local out="$4"

  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#000000B8" -draw "rectangle 0,810 1920,1080" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+900 "$title" \
    -font "$FONT" -fill white -pointsize 34 -annotate +72+980 "$subtitle" \
    "$out"
}

make_text_slide() {
  local title="$1"
  local subtitle="$2"
  local footer="$3"
  local out="$4"

  magick -size 1920x1080 xc:"#f5f7fb" \
    -fill "#143226" -draw "rectangle 0,0 1920,250" \
    -fill "#0b6b4f" -draw "rectangle 78,328 1842,358" \
    -fill "#ffffff" -font "$FONT" -pointsize 72 -annotate +82+148 "$title" \
    -fill "#e7f5ef" -font "$FONT" -pointsize 34 -annotate +86+216 "$subtitle" \
    -fill "#ffffff" -stroke "#d7e0e6" -strokewidth 3 -draw "roundrectangle 120,420 1800,735 24,24" \
    -stroke none -fill "#14212b" -font "$FONT" -pointsize 46 -annotate +170+520 "$footer" \
    -fill "#64717d" -font "$FONT" -pointsize 28 -annotate +170+640 "A verified local prototype with Splunk-ready events, SPL searches, dashboard, and evidence-bound AI summaries." \
    "$out"
}

cat > "$TMP_DIR/narration.txt" <<'TEXT'
AgentOps Flight Recorder is a black box for AI-agent operations.

AI agents can now run tools, call APIs, retry failures, and suggest production actions. But after an incident, teams need more than a chat transcript. They need to reconstruct what actually happened.

This prototype turns human, AI agent, robot, API, and system activity into structured operational events. Each event records the actor, action, status, risk, cost, approval requirement, and evidence reference.

Those events are exported as Splunk HEC-shaped payloads and draft SPL searches. Teams can search timelines, risky actions, retry loops, approval gates, and cost spikes.

The dashboard shows the review experience: active cases, risk signals, approvals, a chronological timeline, and SPL queries a team can bring into Splunk.

The AI layer is evidence-bound. It can summarize only from cited event IDs and search results, so humans can challenge, approve, reject, or hand off the work safely.

This submission is honest about its boundary: it is a verified local prototype with Splunk-ready artifacts. Live Splunk Cloud ingestion is the next step, not something claimed before verification.
TEXT

"$EDGE_TTS_PYTHON" -m edge_tts \
  --voice "$EDGE_TTS_VOICE" \
  --rate="$EDGE_TTS_RATE" \
  --file "$TMP_DIR/narration.txt" \
  --write-media "$TMP_DIR/narration.mp3"

make_text_slide \
  "AgentOps Flight Recorder" \
  "A Splunk-ready black box for AI-agent operations" \
  "When AI agents act, teams need searchable evidence." \
  "$TMP_DIR/slide-0.png"

make_screenshot_slide "$ROOT/media/flight-recorder-dashboard-full.png" \
  "From Chat Transcript To Operational Timeline" \
  "Review cases, risk, approvals, cost, and evidence in one surface." \
  "$TMP_DIR/slide-1.png"

make_screenshot_slide "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "Structured AgentOps Events" \
  "Capture human, AI, robot, API, and system activity with event IDs." \
  "$TMP_DIR/slide-2.png"

make_text_slide \
  "Splunk-Ready Architecture" \
  "HEC-shaped payloads, SPL searches, dashboard review, and evidence-bound AI" \
  "Events become searchable evidence before humans make decisions." \
  "$TMP_DIR/slide-3.png"

make_text_slide \
  "Evidence-Bound AI Investigation" \
  "Summaries cite event IDs instead of inventing facts" \
  "Humans can challenge, approve, reject, or hand off safely." \
  "$TMP_DIR/slide-4.png"

make_screenshot_slide "$ROOT/media/flight-recorder-dashboard-full.png" \
  "Honest Submission Boundary" \
  "Verified local prototype. Live Splunk Cloud ingestion is not claimed yet." \
  "$TMP_DIR/slide-5.png"

ffmpeg -y \
  -loop 1 -t 16 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 16 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 16 -i "$TMP_DIR/slide-2.png" \
  -loop 1 -t 16 -i "$TMP_DIR/slide-3.png" \
  -loop 1 -t 16 -i "$TMP_DIR/slide-4.png" \
  -loop 1 -t 16 -i "$TMP_DIR/slide-5.png" \
  -i "$TMP_DIR/narration.mp3" \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v];[6:a]loudnorm=I=-16:TP=-1.5:LRA=11,volume=0.85[a]" \
  -map "[v]" -map "[a]" -r 30 -shortest -movflags +faststart "$OUT"

cp "$OUT" "$ROOT/media/agentops-flight-recorder-demo-draft.mp4"
rm -rf "$TMP_DIR"
echo "$OUT"
