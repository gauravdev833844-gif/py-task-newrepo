import os
import sys
import json
import subprocess

url = "https://www.youtube.com/watch?v=gCNeDWCI0vo"
clients = [
    "android", "android_vr", "android_creator", "android_music", "android_problabs",
    "web", "web_embedded", "web_creator", "web_safari",
    "mweb", "tv", "tv_embedded"
]

print(f"Testing all player_clients for {url} on runner...\n")

for client in clients:
    cmd = [
        sys.executable, "-m", "yt_dlp", "--no-config", "--no-cache-dir",
        "-J", "--skip-download", "--socket-timeout", "10",
        "--extractor-args", f"youtube:player_client={client}",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        code = res.returncode
        out_len = len(res.stdout or "")
        err = (res.stderr or "").replace("\n", " ")[:150]
        is_live = False
        formats = 0
        if code == 0 and res.stdout.strip():
            d = json.loads(res.stdout)
            is_live = d.get("is_live")
            formats = len(d.get("formats", []))
            print(f"[{client:16}] SUCCESS: exit=0 formats={formats} is_live={is_live}")
        else:
            print(f"[{client:16}] FAIL: exit={code} | {err}")
    except Exception as e:
        print(f"[{client:16}] ERROR: {e}")
