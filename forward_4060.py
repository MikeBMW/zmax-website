#!/usr/bin/env python3
"""ECS → 4060 数据转发器
监控 relay 数据目录，隧道通后自动推送到 xspace 4060
目标路径: /root/datasets/act_training/
"""
import time, os, subprocess, glob
from pathlib import Path

SRC = Path("/root/zmax-relay/data")
DST = "root@localhost:/root/datasets/act_training/"
TUNNEL_PORT = 50053
sent = set()

def tunnel_up():
    r = subprocess.run(["netstat", "-tlnp"], capture_output=True, text=True)
    return f":{TUNNEL_PORT}" in r.stdout

def push_files():
    files = sorted(glob.glob(str(SRC / "pkg_*.json")))
    new = [f for f in files if f not in sent]
    if not new:
        return 0
    for f in new[-50:]:  # 最多一次推50个
        try:
            subprocess.run([
                "sshpass", "-p", "Nix19789", "scp",
                "-o", "StrictHostKeyChecking=no",
                "-o", "ConnectTimeout=3",
                "-P", str(TUNNEL_PORT),
                f, DST
            ], timeout=10, capture_output=True)
            sent.add(f)
            print(f"[{time.strftime('%H:%M:%S')}] 已推送: {os.path.basename(f)}")
        except Exception as e:
            print(f"推送失败: {e}")
            break
    return len(new)

if __name__ == "__main__":
    print("ECS→4060 转发器启动")
    print(f"源: {SRC}")
    print(f"目标: {DST}")
    print(f"等待隧道 {TUNNEL_PORT} ...")
    while True:
        if tunnel_up():
            n = push_files()
            if n: print(f"已转发 {n} 个文件")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] 隧道未通，等待...")
        time.sleep(10)
