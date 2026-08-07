#!/usr/bin/env python3
"""Z-MAX 链路健康检查 · 每10分钟cron执行"""
import requests, subprocess, sys, time

CHECKS = {
    "relay": "https://datadrive.world/api/relay/status",
    "orin": "https://datadrive.world/orin/status",
    "snapshot": "https://datadrive.world/api/snapshot/latest",
}

ok = True
for name, url in CHECKS.items():
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"[OK] {name}: 200")
        else:
            print(f"[FAIL] {name}: {r.status_code}")
            ok = False
    except Exception as e:
        print(f"[DOWN] {name}: {e}")
        ok = False

# Restart relay if down
if not ok:
    subprocess.run(["pkill", "-f", "zmax_relay.py"])
    time.sleep(1)
    subprocess.Popen(["python3", "/root/zmax-relay/zmax_relay.py"],
                     cwd="/root/zmax-relay")
    print("[ACTION] Relay restarted")

sys.exit(0 if ok else 1)
