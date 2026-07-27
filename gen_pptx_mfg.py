#!/usr/bin/env python3
"""Z-MAX PPT — 智蜂模板 · DDS全站数据 · 高对比度文字"""
import sqlite3, os, shutil
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

TEMPLATE = '/www/wwwroot/datadrive.world/uploads/data/智蜂具身机器人产品规划和宣传页_v1.1_0422.pptx'
OUT = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx'

# High-contrast palette: dark bg + bright text
GREEN = RGBColor(0x00, 0xff, 0xaa)
WHITE = RGBColor(0xff, 0xff, 0xff)
GRAY = RGBColor(0xc0, 0xc8, 0xd4)
DARK = RGBColor(0x04, 0x06, 0x0a)

def load():
    db = sqlite3.connect('/www/wwwroot/datadrive.world/dds.db'); db.row_factory = sqlite3.Row
    d = {}
    d['c'] = {r['key']: r['value'] for r in db.execute('SELECT key,value FROM company')}
    d['kpi'] = {r['id']: dict(r) for r in db.execute('SELECT * FROM kpi')}
    d['robots'] = [dict(r) for r in db.execute('SELECT * FROM robots ORDER BY id')]
    d['roadmap'] = [dict(r) for r in db.execute('SELECT * FROM roadmap ORDER BY version')]
    d['zones'] = [dict(r) for r in db.execute('SELECT * FROM factory_zones ORDER BY id')]
    d['pipe'] = [dict(r) for r in db.execute('SELECT * FROM pipeline ORDER BY step')]
    d['st'] = db.execute('SELECT COUNT(*) FROM atomic_skills').fetchone()[0]
    d['sc'] = {}
    for r in db.execute('SELECT category, COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC'):
        d['sc'][r['category']] = r['cnt']
    db.close()
    return d

D = load(); c = D['c']

shutil.copy(TEMPLATE, OUT)
prs = Presentation(OUT)

def bg(s): s.background.fill.solid(); s.background.fill.fore_color.rgb = DARK

def title(slide, text, top=Inches(0.4), sz=Pt(30)):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.9))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = sz; p.font.bold = True; p.font.color.rgb = WHITE

def sub(slide, text, top, sz=Pt(14)):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = sz; p.font.color.rgb = GRAY

def box(slide, l, t, w, h, title, desc, tc=GREEN):
    sh = slide.shapes.add_shape(1, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0x0a, 0x0e, 0x14)
    sh.line.color.rgb = GREEN; sh.line.width = Pt(1)
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(12); tf.margin_right = Pt(12); tf.margin_top = Pt(10)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = tc
    p2 = tf.add_paragraph(); p2.text = desc
    p2.font.size = Pt(12); p2.font.color.rgb = GRAY; p2.space_before = Pt(8)

# Brand template slides
for sl in prs.slides:
    for sh in sl.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for run in p.runs:
                    if 'ReinBee' in run.text: run.text = run.text.replace('ReinBee', c.get('name','智蜂创元'))
                    if '© ReinBee' in run.text: run.text = run.text.replace('© ReinBee All Rights Reserved.', f'© {c.get("name","智蜂创元")} All Rights Reserved.')
        if sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    for p in cell.text_frame.paragraphs:
                        for run in p.runs:
                            if 'ReinBee' in run.text: run.text = run.text.replace('ReinBee', c.get('name','智蜂创元'))

BODY_LAYOUT = prs.slide_layouts[1]  # template's content layout
COVER_LAYOUT = prs.slide_layouts[0]  # template's title layout
BLANK_LAYOUT = BODY_LAYOUT  # fallback

def ns():
    return prs.slides.add_slide(BLANK_LAYOUT)

# === S1 Cover ===
sl = ns(); bg(sl)
title(sl, 'Z700 光模块精密制造', Inches(2), Pt(40))
sub(sl, '具身智能机器人系统 · 立项申请书', Inches(3.2), Pt(22))
sub(sl, f'{c.get("name","智蜂创元")} · datadrive.world', Inches(4.2), Pt(16))
sub(sl, '掌握智能，蜂动未来', Inches(5.2), Pt(14))

# === S2 KPI ===
sl = ns(); bg(sl)
title(sl, '一、核心性能指标')
kpi_items = [('precision','🎯'),('yield','✅'),('takt','⏱️'),('force','⚡')]
for i, (k, icon) in enumerate(kpi_items):
    v = D['kpi'].get(k, {})
    x = Inches(0.8 + i * 3.15)
    sh = sl.shapes.add_shape(9, x, Inches(2), Inches(3), Inches(3))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0x0a, 0x0e, 0x14)
    sh.line.color.rgb = GREEN; sh.line.width = Pt(2)
    tf = sh.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = f'{icon}\n{v.get("value","")}{v.get("unit","")}'
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = v.get('label',''); p2.font.size = Pt(14)
    p2.font.color.rgb = WHITE; p2.alignment = PP_ALIGN.CENTER
sub(sl, 'FW Loading · 微米级定位+柔性力控 · 精密操作试金石', Inches(5.8), Pt(12))

# === S3 Products ===
sl = ns(); bg(sl)
title(sl, '二、Z700 产品系列 · L2→L4 软件定义进化')
colors = [GREEN, WHITE, GREEN, WHITE]
for i, bot in enumerate(D['robots']):
    box(sl, Inches(0.8), Inches(1.4 + i * 1.4), Inches(11.7), Inches(1.2),
        f'{bot["icon"]} {bot["name"]} [{bot["level_label"]}]', bot['desc'], GREEN)

# === S4 Architecture ===
sl = ns(); bg(sl)
title(sl, '三、创元 XWorld · 全技能智能体平台')
items = [
    ('🧠 XAgent 大脑', '全技能智能体 · 统一指挥调度 · 安全高效自主交互'),
    ('📊 XData 数据', '全模态数据 · 人机料法环贯通 · 数据基石'),
    ('🤖 XRobot 机器人', '垂域模型+强健肢体 · 感驱控一体 · 精准执行'),
]
for i, (t, d) in enumerate(items):
    box(sl, Inches(0.8), Inches(1.4 + i * 1.8), Inches(11.7), Inches(1.5), t, d, GREEN)
sub(sl, f'{D["st"]} 项原子技能 · {len(D["sc"])} 大类 · DDS全局数据驱动', Inches(6.8), Pt(12))

# === S5 Pipeline ===
sl = ns(); bg(sl)
title(sl, '四、端到端流水线')
for i, p in enumerate(D['pipe']):
    box(sl, Inches(0.8 + i * 4.2), Inches(1.5), Inches(3.8), Inches(4.5),
        f'{p.get("icon","")} {p.get("name","")}', p.get('desc',''), GREEN)

# === S6 Factory ===
sl = ns(); bg(sl)
title(sl, '五、目标工厂 · 800G DR8 光模块产线')
for i, z in enumerate(D['zones']):
    box(sl, Inches(0.8 + (i%2)*6.2), Inches(1.5 + (i//2)*2.8), Inches(5.8), Inches(2.5),
        z['name'], f'{z["stations"]} ({z["count"]}站)', GREEN)

# === S7 Roadmap ===
sl = ns(); bg(sl)
title(sl, '六、开发路线图 · 2026→2028')
for i, r in enumerate(D['roadmap']):
    box(sl, Inches(0.8 + i*4.2), Inches(1.5), Inches(3.8), Inches(4.5),
        f'{r["name"]} · {r["timeline"]}', r['desc'], GREEN)

# === S8 Skills ===
sl = ns(); bg(sl)
title(sl, f'七、原子技能库 · {D["st"]} 项 · {len(D["sc"])} 大类')
for i, (cat, cnt) in enumerate(D['sc'].items()):
    col = i % 3; row = i // 3
    box(sl, Inches(0.8 + col*4.2), Inches(1.5 + row*2.0), Inches(3.8), Inches(1.7),
        cat, f'{cnt} 条原子技能', GREEN)

# === S9 Team ===
sl = ns(); bg(sl)
title(sl, '八、项目团队与立项总结')
team = [
    ('xspace 总工', 'Sys架构 · GUI引擎 · Orin部署 · 18项 88%'),
    ('web PM/前端', 'Sys2训练 · Web全站 · 仿真 · 18项 94%'),
    ('小芳 硬件', 'Orin采集 · MAC转发 · 硬件测试 · 14项 78%'),
]
for i, (name, role) in enumerate(team):
    box(sl, Inches(0.8 + i*4.2), Inches(1.5), Inches(3.8), Inches(2.2), name, role, GREEN)
box(sl, Inches(0.8), Inches(4), Inches(11.7), Inches(2.5), '立项总结',
    '技术领先: 视触觉混合动作模型 · 端到端感知决策控制 · >1kHz力控闭环\n'
    '市场刚需: AI算力驱动光模块扩产 · 精密制造人工替代\n'
    '团队完备: 三人全栈 · 50项88%完成 · 零阻塞 · kanban驱动\n'
    f'数据资产: DDS全局数据空间 · 63页面 · {D["st"]}项原子技能', GREEN)

# === S10 Thanks ===
sl = ns(); bg(sl)
title(sl, '谢 谢', Inches(3), Pt(44))
sub(sl, f'{c.get("name","智蜂创元")} · datadrive.world', Inches(4.5), Pt(18))
sub(sl, '掌握智能，蜂动未来', Inches(5.2), Pt(14))

prs.save(OUT)
sz = os.path.getsize(OUT)
print(f'✅ {OUT} ({sz} bytes) · {len(prs.slides)} slides · {D["st"]} skills')
print(f'   正文 10页 · 模板附录 11页 · 深色背景高对比')
