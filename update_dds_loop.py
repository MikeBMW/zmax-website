#!/usr/bin/env python3
"""更新全局数据空间 dds.db — 以 2026-08-02 数据闭环全景为准
更新: pipeline(闭环5环节) / models(真机模型) / kpi(实测) / changelog
"""
import sqlite3

db = sqlite3.connect("/home/xspace/zmax-website/dds.db")
c = db.cursor()

# 1. pipeline: 边学边练闭环 (旧: 采集→转发→训练, 3步)
c.execute("DELETE FROM pipeline")
c.executemany(
    "INSERT INTO pipeline (step, name, node, duration, icon) VALUES (?,?,?,?,?)",
    [
        ("1", "采集", "Orin 真机", "20", "📡"),
        ("2", "上传", "ECS 中转", "5", "📤"),
        ("3", "训练", "4060 ACT", "150", "🧠"),
        ("4", "部署", "静态URL→Orin", "60", "🚀"),
        ("5", "推理", "Orin 6D", "0.5", "⚡"),
    ],
)

# 2. models: 补充真机 6D 模型 (v3)
c.execute("DELETE FROM models")
c.executemany(
    "INSERT INTO models (id, name, full_name, params, type, deployment, desc, color) VALUES (?,?,?,?,?,?,?,?)",
    [
        ("ACT", "ACT", "Action Chunking Transformer", "22M", "动作分块Transformer",
         "Sys1 (4060训练)", "真机6D关节模型 state6→action6 · 训练957帧 loss1.543 · 推理479ms", "#58a6ff"),
        ("ACT_6D", "ACT-6D", "真机6D关节模型 (闭环v3)", "22M", "关节空间ACT",
         "静态URL /models/act_cartesian", "采集→训练→部署→推理全自动闭环 · 957帧/24轨迹", "#00d4aa"),
        ("SmolVLA", "SmolVLA", "SmolVLA 视觉-语言-动作模型", "450M", "视觉-语言-动作",
         "Sys11 · Sys2", "端到端视觉-语言-动作。支持零样本泛化。", "#a371f7"),
        ("GR00T", "GR00T", "GR00T N1.7 通用机器人基础模型", "7B", "通用机器人基础模型",
         "Sys2", "NVIDIA GR00T N1.7-3B。DiT 1.09B。封装16种具身操作。", "#ff6b35"),
        ("VLA_T", "VLA-T", "VLA-T 触觉力控模型", "—", "视觉-语言-动作-触觉",
         "Sys21", "3D感知+力控+触觉编码器。", "#d4a800"),
    ],
)

# 3. kpi: 闭环实测指标
c.execute("DELETE FROM kpi")
c.executemany(
    "INSERT INTO kpi (id, value, unit, label, icon) VALUES (?,?,?,?,?)",
    [
        ("precision", "±0.02", "mm", "重复定位精度", "🎯"),
        ("yield_rate", ">99", "%", "关键工序良率", "✅"),
        ("infer_lat", "479", "ms", "真机推理延迟 (v2实测)", "⚡"),
        ("loop_cycle", "<5", "min", "数据闭环周期 (采集→部署)", "🔄"),
        ("cycle_time", "<15", "s", "单次插拔节拍", "⏱️"),
    ],
)

# 4. changelog: 记录本次更新 (字段级审计)
for tbl, note in [("pipeline", "边学边练闭环5环节"), ("models", "真机6D模型ACT_6D"), ("kpi", "实测推理479ms/闭环<5min")]:
    c.execute("INSERT INTO changelog (ts, table_name, key_name, field_name, old_value, new_value) VALUES (datetime('now','localtime'), ?, 'v4.0', '数据闭环全景', NULL, ?)",
              (tbl, note))

db.commit()
print("✅ dds.db 更新完成")
for t in ["pipeline", "models", "kpi"]:
    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {n} 行")
db.close()
