#!/usr/bin/env python3
"""Z-MAX PPT生成器 — 基于智蜂模板 · 替换DDS数据"""
import sqlite3, os, shutil
from pptx import Presentation

TEMPLATE = '/www/wwwroot/datadrive.world/uploads/data/智蜂具身机器人产品规划和宣传页_v1.1_0422.pptx'
OUT = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx'

def load_dds():
    db = sqlite3.connect('/www/wwwroot/datadrive.world/dds.db'); db.row_factory = sqlite3.Row
    d = {}
    d['company'] = {r['key']: r['value'] for r in db.execute('SELECT key,value FROM company')}
    d['kpi'] = {r['id']: dict(r) for r in db.execute('SELECT * FROM kpi')}
    d['robots'] = [dict(r) for r in db.execute('SELECT * FROM robots')]
    d['total_skills'] = db.execute('SELECT COUNT(*) FROM atomic_skills').fetchone()[0]
    db.close()
    return d

def replace_text(obj, old, new):
    """Replace text in all paragraphs of a shape or cell"""
    tf = getattr(obj, 'text_frame', None)
    if tf is None: return 0
    count = 0
    for p in tf.paragraphs:
        if old in p.text:
            for run in p.runs:
                if old in run.text:
                    run.text = run.text.replace(old, new)
                    count += 1
    return count

def replace_all(prs, old, new):
    """Replace text across all slides"""
    count = 0
    for sl in prs.slides:
        for shape in sl.shapes:
            count += replace_text(shape, old, new)
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        count += replace_text(cell, old, new)
    return count

# Copy template
shutil.copy(TEMPLATE, OUT)
prs = Presentation(OUT)
D = load_dds()
c = D['company']

# Slide 1: Brand
replace_all(prs, 'ReinBee', c.get('name', '智蜂创元'))
replace_all(prs, '© ReinBee All Rights Reserved.', f'© {c.get("name","智蜂创元")} All Rights Reserved.')

# Inject skill count
n = replace_all(prs, '开启工厂全技能智能体新时代',
    f'开启工厂全技能智能体新时代 · 已构建{D["total_skills"]}项原子技能')

# Update spec values from DDS
kpi = D['kpi']
for k, v in kpi.items():
    if v.get('label') == '定位精度':
        replace_all(prs, '±0.05mm+0.05N', f'{v["value"]}mm+{v.get("unit","0.05N")}')
    if v.get('label') == '力控带宽':
        replace_all(prs, '0.05N', '>1kHz')

prs.save(OUT)
replaced = replace_all(prs, '__', '__')  # dummy to count
print(f'✅ Template PPTX: {OUT} ({os.path.getsize(OUT)} bytes) · {len(prs.slides)} slides · {D["total_skills"]} skills')

# Verify key text
for i, sl in enumerate(prs.slides):
    for shape in sl.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.paragraphs[0].text.strip()
            if t and len(t) > 10:
                print(f'  S{i+1}: {t[:60]}')
                break
