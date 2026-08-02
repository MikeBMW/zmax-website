#!/usr/bin/env python3
"""落地主数据表 + 种子数据 (Master Data v1.0)
运行: python3 init_master_data.py
"""
import sqlite3, json

db = sqlite3.connect("/home/xspace/zmax-website/dds.db")
c = db.cursor()

# ── M1 工件主数据 ──
c.execute("""CREATE TABLE IF NOT EXISTS m_workpiece (
    wp_id TEXT PRIMARY KEY, name TEXT, material TEXT, size_mm TEXT,
    insert_force_N REAL, pick_points TEXT, tolerance_mm REAL, note TEXT)""")
c.executemany("INSERT OR REPLACE INTO m_workpiece VALUES (?,?,?,?,?,?,?,?)", [
    ("WP-SR5-100G", "100G QSFP28 光模块", "铜合金+PCBA", "18.35×8.5×18.35",
     4.5, json.dumps([[0.0,0.0,0.0,0,0,0]]), 0.02, "主推型号"),
    ("WP-SR5-400G", "400G QSFP-DD 光模块", "铜合金+PCBA", "18.35×8.5×22.58",
     5.0, json.dumps([[0.0,0.0,0.0,0,0,0]]), 0.02, "高密度"),
    ("WP-LD-1310", "1310nm 激光二极管", "InP芯片+TO封装", "φ5.6×3.5",
     0.5, json.dumps([[0.0,0.0,0.0,0,0,0]]), 0.01, "光芯片"),
])

# ── M2 设备主数据 ──
c.execute("""CREATE TABLE IF NOT EXISTS m_equipment (
    eq_id TEXT PRIMARY KEY, type TEXT, model TEXT, dof INT,
    joint_names TEXT, control_topics TEXT, calib TEXT, note TEXT)""")
c.executemany("INSERT OR REPLACE INTO m_equipment VALUES (?,?,?,?,?,?,?,?)", [
    ("EQ-ROKAE-SR5", "6轴机械臂", "珞石SR5-C", 6,
     json.dumps(["joint_1","joint_2","joint_3","joint_4","joint_5","joint_6"]),
     json.dumps(["/sim_joint_trajectory", "/robot/tcp_pose", "/execute_external_task"]),
     json.dumps({"tcp_offset_mm":[0,0,120]}), "主臂"),
    ("EQ-GRIPPER-DH", "夹爪", "DH-3 电爪", 1,
     json.dumps(["gripper"]), json.dumps(["/gripper/cmd"]),
     json.dumps({"stroke_mm":20,"force_N":20}), "插拔夹持"),
    ("EQ-CAM-D405", "RGB-D相机", "Intel RealSense D405", 0,
     json.dumps([]), json.dumps(["/cam/color", "/cam/depth"]),
     json.dumps({"eye":"hand","fov":85}), "视觉定位"),
    ("EQ-ORIN", "边缘计算", "Orin NX 16GB", 0,
     json.dumps([]), json.dumps(["/orin/infer"]),
     json.dumps({"gpu":"Ampere 1024CUDA"}), "推理部署"),
])

# ── M3 工位主数据 ──
c.execute("""CREATE TABLE IF NOT EXISTS m_station (
    st_id TEXT PRIMARY KEY, name TEXT, zone TEXT, layout TEXT, tasks TEXT, note TEXT)""")
c.executemany("INSERT OR REPLACE INTO m_station VALUES (?,?,?,?,?,?)", [
    ("ST-LOAD-1", "入料工位", "z1", json.dumps({"tray":4,"slot":32}),
     json.dumps(["扫码","取料"]), "Z700F 5工位循环"),
    ("ST-PLUG-3", "插拔工位", "z2", json.dumps({"fixture":1,"slot":8}),
     json.dumps(["插入","拔出"]), "核心精细操作"),
    ("ST-AOI-6", "AOI检测", "z3", json.dumps({"camera":1,"stage":2}),
     json.dumps(["AOI检测","缺陷判定"]), "全状态展示"),
    ("ST-OUT-12", "出料包装", "z4", json.dumps({"tray":2}),
     json.dumps(["放置","包装"]), "末端工位"),
])

# ── M4 工艺/动作主数据 ──
c.execute("""CREATE TABLE IF NOT EXISTS m_process (
    act_id TEXT PRIMARY KEY, label TEXT, action_dim INT, target TEXT,
    cond TEXT, atomic_skill TEXT, note TEXT)""")
c.executemany("INSERT OR REPLACE INTO m_process VALUES (?,?,?,?,?,?,?)", [
    ("ACT-RELEASE", "暂时松开", 6, "夹爪开度100%", "插入完成信号", "P006", "夹爪释放"),
    ("ACT-MOVE-SLOT", "移动到治具插槽", 6, "末端至插槽位姿", "扫码通过", "P006", "平移定位"),
    ("ACT-WAIT-TEST", "等待测试结果", 6, "保持当前位姿", "AOI结果", "P007", "等待判定"),
    ("ACT-SCAN", "扫码", 6, "相机对准条码", "入料到位", "P001", "条码读取"),
    ("ACT-PICK", "取料", 6, "夹持工件", "料盘就位", "P002", "抓取"),
    ("ACT-INSERT", "插入", 6, "插入到位(力控)", "位姿对准", "P006", "精细插拔"),
])

# ── M5 模型主数据 ──
c.execute("""CREATE TABLE IF NOT EXISTS m_model (
    model_id TEXT PRIMARY KEY, name TEXT, state_dim INT, action_dim INT,
    train_frames INT, loss REAL, infer_ms INT, url TEXT, status TEXT, note TEXT)""")
c.executemany("INSERT OR REPLACE INTO m_model VALUES (?,?,?,?,?,?,?,?,?,?)", [
    ("MD-ACT6D-v3", "ACT-6D 真机关节模型", 6, 6, 957, 1.543, 479,
     "https://datadrive.world/models/act_cartesian.safetensors", "deployed",
     "2026-08-02 闭环v3 · 24轨迹"),
    ("MD-ACT-CART-v1", "ACT 笛卡尔模型", 3, 4, 500, 1.555, 1051,
     "https://datadrive.world/models/act_cartesian.safetensors", "retired",
     "v1 笛卡尔接口"),
    ("MD-SMOLVLA", "SmolVLA-500M", 6, 6, 0, 0, 0, "", "planned", "认知层"),
])

db.commit()
print("✅ 主数据表落地 (m_workpiece/m_equipment/m_station/m_process/m_model)")
for t in ["m_workpiece", "m_equipment", "m_station", "m_process", "m_model"]:
    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {n} 行")
db.close()
