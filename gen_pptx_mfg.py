#!/usr/bin/env python3
"""Z-MAX PPT — 使用智蜂模板布局 · 全站DDS数据 · 正文+附录"""
import sqlite3, os, shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

TEMPLATE = '/www/wwwroot/datadrive.world/uploads/data/智蜂具身机器人产品规划和宣传页_v1.1_0422.pptx'
OUT = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx'

GREEN = RGBColor(0x00, 0xd4, 0xaa); WHITE = RGBColor(0xff, 0xff, 0xff)
GRAY = RGBColor(0x8b, 0x94, 0x9e); BLUE = RGBColor(0x58, 0xa6, 0xff)
ORANGE = RGBColor(0xf0, 0xa5, 0x00); PURPLE = RGBColor(0xa3, 0x71, 0xf7)

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

# Use template as base
shutil.copy(TEMPLATE, OUT)
prs = Presentation(OUT)

BODY = prs.slide_layouts[1]  # 正文页 3-column layout

def tmpl_cover(title_text, subtitle):
    sl = prs.slides.add_slide(prs.slide_layouts[0])
    sh = sl.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(1))
    p = sh.text_frame.paragraphs[0]; p.text = title_text
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    sh2 = sl.shapes.add_textbox(Inches(1), Inches(3.5), Inches(11), Inches(0.8))
    p2 = sh2.text_frame.paragraphs[0]; p2.text = subtitle
    p2.font.size = Pt(20); p2.font.color.rgb = WHITE; p2.alignment = PP_ALIGN.CENTER
    sh3 = sl.shapes.add_textbox(Inches(1), Inches(5), Inches(11), Inches(0.5))
    p3 = sh3.text_frame.paragraphs[0]; p3.text = f'{c.get("name","智蜂创元")} · datadrive.world'
    p3.font.size = Pt(14); p3.font.color.rgb = GRAY; p3.alignment = PP_ALIGN.CENTER
    return sl

def tmpl_slide(title):
    sl = prs.slides.add_slide(BODY)
    # Use the title placeholder (placeholder idx 0 = CENTER_TITLE)
    for ph in sl.placeholders:
        if ph.placeholder_format.type == 3:  # CENTER_TITLE
            ph.text = title
            break
    return sl

def card(sl, l, t, w, h, title, desc, tc=GREEN):
    sh = sl.shapes.add_shape(1, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0x0d, 0x11, 0x17)
    sh.line.fill.background()
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(10); tf.margin_right = Pt(10); tf.margin_top = Pt(8)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = tc
    p2 = tf.add_paragraph(); p2.text = desc
    p2.font.size = Pt(10); p2.font.color.rgb = GRAY; p2.space_before = Pt(6)

# Brand template slides
for sl in prs.slides:
    for sh in sl.shapes:
        tf = getattr(sh, 'text_frame', None)
        if tf:
            for p in tf.paragraphs:
                for run in p.runs:
                    if 'ReinBee' in run.text: run.text = run.text.replace('ReinBee', c.get('name','智蜂创元'))
                    if '© ReinBee All Rights Reserved.' in run.text: run.text = run.text.replace('© ReinBee All Rights Reserved.', f'© {c.get("name","智蜂创元")} All Rights Reserved.')

# === Cover ===
tmpl_cover('Z700 光模块精密制造', '具身智能机器人系统 · 立项申请书')

# === KPI ===
sl = tmpl_slide('一、核心性能指标')
for i, (k, icon) in enumerate([('precision','🎯'),('yield','✅'),('takt','⏱️'),('force','⚡')]):
    v = D['kpi'].get(k, {})
    x = Inches(0.8 + i * 3.15)
    sh = sl.shapes.add_shape(9, x, Inches(2.2), Inches(3), Inches(3))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0x0d, 0x11, 0x17)
    sh.line.color.rgb = GREEN; sh.line.width = Pt(2)
    tf = sh.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = f'{icon}\n{v.get("value","")}{v.get("unit","")}'
    p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = v.get('label',''); p2.font.size = Pt(12)
    p2.font.color.rgb = WHITE; p2.alignment = PP_ALIGN.CENTER

# === Products ===
sl = tmpl_slide('二、Z700 产品系列 · L2→L4 软件定义进化')
for i, bot in enumerate(D['robots']):
    card(sl, Inches(0.8), Inches(1.4 + i * 1.4), Inches(11.7), Inches(1.2),
         f'{bot["icon"]} {bot["name"]} [{bot["level_label"]}]', bot['desc'], [BLUE,GREEN,PURPLE,ORANGE][i%4])

# === Architecture ===
sl = tmpl_slide('三、创元 XWorld · 全技能智能体平台')
for i, (t, d, col) in enumerate([
    ('🧠 XAgent 大脑', '全技能智能体 · 统一指挥调度 · 安全高效自主交互', GREEN),
    ('📊 XData 数据', '全模态数据 · 人机料法环贯通 · 数据基石', BLUE),
    ('🤖 XRobot 机器人', '垂域模型+强健肢体 · 感驱控一体 · 精准执行', ORANGE),
]):
    card(sl, Inches(0.8), Inches(1.4 + i * 1.9), Inches(11.7), Inches(1.6), t, d, col)

# === Pipeline ===
sl = tmpl_slide('四、端到端流水线')
for i, p in enumerate(D['pipe']):
    card(sl, Inches(0.8 + i * 4.2), Inches(1.5), Inches(3.8), Inches(4.5),
         f'{p.get("icon","")} {p.get("name","")}', p.get('desc',''), [GREEN,BLUE,ORANGE][i%3])

# === Factory ===
sl = tmpl_slide('五、目标工厂 · 800G DR8 光模块产线')
for i, z in enumerate(D['zones']):
    card(sl, Inches(0.8 + (i%2)*6.2), Inches(1.5 + (i//2)*2.8), Inches(5.8), Inches(2.5),
         z['name'], f'{z["stations"]} ({z["count"]}站)', [BLUE,ORANGE,GREEN,PURPLE][i%4])

# === Roadmap ===
sl = tmpl_slide('六、开发路线图 · 2026→2028')
for i, r in enumerate(D['roadmap']):
    card(sl, Inches(0.8 + i*4.2), Inches(1.5), Inches(3.8), Inches(4.0),
         f'{r["name"]} · {r["timeline"]}', r['desc'], [BLUE,GREEN,PURPLE][i%3])

# === Skills ===
sl = tmpl_slide(f'七、原子技能库 · {D["st"]} 项 · {len(D["sc"])} 大类')
for i, (cat, cnt) in enumerate(D['sc'].items()):
    col = i % 3; row = i // 3
    card(sl, Inches(0.8 + col*4.2), Inches(1.5 + row*2.0), Inches(3.8), Inches(1.7),
         cat, f'{cnt} 条', [GREEN,BLUE,ORANGE,PURPLE][col%4])

# === Team ===
sl = tmpl_slide('八、项目团队与立项总结')
for i, (name, role, col) in enumerate([
    ('xspace 总工', 'Sys架构 · GUI引擎 · Orin部署 · 18项 88%', BLUE),
    ('web PM/前端', 'Sys2训练 · Web全站 · 仿真 · 18项 94%', GREEN),
    ('小芳 硬件', 'Orin采集 · MAC转发 · 硬件测试 · 14项 78%', PURPLE),
]):
    card(sl, Inches(0.8 + i*4.2), Inches(1.5), Inches(3.8), Inches(2.0), name, role, col)
card(sl, Inches(0.8), Inches(3.8), Inches(11.7), Inches(2.8), '立项总结',
     '技术领先: 视触觉混合动作模型 · 端到端感知决策控制 · >1kHz力控\n'
     '市场刚需: AI算力驱动光模块扩产 · 精密制造人工替代\n'
     '团队完备: 三人全栈 · 50项88%完成 · 零阻塞\n'
     f'数据资产: DDS全局 · 63页面 · {D["st"]}项原子技能', GREEN)

# === Thanks ===
sl = tmpl_slide('谢 谢')
sh = sl.shapes.add_textbox(Inches(3), Inches(3), Inches(7), Inches(1))
p = sh.text_frame.paragraphs[0]; p.text = f'{c.get("name","智蜂创元")} · datadrive.world'
p.font.size = Pt(16); p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER

prs.save(OUT)
print(f'✅ {OUT} ({os.path.getsize(OUT)} bytes) · {len(prs.slides)} slides · {D["st"]} skills')
print(f'   正文 10页 + 附录 {len(prs.slides)-10}页 · 使用{os.path.basename(TEMPLATE)}')
