# Z-MAX 具身智能主数据空间设计 (Master Data Space v1.0)

> 2026-08-02 · 工厂精细操作场景 · 与水流式动态数据(dds_flow)分层

---

## 1. 设计原则：主数据 vs 流水数据

```
┌────────────────────────────────────────────────────────────┐
│  主数据 (Master Data) = 稳定权威层 · 变化慢 · 全链路引用      │
│  ── 工件/设备/工位/工艺/模型/技能 的"字典与台账"              │
│  = 单点事实来源 (Single Source of Truth)                    │
├────────────────────────────────────────────────────────────┤
│  流水数据 (Flow Data) = 动态实时层 · 变化快 · 引用主数据ID    │
│  ── 节点状态/推理计数/队列包数/loss 曲线/时间序列              │
│  = 水流刷写 (waterflow_dds.py 每10s)                        │
└────────────────────────────────────────────────────────────┘
```

**核心：流水数据只存"引用主数据的ID + 实时值"，不复制主数据内容** → 数据一致、无冗余、可追溯。

---

## 2. 主数据分类 (工厂精细操作场景)

### M1. 工件主数据 (Workpiece)
| 字段 | 说明 | 示例 |
|---|---|---|
| wp_id | 工件编码 | WP-SR5-100G |
| name | 名称 | 100G QSFP28 光模块 |
| material | 材质 | 铜合金+PCBA |
| size_mm | 尺寸 | 18.35×8.5×18.35 |
| insert_force_N | 插拔力规格 | 4.5±0.5N |
| pick_points | 取放点(坐标系) | [[x,y,z,rx,ry,rz]×N] |
| tolerance_mm | 精度要求 | ±0.02 |

### M2. 设备主数据 (Equipment)
| 字段 | 说明 | 示例 |
|---|---|---|
| eq_id | 设备编码 | EQ-ROKAE-SR5 |
| type | 类型 | 6轴机械臂/夹爪/相机/Orin |
| model | 型号 | 珞石SR5-C |
| dof | 自由度 | 6 (或夹爪1) |
| joint_names | 关节名 | joint_1..joint_6 |
| control_topics | ROS2 topics | /sim_joint_trajectory, /robot/tcp_pose |
| calib | 标定参数 | TCP偏移/相机外参 |

### M3. 工位主数据 (Station)
| 字段 | 说明 | 示例 |
|---|---|---|
| st_id | 工位编码 | ST-AOI-6 |
| name | 名称 | AOI检测工位 |
| zone | 区域 | factory_zones |
| layout | 工装布局 | 治具插槽坐标/料盘位 |
| tasks | 任务集 | 扫码/插拔/AOI |

### M4. 工艺/动作主数据 (Process-Action)
| 字段 | 说明 | 示例 |
|---|---|---|
| act_id | 动作编码 | ACT-RELEASE |
| label | 动作标签(统一) | 暂时松开 |
| action_dim | 动作维度 | 6D 关节增量 |
| target | 目标状态 | 夹爪开度/末端位姿 |
| cond | 触发条件 | 插入完成信号 |
| atomic_skill | 关联原子技能 | P006 动作执行 |

### M5. 模型主数据 (Model)
| 字段 | 说明 | 示例 |
|---|---|---|
| model_id | 模型编码 | MD-ACT6D-v3 |
| name | 名称 | ACT-6D 真机关节模型 |
| state_dim | 状态维度 | 6 |
| action_dim | 动作维度 | 6 |
| train_frames | 训练帧数 | 957 |
| loss | 训练loss | 1.543 |
| infer_ms | 推理延迟 | 479 |
| url | 静态URL | /models/act_cartesian.safetensors |
| status | 状态 | deployed/retired |

### M6. 原子技能主数据 (Atomic Skill) — 已有242条
见 `atomic_skills` 表 (P001-P242, 11大类)

---

## 3. 数据空间分层架构

```
                     ┌─────────────────────────┐
                     │   主数据 (Master Data)   │
                     │  m_workpiece/m_equipment │
                     │  m_station/m_process     │
                     │  m_model/m_skill         │
                     └───────────┬─────────────┘
                                 │ 引用ID
        ┌───────────────┬────────┴───────┬───────────────┐
        ▼               ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 采集流       │ │ 训练流       │ │ 部署流       │ │ 推理流       │
│ dds_flow    │ │ dds_flow    │ │ dds_flow    │ │ dds_flow    │
│ (Orin快照)   │ │ (loss曲线)  │ │ (URL状态)   │ │ (infer计数) │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 4. 落地实现

### 4.1 主数据表 (新)
```sql
CREATE TABLE m_workpiece (wp_id TEXT PK, name TEXT, material TEXT, size_mm TEXT,
                          insert_force_N REAL, pick_points TEXT, tolerance_mm REAL);
CREATE TABLE m_equipment (eq_id TEXT PK, type TEXT, model TEXT, dof INT,
                          joint_names TEXT, control_topics TEXT, calib TEXT);
CREATE TABLE m_station   (st_id TEXT PK, name TEXT, zone TEXT, layout TEXT, tasks TEXT);
CREATE TABLE m_process   (act_id TEXT PK, label TEXT, action_dim INT, target TEXT,
                          cond TEXT, atomic_skill TEXT);
CREATE TABLE m_model     (model_id TEXT PK, name TEXT, state_dim INT, action_dim INT,
                          train_frames INT, loss REAL, infer_ms INT, url TEXT, status TEXT);
```

### 4.2 流水数据引用
```sql
-- 推理流 (引用主数据)
INSERT INTO dds_flow (ts, node_id, node_name, stage, state, detail, flow_rate)
VALUES (now, 'orin_infer', 'Orin推理', '推理',
        'flow', 'MD-ACT6D-v3 · 推理5次 · 479ms', 1.0);
-- 主数据变化才更新 m_model, 流水只记引用
```

### 4.3 刷写策略 (水流)
1. **主数据**：变化时更新（版本升级/新增设备/新增工位）
2. **流水数据**：每10s刷写（节点状态/推理/队列）
3. **条件触发**：流水数据满足条件 → 更新主数据状态（如 infer>0 → m_model.status=deployed）

---

## 5. 优良性评估
| 维度 | 设计 |
|---|---|
| 单一事实 | 主数据唯一，流水只引用ID |
| 一致性 | 无冗余复制，改动一处全局生效 |
| 可追溯 | dds_flow 时间序列 = 完整水流痕迹 |
| 可扩展 | 新增主数据类/流水节点即插即用 |
| 性能 | 主数据小表常驻内存，流水只增 |
