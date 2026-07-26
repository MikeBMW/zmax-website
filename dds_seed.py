#!/usr/bin/env python3
"""DDS 数据库初始化 — 从 dds-global.js 提取数据写入 SQLite"""
import sqlite3, json, re, os

DB_PATH = '/www/wwwroot/datadrive.world/dds.db'

# 读取 DDS JS 文件，提取 JSON 数据
with open('/www/wwwroot/datadrive.world/dds-global.js') as f:
    js = f.read()

# 提取 window.DDS = {...} 中间的 JSON
m = re.search(r'window\.DDS\s*=\s*(\{.*?\n\});', js, re.DOTALL)
if not m:
    raise ValueError("Cannot find DDS object in JS")

dds_raw = m.group(1)

# 用 node 解析 JS 对象为 JSON
import subprocess
node_script = f"""
const dds = {dds_raw};
console.log(JSON.stringify(dds, null, 2));
"""
result = subprocess.run(['node', '-e', node_script], capture_output=True, text=True)
if result.returncode != 0:
    raise RuntimeError(f"Node parse failed: {result.stderr}")

dds = json.loads(result.stdout)

# ── 创建数据库 ──
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 公司
c.execute('''CREATE TABLE IF NOT EXISTS company (
    key TEXT PRIMARY KEY, value TEXT
)''')
for k, v in dds['company'].items():
    c.execute('INSERT OR REPLACE INTO company VALUES(?,?)', (k, str(v)))

# KPI
c.execute('''CREATE TABLE IF NOT EXISTS kpi (
    id TEXT PRIMARY KEY, value TEXT, unit TEXT, label TEXT, icon TEXT
)''')
for k, v in dds['kpi'].items():
    c.execute('INSERT OR REPLACE INTO kpi VALUES(?,?,?,?,?)',
              (k, v['value'], v['unit'], v['label'], v.get('icon','')))

# 机器人
c.execute('''CREATE TABLE IF NOT EXISTS robots (
    id TEXT PRIMARY KEY, name TEXT, level TEXT, level_label TEXT, desc TEXT, icon TEXT, page TEXT, color TEXT
)''')
for k, v in dds['robots'].items():
    c.execute('INSERT OR REPLACE INTO robots VALUES(?,?,?,?,?,?,?,?)',
              (k, v['name'], v['level'], v['level_label'], v['desc'], v['icon'], v.get('page',''), v['color']))

# 系统节点
c.execute('''CREATE TABLE IF NOT EXISTS systems (
    id TEXT PRIMARY KEY, name TEXT, hardware TEXT, gpu TEXT, ram TEXT, role TEXT, model TEXT, color TEXT
)''')
for k, v in dds['systems'].items():
    c.execute('INSERT OR REPLACE INTO systems VALUES(?,?,?,?,?,?,?,?)',
              (k, v['name'], v['hardware'], v['gpu'], v['ram'], v['role'], v['model'], v['color']))

# 模型
c.execute('''CREATE TABLE IF NOT EXISTS models (
    id TEXT PRIMARY KEY, name TEXT, full_name TEXT, params TEXT, type TEXT, deployment TEXT, desc TEXT, color TEXT
)''')
for k, v in dds['models'].items():
    c.execute('INSERT OR REPLACE INTO models VALUES(?,?,?,?,?,?,?,?)',
              (k, v['name'], v['full_name'], v['params'], v['type'], v['deployment'], v['desc'], v['color']))

# 硬件
c.execute('''CREATE TABLE IF NOT EXISTS hardware (
    id TEXT PRIMARY KEY, model TEXT, type TEXT, spec TEXT
)''')
for k, v in dds['hardware'].items():
    c.execute('INSERT OR REPLACE INTO hardware VALUES(?,?,?,?)',
              (k, v['model'], v['type'], v['spec']))

# 工厂产线
c.execute('''CREATE TABLE IF NOT EXISTS factory_zones (
    id TEXT PRIMARY KEY, name TEXT, color TEXT, page TEXT, stations TEXT, count INTEGER
)''')
for z in dds['factory']['zones']:
    c.execute('INSERT OR REPLACE INTO factory_zones VALUES(?,?,?,?,?,?)',
              (z['id'], z['name'], z['color'], z['page'], z['stations'], z['count']))

# 工厂全局
c.execute('''CREATE TABLE IF NOT EXISTS factory_meta (
    key TEXT PRIMARY KEY, value TEXT
)''')
for k in ['product', 'product_pn', 'total_stations', 'final_inspection']:
    c.execute('INSERT OR REPLACE INTO factory_meta VALUES(?,?)', (k, str(dds['factory'][k])))

# 路线图
c.execute('''CREATE TABLE IF NOT EXISTS roadmap (
    version TEXT PRIMARY KEY, timeline TEXT, name TEXT, desc TEXT, color TEXT
)''')
for r in dds['roadmap']:
    c.execute('INSERT OR REPLACE INTO roadmap VALUES(?,?,?,?,?)',
              (r['version'], r['timeline'], r['name'], r['desc'], r['color']))

# 主题色
c.execute('''CREATE TABLE IF NOT EXISTS theme (
    key TEXT PRIMARY KEY, value TEXT
)''')
for k, v in dds['theme'].items():
    c.execute('INSERT OR REPLACE INTO theme VALUES(?,?)', (k, v))

# DDS 技能
c.execute('''CREATE TABLE IF NOT EXISTS dds_skills (
    id TEXT PRIMARY KEY, count INTEGER, id_range TEXT, color TEXT, icon TEXT, label TEXT, desc TEXT
)''')
for k, v in dds['dds_skills'].items():
    c.execute('INSERT OR REPLACE INTO dds_skills VALUES(?,?,?,?,?,?,?)',
              (k, v.get('count',0), v.get('id_range',''), v.get('color',''), v.get('icon',''), v.get('label',''), v.get('desc','')))

# 链接
c.execute('''CREATE TABLE IF NOT EXISTS links (
    key TEXT PRIMARY KEY, url TEXT
)''')
for k, v in dds['links'].items():
    c.execute('INSERT OR REPLACE INTO links VALUES(?,?)', (k, v))

# 数据流水线
c.execute('''CREATE TABLE IF NOT EXISTS pipeline (
    step INTEGER PRIMARY KEY, name TEXT, node TEXT, duration INTEGER, icon TEXT
)''')
for i, p in enumerate(dds['pipeline']['phases']):
    c.execute('INSERT OR REPLACE INTO pipeline VALUES(?,?,?,?,?)',
              (i+1, p['name'], p['node'], p['duration'], p['icon']))

conn.commit()

# ── 验证 ──
tables = ['company','kpi','robots','systems','models','hardware','factory_zones','roadmap','theme','dds_skills','links','pipeline']
for t in tables:
    c.execute(f"SELECT COUNT(*) FROM {t}")
    n = c.fetchone()[0]
    print(f"  {t}: {n} rows")

conn.close()
print(f"\nDDS Database created: {DB_PATH}")
print(f"Size: {os.path.getsize(DB_PATH)/1024:.1f} KB")
