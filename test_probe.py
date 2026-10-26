import os
import sys
import json
import subprocess

cookie_text = os.environ.get("YT_COOKIES", "").strip()
cookie_file = "/tmp/test_cookies.txt"
with open(cookie_file, "w", encoding="utf-8") as f:
    f.write(cookie_text)

url = "https://www.youtube.com/watch?v=gCNeDWCI0vo"
clients = ["web", "mweb", "android", "tv", "ios"]

print(f"Testing url={url} with cookies (bytes: {len(cookie_text)}) + Deno...\n")

for client in clients:
    cmd = [
        sys.executable, "-m", "yt_dlp", "--no-config", "--no-cache-dir",
        "-J", "--skip-download", "--socket-timeout", "15",
        "--cookies", cookie_file,
        "--extractor-args", f"youtube:player_client={client}",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        code = res.returncode
        out_len = len(res.stdout or "")
        err = (res.stderr or "").replace("\n", " ")[:200]
        if code == 0 and res.stdout.strip():
            d = json.loads(res.stdout)
            print(f"[{client:10}] SUCCESS: exit=0 formats={len(d.get('formats', []))} is_live={d.get('is_live')} live_status={d.get('live_status')}")
        else:
            print(f"[{client:10}] FAIL: exit={code} | {err}")
    except Exception as e:
        print(f"[{client:10}] ERROR: {e}")
