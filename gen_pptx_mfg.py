#!/usr/bin/env python3
"""Z-MAX PPT — 全站DDS数据驱动 · 正文10页"""
import sqlite3, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

TEMPLATE = '/www/wwwroot/datadrive.world/uploads/data/智蜂具身机器人产品规划和宣传页_v1.1_0422.pptx'
OUT = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx'

GREEN = RGBColor(0x00, 0xd4, 0xaa); WHITE = RGBColor(0xff, 0xff, 0xff)
GRAY = RGBColor(0x8b, 0x94, 0x9e); DARK = RGBColor(0x06, 0x08, 0x0d)
BLUE = RGBColor(0x58, 0xa6, 0xff); ORANGE = RGBColor(0xf0, 0xa5, 0x00)
PURPLE = RGBColor(0xa3, 0x71, 0xf7); CARD_BG = RGBColor(0x0d, 0x11, 0x17)

def bg(s): s.background.fill.solid(); s.background.fill.fore_color.rgb = DARK

def tt(slide, text, top=Inches(0.3), sz=Pt(26), clr=WHITE):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = sz; p.font.bold = True; p.font.color.rgb = clr

def sub(slide, text, top, sz=Pt(12), clr=GRAY):
    tb = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.size = sz; p.font.color.rgb = clr

def card(slide, l, t, w, h, title, desc, tc=GREEN):
    sh = slide.shapes.add_shape(1, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = CARD_BG; sh.line.fill.background()
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(10); tf.margin_right = Pt(10); tf.margin_top = Pt(8)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = tc
    p2 = tf.add_paragraph(); p2.text = desc
    p2.font.size = Pt(10); p2.font.color.rgb = GRAY; p2.space_before = Pt(6)

def load():
    db = sqlite3.connect('/www/wwwroot/datadrive.world/dds.db'); db.row_factory = sqlite3.Row
    d = {}
    d['c'] = {r['key']: r['value'] for r in db.execute('SELECT key,value FROM company')}
    d['kpi'] = {r['id']: dict(r) for r in db.execute('SELECT * FROM kpi')}
    d['robots'] = [dict(r) for r in db.execute('SELECT * FROM robots ORDER BY id')]
    d['roadmap'] = [dict(r) for r in db.execute('SELECT * FROM roadmap ORDER BY version')]
    d['zones'] = [dict(r) for r in db.execute('SELECT * FROM factory_zones ORDER BY id')]
    d['pipe'] = [dict(r) for r in db.execute('SELECT * FROM pipeline ORDER BY step')]
    d['skill_total'] = db.execute('SELECT COUNT(*) FROM atomic_skills').fetchone()[0]
    d['skill_cats'] = {}
    for r in db.execute('SELECT category, COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC'):
        d['skill_cats'][r['category']] = r['cnt']
    db.close()
    return d

# Use template dimensions
tmpl = Presentation(TEMPLATE)
prs = Presentation()
prs.slide_width = tmpl.slide_width
prs.slide_height = tmpl.slide_height

D = load(); c = D['c']
def ns(): return prs.slides.add_slide(prs.slide_layouts[6])

# === S1: Cover ===
sl = ns(); bg(sl)
tt(sl, 'Z700 光模块精密制造', Inches(2), Pt(36), GREEN)
sub(sl, '具身智能机器人系统 · 立项申请书', Inches(3), Pt(20))
sub(sl, f'{c.get("name","智蜂创元")} · datadrive.world', Inches(4), Pt(14))
sub(sl, '掌握智能，蜂动未来', Inches(5), Pt(13), GRAY)

# === S2: KPI ===
sl = ns(); bg(sl)
tt(sl, '一、核心性能指标')
for i, (k, icon) in enumerate([('precision','🎯'),('yield','✅'),('takt','⏱️'),('force','⚡')]):
    v = D['kpi'].get(k, {})
    x = Inches(0.8 + i * 3.15)
    sh = sl.shapes.add_shape(9, x, Inches(2.2), Inches(3), Inches(3))
    sh.fill.solid(); sh.fill.fore_color.rgb = CARD_BG
    sh.line.color.rgb = GREEN; sh.line.width = Pt(2)
    tf = sh.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = f'{icon}\n{v.get("value","")}{v.get("unit","")}'
    p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = v.get('label',''); p2.font.size = Pt(12)
    p2.font.color.rgb = WHITE; p2.alignment = PP_ALIGN.CENTER
sub(sl, 'FW Loading · 微米级定位+柔性力控 · 检验精密操作能力的试金石', Inches(6), Pt(11), GRAY)

# === S3: Products ===
sl = ns(); bg(sl)
tt(sl, '二、Z700 产品系列 · L2→L4 软件定义进化')
for i, bot in enumerate(D['robots']):
    card(sl, Inches(0.8), Inches(1.5 + i * 1.4), Inches(11.7), Inches(1.2),
         f'{bot["icon"]} {bot["name"]} [{bot["level_label"]}]', bot['desc'], [BLUE,GREEN,PURPLE,ORANGE][i%4])

# === S4: Architecture ===
sl = ns(); bg(sl)
tt(sl, '三、创元 XWorld · 全技能智能体平台')
for i, (t, d, col) in enumerate([
    ('🧠 XAgent 大脑', '全技能智能体 · 统一指挥调度 · 安全高效自主交互', GREEN),
    ('📊 XData 数据', '全模态数据 · 人机料法环贯通 · 数据基石', BLUE),
    ('🤖 XRobot 机器人', '垂域模型+强健肢体 · 感驱控一体 · 精准执行', ORANGE),
]):
    card(sl, Inches(0.8), Inches(1.5 + i * 1.9), Inches(11.7), Inches(1.6), t, d, col)
sub(sl, f'{D["skill_total"]} 项原子技能 · {len(D["skill_cats"])} 大类 · DDS全局数据驱动', Inches(6.8), Pt(11), GRAY)

# === S5: Pipeline ===
sl = ns(); bg(sl)
tt(sl, '四、端到端流水线')
for i, p in enumerate(D['pipe']):
    card(sl, Inches(0.8 + i * 4.2), Inches(1.5), Inches(3.8), Inches(4.5),
         f'{p.get("icon","")} {p.get("name","")}', p.get('desc',''), [GREEN,BLUE,ORANGE][i%3])

# === S6: Factory ===
sl = ns(); bg(sl)
tt(sl, '五、目标工厂 · 800G DR8 光模块产线')
for i, z in enumerate(D['zones']):
    card(sl, Inches(0.8 + (i%2)*6.2), Inches(1.5 + (i//2)*2.8), Inches(5.8), Inches(2.5),
         z['name'], f'{z["stations"]} ({z["count"]}站)', [BLUE,ORANGE,GREEN,PURPLE][i%4])

# === S7: Roadmap ===
sl = ns(); bg(sl)
tt(sl, '六、开发路线图 · 2026→2028')
for i, r in enumerate(D['roadmap']):
    card(sl, Inches(0.8 + i*4.2), Inches(1.5), Inches(3.8), Inches(4.0),
         f'{r["name"]} · {r["timeline"]}', r['desc'], [BLUE,GREEN,PURPLE][i%3])
for i in range(2):
    tb = sl.shapes.add_textbox(Inches(4.2 + i*4.2), Inches(3.2), Inches(0.5), Inches(0.5))
    p = tb.text_frame.paragraphs[0]; p.text = '→'; p.font.size = Pt(28); p.font.color.rgb = GREEN

# === S8: Skills ===
sl = ns(); bg(sl)
tt(sl, f'七、原子技能库 · {D["skill_total"]} 项 · {len(D["skill_cats"])} 大类')
for i, (cat, cnt) in enumerate(D['skill_cats'].items()):
    col = i % 3; row = i // 3
    card(sl, Inches(0.8 + col*4.2), Inches(1.5 + row*2.0), Inches(3.8), Inches(1.7),
         cat, f'{cnt} 条', [GREEN,BLUE,ORANGE,PURPLE][col%4])

# === S9: Team ===
sl = ns(); bg(sl)
tt(sl, '八、项目团队与立项总结')
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
     f'数据资产: DDS全局 · 63页面 · {D["skill_total"]}项原子技能', GREEN)
sub(sl, 'datadrive.world/kanban.html · 看板驱动项目管理', Inches(7), Pt(11), GRAY)

# === S10: Thanks ===
sl = ns(); bg(sl)
tt(sl, '谢 谢', Inches(2.5), Pt(44), GREEN)
sub(sl, f'{c.get("name","智蜂创元")} · datadrive.world', Inches(3.5), Pt(16))
sub(sl, '掌握智能，蜂动未来', Inches(4.2), Pt(14), GRAY)

prs.save(OUT)
print(f'✅ {OUT} ({os.path.getsize(OUT)} bytes) · 10 slides · {D["skill_total"]} skills')
