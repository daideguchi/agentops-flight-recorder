#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
SHARED_ROOT="$REPO_ROOT/shared-agentops-engine"
VIDEO="$ROOT/media/agentops-flight-recorder-demo.mp4"

cd "$SHARED_ROOT"
python3 scripts/generate_portfolio_artifacts.py >/tmp/agentops-flight-recorder-shared-generate.json
python3 scripts/verify_artifacts.py >/tmp/agentops-flight-recorder-shared-verify.json

cd "$ROOT"
python3 scripts/build_flight_recorder_dashboard.py >/tmp/agentops-flight-recorder-dashboard.json
bash scripts/build_demo_video.sh >/tmp/agentops-flight-recorder-video-path.txt

python3 - "$REPO_ROOT" "$VIDEO" <<'PY'
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
video = Path(sys.argv[2])

required = [
    repo_root / "ARCHITECTURE.md",
    repo_root / "architecture-diagram.svg",
    repo_root / "README.md",
    repo_root / "SUBMISSION_PACKAGE.md",
    repo_root / "shared-agentops-engine" / "adapters" / "splunk" / "hec_events.jsonl",
    repo_root / "shared-agentops-engine" / "adapters" / "splunk" / "searches.spl",
    repo_root / "splunk-agentic-ops" / "prototype" / "flight-recorder-dashboard.html",
    repo_root / "splunk-agentic-ops" / "media" / "flight-recorder-dashboard-full.png",
    video,
]

missing = [str(path.relative_to(repo_root)) for path in required if not path.exists()]
if missing:
    raise SystemExit(f"missing_required_files={missing}")

events_path = repo_root / "shared-agentops-engine" / "adapters" / "splunk" / "hec_events.jsonl"
events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
if len(events) < 20:
    raise SystemExit(f"too_few_splunk_events={len(events)}")

probe = subprocess.check_output(
    [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size",
        "-show_entries",
        "stream=codec_type,codec_name,width,height",
        "-of",
        "json",
        str(video),
    ],
    text=True,
)
media = json.loads(probe)
duration = float(media["format"]["duration"])
streams = media["streams"]
has_video = any(stream.get("codec_type") == "video" and stream.get("width") == 1920 for stream in streams)
has_audio = any(stream.get("codec_type") == "audio" for stream in streams)
if not (30 <= duration < 180 and has_video and has_audio):
    raise SystemExit(f"bad_video duration={duration} has_video={has_video} has_audio={has_audio}")

print("splunk_local_checks_ok")
print(f"hec_events={len(events)}")
print(f"video_seconds={duration:.1f}")
print("architecture=root")
print("claim_boundary=verified_local_splunk_ready_no_live_ingestion_claim")
PY
