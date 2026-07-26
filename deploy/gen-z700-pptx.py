#!/usr/bin/env python3
"""Generate Z700 analysis PPTX"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
C = RGBColor(0x00, 0xD4, 0xAA)
DARK = RGBColor(0x06, 0x08, 0x0D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x8B, 0x94, 0x9E)
BLUE = RGBColor(0x58, 0xA6, 0xFF)
GOLD = RGBColor(0xD4, 0xA8, 0x00)

def add_slide(title, lines):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background; bg.fill.solid(); bg.fill.fore_color.rgb = DARK
    tx = slide.shapes.add_textbox(Inches(.5), Inches(.3), Inches(12), Inches(.8))
    tf = tx.text_frame; p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = C
    tx2 = slide.shapes.add_textbox(Inches(.5), Inches(1.3), Inches(12), Inches(5.5))
    tf2 = tx2.text_frame; tf2.word_wrap = True
    for i, line in enumerate(lines):
        p2 = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p2.text = line; p2.font.size = Pt(16); p2.font.color.rgb = GRAY
        p2.space_after = Pt(4)

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg = slide.background; bg.fill.solid(); bg.fill.fore_color.rgb = DARK
tx = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
tf = tx.text_frame
p = tf.paragraphs[0]; p.text = "Z700 轮式双臂 · 精品分析报告"
p.font.size = Pt(42); p.font.bold = True; p.font.color.rgb = C; p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph(); p2.text = "光模块精密制造 · 具身智能旗舰 · 对比它石智航 TARS"
p2.font.size = Pt(18); p2.font.color.rgb = GRAY; p2.alignment = PP_ALIGN.CENTER
p3 = tf.add_paragraph(); p3.text = "智蜂创元 (苏州) × 它石智航 TARS (上海) · 2026"
p3.font.size = Pt(14); p3.font.color.rgb = GRAY; p3.alignment = PP_ALIGN.CENTER; p3.space_before = Pt(20)

# Slide 2: KPI
add_slide("核心性能指标", [
    "🎯 ±0.02mm 重复定位精度    ✅ >99% 关键工序良率    ⚡ >10kHz 力控闭环带宽",
    "⏱ <15s 单次插拔节拍    🤚 ≤0.1N 接触力控制    🏋 >50kg 双臂负载",
    "",
    "Z700 轮式双臂精密操作机器人 — L4 旗舰级",
    "轮式底盘AMR自主导航 + 双臂6轴×2协同操作 + 8+传感器融合 + 力控闭环>10kHz"
])

# Slide 3: Architecture
add_slide("产品架构", [
    "🔵 感知系统: 2D/3D视觉 · 六维力/力矩 · 触觉阵列 · 结构光 · 激光雷达 · 编码器 · IMU",
    "   → 原子技能 P001-P015 感知定位 (15项)",
    "",
    "🟢 操作执行: 双臂协同 · 精密夹爪/真空 · 力位混合控制 · 柔顺装配 · 自适应抓取",
    "   → 原子技能 A001-A015 操作执行 (15项)",
    "",
    "🟡 智能决策: 任务规划 · 路径优化 · 异常检测 · 自恢复 · 多机调度 · MES集成",
    "   → 原子技能 L001-L008 学习泛化 (8项)",
    "",
    "🟣 力控安全: 碰撞检测 · 力控闭环 · 急停 · 区域监控 · 安全互锁",
    "   → 原子技能 S001-S010 安全集成 (10项)"
])

# Slide 4: Five Scenarios
add_slide("五大应用场景", [
    "1. FW固件烧录 — 下载FW · SN识别 — 扫码→烧录→校验→追溯 — 节拍≤15s — Phase1 ✅",
    "2. 上下料 — COC上料 · BI上下料 · 贴片备料 — 识别→取件→放置→满空交换 — 零损伤 — Phase1 ✅",
    "3. 老化箱插拔 — COC BI-01 · 模块BI · DA烘烤 — 定位→插入→力控→锁止 — 力≤0.1N — Phase1 ✅",
    "4. 热海柜操作 — TCT温变 · 热岛立柜 — 开柜→取放→关柜→监控 — ±0.05mm — Phase2 🔶",
    "5. ATS自动测试 — MPD测试 · OE测试 · OE/TRX — 装夹→插拔→测试→分Bin — ≥99%良率 — Phase2 🔶"
])

# Slide 5: TARS Comparison
add_slide("它石智航 TARS 对标分析", [
    "智蜂创元(苏州) × 它石智航 TARS(上海) · 一期10台(5自研Z700+5台TARS) · 1000万预算 · 白盒交付",
    "",
    "力控精度:   Z700 ≤0.1N/10kHz    vs    TARS ≤0.5N/1kHz    → Z700领先 5×",
    "重复定位:   Z700 ±0.02mm        vs    TARS ±0.05mm      → Z700领先 2.5×",
    "插拔节拍:   Z700 <15s/次        vs    TARS 20-30s/次    → Z700快 1.5-2×",
    "自主导航:   Z700 AMR多工位自由  vs    TARS 需轨道/固定   → Z700独有优势",
    "双臂协同:   Z700 原生双臂       vs    TARS 单臂为主      → Z700架构优势",
    "交付模式:   Z700 白盒全栈       vs    TARS 黑盒SDK       → Z700战略优势",
    "部署周期:   Z700 2-4周/工站     vs    TARS 4-8周/工站    → Z700更快"
])

# Slide 6: SWOT
add_slide("SWOT 分析", [
    "💪 优势 S: 光模块深度定制 · 89原子技能全产线覆盖 · 力控闭环>10kHz · 白盒交付获全栈能力 · 苏州产业集群",
    "",
    "⚠️ 劣势 W: 品牌知名度低于它石/珞石 · 量产成熟度待Phase1验证 · 供应链外部依赖 · 单行业聚焦",
    "",
    "🚀 机会 O: 光模块800G/1.6T升级 · AI算力驱动产能扩张 · 机器换人政策红利 · 白盒可复制半导体/汽车电子",
    "",
    "🔻 威胁 T: 它石可能自研光模块方案 · 成熟厂商向下整合 · 行业周期波动 · 人才竞争 · 价格战风险"
])

# Slide 7: Atomic Skills
add_slide("89项原子技能 × 光模块全产线覆盖", [
    "感知定位 15项 (P001-P015): 对象识别 · 位姿估计 · 缺陷检测 · 视觉伺服 · 条码/OCR · 3D点云 · 尺寸测量",
    "操作执行 15项 (A001-A015): 精密夹取 · 力控插入 · 柔顺装配 · 螺丝锁付 · 点胶涂覆 · 焊接 · 贴装",
    "装配工艺 15项 (P056-P070): COC共晶 · WB打线 · UV固化 · 耦合对准 · 分板切割 · COC绑定 · 探针测试 · 组装",
    "质量检测 10项 (Q001-Q010): 目检 · AOI检测 · 3D测量 · GR&R · 缺陷分类 · 追溯报告",
    "安全集成 10项 (S001-S010): 碰撞检测 · 力控闭环 · 急停 · 区域监控 · 安全互锁",
    "载具物流 9项 (H001-H009): 载具识别 · 工站接驳 · 满空交换 · 槽位追溯 · 异常恢复",
    "学习泛化 8项 (L001-L008): 技能迁移 · 自校准 · 少样本学习 · 多模态指令理解",
    "移动导航 7项 (M001-M007): SLAM · 路径规划 · 动态避障 · 工站精准对接"
])

# Slide 8: Roadmap
add_slide("交付路线图", [
    "Phase 1 (2026.07 — 2026.11): 首批样机 + POC验证",
    "  Z700: 5台 · FW烧录/上下料/老化箱插拔",
    "  TARS: 5台 · 同步部署",
    "  验收: 插拔成功率 ≥99%",
    "",
    "Phase 2 (2026.12 — 2027.04): 全线部署 + 产线联调",
    "  Z700: 热海柜操作 + ATS自动测试 + 全线串联",
    "  TARS: 补充优化",
    "  验收: 全工站节拍达标",
    "",
    "Phase 3 (2027.05+): 规模复制 + 行业扩展",
    "  跨行业复制: 3C电子 / 汽车电子 / 半导体",
    "  TARS: 评估续约",
    "  验收: ROI验证"
])

# Slide 9: Business Value
add_slide("商业价值", [
    "人工效率提升: 3-5×",
    "",
    "连续运行: 24/7 不间断生产",
    "",
    "投资回收期: <12个月",
    "",
    "单台覆盖: 5-8个工站",
    "",
    "年化节省: 3-5名熟练操作工 × 24/7 = 等效15-25人",
    "",
    "",
    "Z-MAX · 智蜂创元 (苏州) × 它石智航 TARS (上海)",
    "datadrive.world · 2026"
])

out = '/www/wwwroot/datadrive.world/api/z700-analysis.pptx'
prs.save(out)
print(f"PPTX saved: {out}")
