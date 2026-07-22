# Web Agent 全状态存档 · 2026-07-22

## 当前版本
- Web工程: v2.5.4
- ECS: 39.102.211.79 (HTTPS已启用)
- 仓库: github.com/MikeBMW/zmax-website (main)

## 核心页面
| 页面 | 功能 |
|------|------|
| comfyui.html | v2.5.4 · VLA-T改名+主页入口+侧栏去重 |
| chat.html | 飞书通知桥+已读回执+@all推送 |
| factory-3d.html | 四区工厂3D·4机器人+4AGV·坐标系统 |
| scenario-oe.html | 2D产线场景·工艺卡·SVG |
| dds-3d-space.html | 54条件×48动作×29工位 3D映射 |
| kanban.html | 任务看板·三人三线 |

## 坐标系（factory-3d）
- 场地: 36×24
- 原点: 左下角(0,0)
- X→ 右正, Y↑ 上正
- 4区: COC(4-18,Y18-24) OE(19-33,Y18-24) MOD(19-33,Y0-6) WH(4-18,Y0-6)

## 飞书桥
- chat.html → forum.php → notify.php → 飞书 dataworld 群
- 每条消息自动推送飞书
- HTTPS证书: Let's Encrypt, 自动续期

## Git状态
- 未push (缺GitHub token)
- 所有改动已在本地commit

## 待办
- [ ] 配GitHub token实现push
- [ ] 4060隧道待xspace建立
- [ ] 大版本升级v3.0待评审
