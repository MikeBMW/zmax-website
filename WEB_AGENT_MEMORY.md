# Web Agent 全状态存档 · 2026-07-20 · 迁移至 4060

## 一、三工程版本
| 工程 | 仓库 | 分支 | 最新 commit | 版本号 |
|------|------|------|------|------|
| web工程 | zmax-website | main | 0379777 | v2.5.3 |
| GUI工程 | lerobot-smolvla-lew | web | 574991bf | - |
| PIPE工程 | zmax-data-pipeline | main | e6a5df5 | v2.5 |

## 二、ComfyUI 前端 (comfyui.html)
- 自动检测采集: forwarded_mb 变化 → 采集, 30s无变化 → 待机
- 磁盘自适应: <1MB显示KB, >=1MB显示MB
- Sys 0 数据集: 双击→📂查看→名称+大小+落盘时间(CST)
- 清理功能: 🗑只保留最新3个
- 数据路径: /root/datasets/mcab/
- 绿框高亮: canvas draw() 直接绘制, 插入在 ctx.stroke() 之后
- 连接按钮: fetch /api/comfy/status → 绿框+红绿灯
- 状态栏: 红绿灯圆点 4090常绿 MAC/Orin 随心跳变
- MAC计数: 📦包数 + 转发MB
- 4090存储: 💾XXMB/KB
- Orin状态: 🟢采集/⚪待机/🔴离线
- 侧栏去重: 硬件/X-Hybrid/Orin部署 已去重
- 系统节点: Sys0-Sys22 只显示编号无模型名
- 动作分组: A00-A10带🎬静态标签
- 版本显示: v2.5.3 · 2026-07-19 21:20

## 三、后端 (comfyui_backend.py) — 4090:50054
- 心跳: POST /api/mac/heartbeat (forwarded_mb 兼容 orin内部+顶层)
- 状态: GET /status (包含 orin_recording, forwarded_mb, disk_gb)
- 数据集: GET /datasets-list (兼容 /api/comfy/datasets-list)
- 清理: GET /cleanup-old (保留最新3个)
- 上传: POST /upload (multipart, dest=/root/datasets/mcab/)
- 磁盘: get_disk_gb() 实时扫描 mcab
- 时区: CST(+8h)
- WebSocket: 已禁用(阻塞修复)
- AUTO_TRAIN: 改用 list[0] 防遮蔽
- glob: __import__("glob") 防变量遮蔽
- 隧道: ECS 39.102.211.79:50053 ←SSH→ 4090:50054

## 四、训练脚本 (4090)
- train_h_jepa.py — H-JEPA 训练 (适配Orin数据NHWC→NCHW+resize, state pad 6→7)
- h_jepa_zflow.py — ZFlow_VLA 三层潜空间
- jepa_encoder.py / jepa_predictor.py — JEPA组件
- z_config.py — 配置类
- train_compare.py — 三架构对比 (A/B/C)
- train_peg.py / train_door.py — per-task训练
- train_only_v2.py — 无MuJoCo纯训练版
- 数据: /root/datasets/compare/reach_expert.npz, peg_expert.npz, door_expert.npz, sweep_expert.npz
- 模型: /root/models/compare/*.pt, /root/models/hjepa_zflow/model.pt

## 五、三架构对比结论
| 架构 | params | door收敛 | 特点 |
|------|------|------|------|
| A 纯VLA | ~1.2M | 13ep/0.0010 | 基线 |
| B +LeWM | ~1.5M | 11ep/0.0007 | 精度最优 |
| C +ZFlow | ~2.2M | 4ep/0.0008 | 收敛最快 |

## 六、ASPICE V-Model (aspice-vmodel.html)
- SYS.6 系统验收 (top, 🟠智蜂R)
- SYS.5 系统合格性测试 (🟢联合)
- SYS.4 系统集成测试 (🟠智蜂R)
- SWE.6 软件集成测试 (🟢联合)
- SWE.5 软件合格性测试 (🔵它石R)
- SWE.4 软件单元测试 (🔵它石R)
- 硬件验收测试 (bottom, 🟠智蜂R)
- 左侧: SWE.1(SWE.1→软件应用分析,🟠智蜂R), SWE.2, SWE.3

## 七、部署方式
- ECS: 39.102.211.79, nginx → /www/wwwroot/datadrive.world/
- scp推送: sshpass -p "Nix19789" scp file root@39.102.211.79:/www/wwwroot/datadrive.world/
- 后端启动: cd /root/lerobot-smolvla-lew && python3.12 comfyui_backend.py
- 隧道: sshpass -p "Nix19789" ssh -N -R 50053:localhost:50054 root@39.102.211.79

## 八、关键约束
- 禁止修改 draw() 核心渲染(var c=colors...ctx.fillStyle='#111'...ctx.strokeStyle=c)
- 默认预设: setTimeout(function(){rz();preset("smolvla");},800)
- 所有改动先 git checkout 回退→Python统一改→node -e 验证JS→grep -c 确认preset→部署
- PIPE工程由@Hermes小芳维护
- 小改: commit+push main不打tag || 中改: 三工程同步tag+Release Note
