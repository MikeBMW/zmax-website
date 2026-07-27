#!/usr/bin/env python3
"""Z-MAX 立项PPT生成器 — 按智蜂模板风格 · 从DDS数据库读取"""
import sqlite3, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

DB = '/www/wwwroot/datadrive.world/dds.db'
OUT = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx'

GREEN = RGBColor(0x00, 0xd4, 0xaa)
WHITE = RGBColor(0xff, 0xff, 0xff)
GRAY = RGBColor(0x8b, 0x94, 0x9e)
DARK = RGBColor(0x06, 0x08, 0x0d)
CARD_BG = RGBColor(0x0d, 0x11, 0x17)
BLUE = RGBColor(0x58, 0xa6, 0xff)
ORANGE = RGBColor(0xf0, 0xa5, 0x00)
PURPLE = RGBColor(0xa3, 0x71, 0xf7)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def bg(slide, color=DARK):
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb = color

def title_box(slide, text, top=Inches(0.3), size=Pt(28), color=WHITE):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = size; p.font.bold = True; p.font.color.rgb = color

def sub_box(slide, text, top, size=Pt(13), color=GRAY):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = size; p.font.color.rgb = color

def card(slide, left, top, w, h, title, desc, title_color=GREEN):
    shape = slide.shapes.add_shape(1, left, top, w, h)  # rectangle
    shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
    shape.line.fill.background()
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(10); tf.margin_right = Pt(10); tf.margin_top = Pt(8)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = title_color
    p2 = tf.add_paragraph(); p2.text = desc
    p2.font.size = Pt(10); p2.font.color.rgb = GRAY; p2.space_before = Pt(6)
    return shape

def load_db():
    db = sqlite3.connect(DB); db.row_factory = sqlite3.Row
    data = {}
    data['company'] = {r['key']: r['value'] for r in db.execute('SELECT key,value FROM company')}
    data['kpi'] = {r['id']: dict(r) for r in db.execute('SELECT * FROM kpi')}
    data['robots'] = [dict(r) for r in db.execute('SELECT * FROM robots')]
    data['roadmap'] = [dict(r) for r in db.execute('SELECT * FROM roadmap')]
    data['zones'] = [dict(r) for r in db.execute('SELECT * FROM factory_zones')]
    data['systems'] = {r['id']: dict(r) for r in db.execute('SELECT * FROM systems')}
    data['pipeline'] = [dict(r) for r in db.execute('SELECT * FROM pipeline ORDER BY step')]
    
    # Atomic skills stats
    cats = {}
    for r in db.execute('SELECT category, COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC'):
        cats[r['category']] = r['cnt']
    data['skill_cats'] = cats
    data['skill_total'] = sum(cats.values())
    db.close()
    return data

D = load_db()
c = D['company']

# ========== SLIDE 1: 封面 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '掌握智能，蜂动未来', Inches(2.5), Pt(40), GREEN)
sub_box(sl, 'Rein Intelligence · Bee the Future', Inches(3.3), Pt(18), GRAY)
sub_box(sl, f'{c.get("name","智蜂创元")} · Z-MAX 具身智能机器人系统', Inches(4.2), Pt(14))
sub_box(sl, '立 项 申 请 书', Inches(4.8), Pt(16), GREEN)
sub_box(sl, f'© {c.get("name","智蜂创元")} All Rights Reserved.', Inches(6.5), Pt(10), GRAY)

# ========== SLIDE 2: 目录 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '目 录', Inches(0.5))
items = ['1. 项目概述与核心指标', '2. 产品规划路线图', '3. 创元 XWorld 平台架构', 
         '4. Z 系列场景与能力', '5. 技术规格', '6. 精密操作能力', 
         '7. 模型演进路线', '8. 团队与项目管理', '9. 立项总结']
for i, item in enumerate(items):
    sub_box(sl, item, Inches(1.5 + i * 0.55), Pt(16), WHITE if i < 2 else GRAY)
sub_box(sl, f'© {c.get("name","智蜂创元")} All Rights Reserved.', Inches(6.5), Pt(10), GRAY)

# ========== SLIDE 3: KPI 核心指标 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '一、核心性能指标 · 极致性能的量化标准')
sub_box(sl, '检验机器人精细操作能力的"试金石"', Inches(1.0), Pt(12), GRAY)

kpi_data = D['kpi']
kpi_items = [
    ('precision', '🎯'), ('yield', '✅'), ('takt', '⏱️'), ('force', '⚡')
]
x_positions = [Inches(1.5), Inches(4.5), Inches(7.5), Inches(10.5)]
for (k, icon), x in zip(kpi_items, x_positions):
    v = kpi_data.get(k, {})
    # KPI circle
    shape = sl.shapes.add_shape(9, x, Inches(2), Inches(2.5), Inches(2.5))  # oval
    shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(0x0d, 0x1a, 0x2a)
    shape.line.color.rgb = GREEN; shape.line.width = Pt(2)
    tf = shape.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = f'{icon}\n{v.get("value","")}{v.get("unit","")}'
    p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = v.get('label',''); p2.font.size = Pt(13)
    p2.font.color.rgb = WHITE; p2.alignment = PP_ALIGN.CENTER

sub_box(sl, 'FW Loading（固件加载）与电口/光口插拔 — 微米级定位 + 柔性力控 + >99% 成功率', Inches(5.8), Pt(12), GRAY)

# ========== SLIDE 4: 产品规划 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '二、智蜂通用具身机器人产品规划')
sub_box(sl, '同一套智能引擎，L2 到 L4 软件定义进化', Inches(1.0), Pt(12), GRAY)

bots = D['robots']
for i, bot in enumerate(bots):
    y = Inches(1.6 + i * 1.35)
    colors = [BLUE, GREEN, PURPLE, ORANGE]
    card(sl, Inches(0.8), y, Inches(11.7), Inches(1.2),
         f'{bot["icon"]} {bot["name"]} [{bot["level_label"]}]',
         bot['desc'], colors[i % 4])

# ========== SLIDE 5: XWorld 架构 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '三、创元 XWorld · 开启工厂全技能智能体新时代')

arch_items = [
    ('🧠 创元·大脑 XAgent', '面向工厂的全技能智能体。统一指挥，安全高效自主交互与操作。'),
    ('📊 创元·数据 XData', '垂直场景的全模态数据。贯通人机料法环全要素工艺数据。'),
    ('🤖 创元·机器人 XRobot', '垂域模型+强健肢体。感驱控一体，快速低时延精准执行。'),
]
for i, (title, desc) in enumerate(arch_items):
    card(sl, Inches(0.8), Inches(1.6 + i * 1.8), Inches(11.7), Inches(1.5), title, desc,
         [GREEN, BLUE, ORANGE][i])

# Show skill stats
skill_line = f'89条原子技能 · {len(D["skill_cats"])}大类: ' + ' · '.join(f'{k}({v})' for k,v in list(D['skill_cats'].items())[:5])
sub_box(sl, skill_line, Inches(6.8), Pt(11), GRAY)

# ========== SLIDE 6: Z系列场景 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '四、智蜂 Z 系列 · 工厂新物种')

scenes = [
    ('A · 搬运上下料', '线边仓/产线分拣/搬运/上下料。视觉+触觉+听觉多模态感知。Z100L。', BLUE),
    ('B · 精密操作', '电口/光口插拔。±0.05mm定位。亚毫米级精密装配。Z700F/Z700。', GREEN),
    ('C · 质量检测巡检', '机器人协同AOI检测。光学+激光+AI。设备盘点/规范巡检。Z700F+AOI。', PURPLE),
    ('D · 柔性无人工厂', '端边云协同。分段+端到端+世界模型。工厂Agents协同。Z700Plus。', ORANGE),
]
for i, (title, desc, color) in enumerate(scenes):
    card(sl, Inches(0.8 + (i % 2) * 6.2), Inches(1.5 + (i // 2) * 2.8),
         Inches(5.8), Inches(2.5), title, desc, color)

# ========== SLIDE 7: 路线图 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '五、开发路线图 · 2026→2028')

roadmap = D['roadmap']
phase_colors = [BLUE, GREEN, PURPLE]
for i, r in enumerate(roadmap):
    x = Inches(0.8 + i * 4.2)
    card(sl, x, Inches(1.5), Inches(3.8), Inches(3.5),
         f'{r["name"]} · {r["timeline"]}',
         r['desc'], phase_colors[i % 3])

# Timeline arrow
for i in range(2):
    arrow = sl.shapes.add_textbox(Inches(4.2 + i * 4.2), Inches(3.0), Inches(0.5), Inches(0.5))
    p = arrow.text_frame.paragraphs[0]; p.text = '→'
    p.font.size = Pt(28); p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER

# ========== SLIDE 8: 规格 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '六、Z700 技术规格')

specs = [
    ('最高身高', '~1700mm'), ('臂展', '~1542mm'), ('单臂臂长', '~696mm'),
    ('整机重量', '≤185kg'), ('单臂负载', '≤5kg'), ('双臂负载', '≤10kg'),
    ('洁净度', 'Class 10000 (ISO 7)'), ('防护等级', 'IP42 / 手臂 IP50'),
    ('定位精度', '±0.05mm (Z700F) / ±0.02mm (Z700Plus)'),
    ('力控精度', '0.05N (Z700F) / 0.03N (Z700Plus)'),
    ('操作成功率', '>99%'), ('UPH', '<12s'),
]

for i, (k, v) in enumerate(specs):
    col = i % 3; row = i // 3
    x = Inches(0.8 + col * 4.2)
    y = Inches(1.3 + row * 0.85)
    tb = sl.shapes.add_textbox(x, y, Inches(4.0), Inches(0.75))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = k
    p.font.size = Pt(10); p.font.color.rgb = GRAY
    p2 = tf.add_paragraph(); p2.text = v
    p2.font.size = Pt(13); p2.font.bold = True; p2.font.color.rgb = WHITE

# ========== SLIDE 9: 精密操作 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '七、精密操作能力 · 在"针尖上跳舞"')

ops = [
    ('01 取料', '3D视觉识别抓取。高精度3D视觉引导，识别微小零件位姿，无损伤抓取。'),
    ('02 过站', '高速动态路径调整。实时调整路径，确保运动节拍与精度双重达标。'),
    ('03 上料插入', '微米级精准力控。精准对位+柔性力控，接口无偏移无损伤精准插入。'),
    ('04 机台拔出', '平稳分离防损伤。匀速拔出，避免冲击损坏精密电路接口。'),
    ('05 下料', '高效运动保节拍。最优轨迹快速完成下料，满足整线高节拍要求。'),
    ('06 分检', '智能视觉分拣。读取状态码，良品与不良品分拣至不同区域，全流程闭环。'),
]
for i, (title, desc) in enumerate(ops):
    col = i % 3; row = i // 3
    card(sl, Inches(0.8 + col * 4.2), Inches(1.3 + row * 2.9),
         Inches(3.8), Inches(2.6), title, desc, GREEN)

# ========== SLIDE 10: 模型演进 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '八、创元具身模型演进路线')

stages = [
    ('第一阶段：分段式', '「分而治之」流水线控制', 'YOLO+CuRobo', BLUE),
    ('第二阶段：端到端', '「数据驱动」单模型闭环', 'ACT / SmolVLA', GREEN),
    ('第三阶段：VLA一体化', '「语义驱动」多模态智能体', 'π₀ / GR00T', PURPLE),
    ('第四阶段：世界模型', '「感知-想象-行动」闭环', '潜空间预测+视触觉融合', ORANGE),
]
for i, (title, desc, model, color) in enumerate(stages):
    x = Inches(0.8 + i * 3.2)
    card(sl, x, Inches(1.5), Inches(2.9), Inches(4.0),
         title, f'{desc}\n\n代表：{model}', color)

# ========== SLIDE 11: 团队 + 总结 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '九、项目团队与立项总结')

team_data = [
    ('xspace 总工', 'Sys架构·GUI引擎·Orin部署', '18项·88%完成', BLUE),
    ('web PM/前端', 'Sys2训练·Web全站·仿真验证', '18项·94%完成', GREEN),
    ('小芳 硬件', 'Orin采集·MAC转发·硬件测试', '14项·78%完成', PURPLE),
]
for i, (name, role, stat, color) in enumerate(team_data):
    card(sl, Inches(0.8 + i * 4.2), Inches(1.5), Inches(3.8), Inches(2.0),
         name, f'{role}\n\n{stat}', color)

# Summary
summary = '技术先进性：视触觉混合动作模型、端到端感知决策控制、>1kHz力控闭环。\n市场紧迫性：AI算力爆发驱动光模块扩产，精密制造人工替代刚需。\n团队完备性：三人核心团队覆盖全栈，模型+硬件+部署闭环。\n总进度：50项任务·44完成(88%)·4进行中·零阻塞。'
card(sl, Inches(0.8), Inches(3.8), Inches(11.7), Inches(2.8), '立项总结', summary, GREEN)

# ========== SLIDE 12: 谢谢 ==========
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
title_box(sl, '谢 谢', Inches(2.8), Pt(48), GREEN)
sub_box(sl, f'{c.get("name","智蜂创元")} · datadrive.world', Inches(4.0), Pt(16))
sub_box(sl, '掌握智能，蜂动未来', Inches(4.6), Pt(14), GRAY)

prs.save(OUT)
print(f'✅ PPTX generated: {OUT} ({os.path.getsize(OUT)} bytes) · 12 slides')
