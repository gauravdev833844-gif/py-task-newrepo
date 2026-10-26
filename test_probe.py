import os
import sys
import json
import subprocess

channels = [
    ("AlJazeera", "https://www.youtube.com/watch?v=gCNeDWCI0vo"),
    ("DWNews", "https://www.youtube.com/watch?v=LuKwFajn37U"),
    ("France24", "https://www.youtube.com/watch?v=HvZt-nh9sGg"),
    ("NASA", "https://www.youtube.com/@NASA/live"),
]

cookie_text = os.environ.get("YT_COOKIES", "").strip()
cookie_file = "/tmp/test_cookies.txt"
has_cookies = False
if cookie_text:
    with open(cookie_file, "w", encoding="utf-8") as f:
        f.write(cookie_text)
    has_cookies = True

print(f"Has cookies: {has_cookies} (bytes: {len(cookie_text)})")

clients = ["android", "web", "ios", "tv"]

for name, url in channels:
    print(f"\n==================== {name}: {url} ====================")
    for use_c in ([True, False] if has_cookies else [False]):
        c_label = "WITH_COOKIES" if use_c else "NO_COOKIES"
        for client in clients:
            cmd = [
                sys.executable, "-m", "yt_dlp", "--no-config", "--no-cache-dir",
                "-J", "--skip-download",
                "--socket-timeout", "10",
                "--extractor-args", f"youtube:player_client={client}",
            ]
            if use_c:
                cmd += ["--cookies", cookie_file]
            cmd.append(url)
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                exit_code = res.returncode
                stdout_len = len(res.stdout or "")
                stderr_snip = (res.stderr or "").replace("\n", " ")[:200]
                
                is_live = None
                live_status = None
                formats_count = 0
                title = None
                if exit_code == 0 and res.stdout.strip():
                    try:
                        d = json.loads(res.stdout)
                        is_live = d.get("is_live")
                        live_status = d.get("live_status")
                        formats_count = len(d.get("formats", []))
                        title = d.get("title", "")[:40]
                    except Exception as e:
                        stderr_snip = f"JSON parse error: {e}"
                        
                print(f"[{c_label}] [{client:7}] exit={exit_code:2} bytes={stdout_len:6} formats={formats_count:2} is_live={is_live} live_status={live_status} | {title or stderr_snip}")
            except subprocess.TimeoutExpired:
                print(f"[{c_label}] [{client:7}] TIMEOUT (15s)")
            except Exception as e:
                print(f"[{c_label}] [{client:7}] ERROR: {e}")
