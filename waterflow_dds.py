#!/usr/bin/env python3
"""
Z-MAX 水流式全局数据空间 · 原型 (v1)
====================================
设计理念: "数据如水流" — Orin采集源头 → 各链路节点(ECS/训练/部署/推理)
→ 持续刷写全局 DDS, 每个节点实时更新状态, 像水流不断冲刷数据库。

映射模型:
  NODE (链路节点)     = 采集/上传/训练/部署/推理/控制台
  TOPIC (数据主题)    = relay 各 API / ROS2 topic / 模型静态URL
  原子技能 (atomic)   = 每个节点关联的 DDS 原子技能 (242条)
  条件 (condition)    = 节点流转条件 (帧数阈值/loss阈值/infer>0等)

刷写机制: 水流守护 (waterflow daemon) 每 10s 拉取各节点真实状态
→ 计算条件 → 更新 dds.db 新增表 dds_flow (时间序列) + dds_node_state (实时)
→ 全站 API 读取, 形成"流动的数据空间"
"""
import sqlite3, json, time, os, sys, subprocess
from datetime import datetime

DDS_DB = "/home/xspace/zmax-website/dds.db"
RELAY = "https://datadrive.world/api/relay"
MODEL_URL = "https://datadrive.world/models/act_cartesian.safetensors"

# ── 链路节点定义 (物理基础: 数据实际流经的每个环节) ──
NODES = [
    {"id": "orin_collect", "name": "Orin 采集", "icon": "📡", "stage": "采集",
     "topic": "orin/snapshot + mcap", "atomic": "P001 作业对象识别",
     "cond": "快照 age<5s", "endpoint": f"{RELAY}/cam/status"},
    {"id": "ecs_relay", "name": "ECS 中转", "icon": "📤", "stage": "上传",
     "topic": "api/relay/status", "atomic": "P002 数据上传",
     "cond": "包数>0 或 队列流转", "endpoint": f"{RELAY}/status"},
    {"id": "train_4060", "name": "4060 训练", "icon": "🧠", "stage": "训练",
     "topic": "loop_train.log", "atomic": "P003 ACT训练",
     "cond": "loss<1.6", "endpoint": "local:outputs/train/act_loop"},
    {"id": "model_url", "name": "模型静态URL", "icon": "📦", "stage": "集成",
     "topic": "models/act_cartesian", "atomic": "P004 模型打包",
     "cond": "HTTP 200", "endpoint": MODEL_URL},
    {"id": "orin_deploy", "name": "Orin 部署", "icon": "🚀", "stage": "部署",
     "topic": "orin/status.model", "atomic": "P005 模型部署",
     "cond": "model 更新且在线", "endpoint": f"{RELAY}/orin/status"},
    {"id": "orin_infer", "name": "Orin 推理", "icon": "⚡", "stage": "推理",
     "topic": "orin/status.infer_count", "atomic": "P006 动作执行",
     "cond": "infer_count>0", "endpoint": f"{RELAY}/orin/status"},
    {"id": "console", "name": "控制台", "icon": "🖥️", "stage": "监控",
     "topic": "Simulink/控制台", "atomic": "P007 闭环监控",
     "cond": "全节点在线", "endpoint": "local:studio.py"},
]

# 原子技能关联 (真实 DDS 技能类)
ATOMIC_MAP = {
    "采集": "P001 作业对象识别",
    "上传": "P007 数据采集与上传",
    "训练": "P003 ACT策略训练",
    "部署": "P005 模型部署",
    "推理": "P006 动作执行",
    "监控": "P008 闭环监控",
}


def http_json(url, timeout=8):
    try:
        import requests
        r = requests.get(url, timeout=timeout)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def probe_node(node):
    """探测单个节点真实状态 → (state, detail)"""
    ep = node["endpoint"]
    if ep.startswith("https://"):
        d = http_json(ep) if not ep.endswith(".safetensors") else _probe_model(ep)
        return _interpret(node, d)
    if ep.startswith("local:"):
        # 本地节点: 训练(读最近loss) / 控制台(常驻)
        if "act_loop" in ep:
            return _probe_train()
        return ("idle", "本地节点(控制台)")


def _probe_train():
    """读最近训练 loss + checkpoint"""
    try:
        log = "/home/xspace/lerobot-smolvla-lew/outputs/train/loop_train.log"
        import re
        txt = open(log, encoding="utf-8", errors="ignore").read()
        m = list(re.finditer(r"loss:([\d.]+)", txt))
        if m:
            loss = float(m[-1].group(1))
            state = "ok" if loss < 1.6 else "flow"
            return (state, f"最近loss={loss}")
        return ("idle", "无训练记录")
    except Exception:
        return ("idle", "训练log不可读")


def _probe_model(url):
    try:
        import requests
        r = requests.head(url, timeout=8)
        return {"http": r.status_code}
    except Exception:
        return None


def _interpret(node, d):
    """根据节点条件解释状态: ok/flow/idle/error"""
    if d is None:
        return ("error", "无法访问")
    sid = node["id"]
    if sid == "orin_collect":
        age = d.get("age_s", 99)
        return ("ok" if age < 5 else "idle", f"快照延迟{age}s")
    if sid == "ecs_relay":
        n = d.get("packages", 0)
        return ("flow" if n > 0 else "idle", f"队列{n}包")
    if sid == "model_url":
        return ("ok" if d.get("http") == 200 else "error", f"HTTP {d.get('http')}")
    if sid in ("orin_deploy", "orin_infer"):
        online = d.get("online", False)
        infer = d.get("infer_count", 0)
        if sid == "orin_deploy":
            return ("ok" if online else "error", f"在线:{online}")
        return ("flow" if infer > 0 else "idle", f"推理{infer}次")
    return ("idle", "?")


def ensure_schema(c):
    """水流表: 节点实时状态 + 时间序列"""
    c.execute("""CREATE TABLE IF NOT EXISTS dds_flow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT, node_id TEXT, node_name TEXT, stage TEXT,
        state TEXT, detail TEXT, flow_rate REAL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS dds_node_state (
        node_id TEXT PRIMARY KEY, node_name TEXT, stage TEXT,
        state TEXT, detail TEXT, updated TEXT)""")


def snapshot(db, c):
    """一次水流刷写: 探测所有节点 → 写状态 + 时间序列 (流水引用主数据ID)"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 主数据引用: 当前部署模型 (m_model)
    model_ref = "MD-ACT6D-v3"
    try:
        r = c.execute("SELECT model_id FROM m_model WHERE status='deployed' LIMIT 1").fetchone()
        if r:
            model_ref = r[0]
    except Exception:
        pass
    for node in NODES:
        state, detail = probe_node(node)
        # 原子技能关联
        atomic = ATOMIC_MAP.get(node["stage"], "")
        detail = f"{detail} · 技能:{atomic}" + (f" · 模型:{model_ref}" if node["stage"] == "推理" else "")
        # 写实时状态
        c.execute("""INSERT OR REPLACE INTO dds_node_state
            (node_id, node_name, stage, state, detail, updated)
            VALUES (?,?,?,?,?,?)""",
            (node["id"], node["name"], node["stage"], state, detail, now))
        # 写时间序列 (水流痕迹)
        rate = 1.0 if state in ("ok", "flow") else (0.5 if state == "idle" else 0.0)
        c.execute("""INSERT INTO dds_flow (ts, node_id, node_name, stage, state, detail, flow_rate)
            VALUES (?,?,?,?,?,?,?)""",
            (now, node["id"], node["name"], node["stage"], state, detail, rate))
    db.commit()


def main():
    once = "--once" in sys.argv
    db = sqlite3.connect(DDS_DB)
    c = db.cursor()
    ensure_schema(c)
    print("💧 水流式全局数据空间守护启动 (每10s刷写)")
    while True:
        try:
            snapshot(db, c)
            n = c.execute("SELECT COUNT(*) FROM dds_node_state").fetchone()[0]
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 💧 刷写 {n} 节点")
        except Exception as ex:
            print(f"⚠️ {ex}")
        if once:
            break
        time.sleep(10)


if __name__ == "__main__":
    main()
