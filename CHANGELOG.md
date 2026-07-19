# Z-MAX 统一变更日志 · Unified CHANGELOG

## v3.9 (2026-07-19)

### zmax-website @web
- ✅ 专业工程UI升级：品牌顶栏+侧栏重设计+工作流面板
- ✅ Ctrl+滚轮世界坐标缩放
- ✅ 📊 仪表盘实时流水线状态
- ✅ 🔗 硬件连接检测+绿色边框
- ✅ 三阶段流水线：Orin采集→MAC转发→4090训练
- ✅ 版本号+日期显示在工具栏

### lerobot-smolvla-lew @web
- ✅ HTTP心跳端点 POST /api/mac/heartbeat
- ✅ 命令通道 PENDING_COMMAND 机制
- ✅ 自动训练触发 + 磁盘清理
- ✅ Nginx上传限制500MB
- ✅ WebSocket端点备用 (50056)

### lerobot-smolvla-lew @xspace
- ✅ H-JEPA ZFlow v3.1 模型 (2.68M)
- ✅ train_h_jepa.py 训练脚本
- ✅ MetaWorld 数据加载器
- ✅ W&B 集成 + 自动上传

### zmax-data-pipeline @Hermes小芳
- ✅ MAC守护服务 心跳轮询
- ✅ Orin网关 数据采集控制
- ✅ 健康检查脚本

### 协同规则
- 所有commit格式: `[版本] 说明 · 日期时间`
- 推送前运行 `sync_all.sh` 同步三库
- Release Notes 与 CHANGELOG 保持同步
- 每个版本打 tag: `vX.Y-YYYYMMDD`
