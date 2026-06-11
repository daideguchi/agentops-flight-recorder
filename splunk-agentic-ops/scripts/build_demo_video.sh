#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
EDGE_TTS_PYTHON="${EDGE_TTS_PYTHON:-python3.11}"
EDGE_TTS_VOICE="${EDGE_TTS_VOICE:-en-US-AvaNeural}"
EDGE_TTS_RATE="${EDGE_TTS_RATE:--5%}"
OUT="$ROOT/media/agentops-flight-recorder-demo.mp4"
DRAFT_OUT="$ROOT/media/agentops-flight-recorder-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

cd "$REPO_ROOT/shared-agentops-engine"
python3 scripts/generate_portfolio_artifacts.py >/tmp/agentops-flight-recorder-shared-generate.json

cd "$ROOT"
python3 scripts/build_flight_recorder_dashboard.py >/tmp/agentops-flight-recorder-dashboard.json
node scripts/record_demo_video.mjs "$TMP_DIR/dashboard-recording.mp4" >/tmp/agentops-flight-recorder-recording-path.txt

cat > "$TMP_DIR/narration.txt" <<'TEXT'
AgentOps Flight Recorder is for operations teams that need to know what an AI agent actually did.

The problem is simple. After a risky agent run, a chat transcript is not enough. A team needs searchable evidence: event IDs, risk levels, approval gates, costs, and handoff context.

Here the working dashboard loads the agent event trail, filters risky actions, shows approval gates, and runs a Splunk-style search over the same evidence.

The AI use is evidence-bound investigation. The assistant can summarize the incident only from cited event IDs and search rows. If the evidence is missing, it cannot invent the answer.

That gives SRE, platform, and security teams a safer way to review, challenge, approve, reject, or resume AI-agent work.
TEXT

"$EDGE_TTS_PYTHON" -m edge_tts \
  --voice "$EDGE_TTS_VOICE" \
  --rate="$EDGE_TTS_RATE" \
  --file "$TMP_DIR/narration.txt" \
  --write-media "$TMP_DIR/narration.mp3"

ffmpeg -y \
  -i "$TMP_DIR/dashboard-recording.mp4" \
  -i "$TMP_DIR/narration.mp3" \
  -filter_complex "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,tpad=stop_mode=clone:stop_duration=45,format=yuv420p[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,volume=0.9[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 22 -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"

cp "$OUT" "$DRAFT_OUT"
rm -rf "$TMP_DIR"
echo "$OUT"
