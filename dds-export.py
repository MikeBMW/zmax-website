#!/usr/bin/env python3
"""DDS SQLite → dds-global.js 同步导出"""
import sqlite3, os

DB = '/www/wwwroot/datadrive.world/dds.db'
OUT = '/www/wwwroot/datadrive.world/dds-global.js'
conn = sqlite3.connect(DB)

def col(c, table, val_col='value'):
    c.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in c.description]
    result = {}
    for r in c.fetchall():
        d = dict(zip(cols, r))
        k = d.pop('key')
        result[k] = d[val_col]
    return result

def row(c, table, key_col='id'):
    c.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in c.description]
    result = {}
    for r in c.fetchall():
        d = dict(zip(cols, r))
        k = d.pop(key_col)
        result[k] = d
    return result

c = conn.cursor()
company = col(c, 'company')
kpi_data = row(c, 'kpi')
robots = row(c, 'robots')
systems = row(c, 'systems')
models = row(c, 'models')
hardware = row(c, 'hardware')

c.execute("SELECT * FROM factory_zones ORDER BY id")
zc = [d[0] for d in c.description]
zones = [dict(zip(zc, r)) for r in c.fetchall()]

factory_meta = col(c, 'factory_meta')
roadmap = [dict(zip([d[0] for d in c.description], r)) for r in c.execute("SELECT * FROM roadmap ORDER BY version").fetchall()]
theme = col(c, 'theme')
skills = [dict(zip([d[0] for d in c.description], r)) for r in c.execute("SELECT * FROM dds_skills").fetchall()]
dds_skills = {s['id']: {k:v for k,v in s.items() if k!='id'} for s in skills}

# Links: key→url (2-column table)
links_data = {}
for r in c.execute("SELECT * FROM links").fetchall():
    links_data[r[0]] = r[1]

pipeline_phases = [dict(zip([d[0] for d in c.description], r)) for r in c.execute("SELECT * FROM pipeline ORDER BY step").fetchall()]
conn.close()

def esc(s): return str(s).replace('\\','\\\\').replace('"','\\"')

lines = []
L = lines.append
L("""/**
 * DDS Global Data Layer · SQLite驱动
 * 数据源：dds.db → dds-export.py 导出
 * 版本：v2.6 · 2026-07-26
 */
window.DDS = {""")

L("  company: {")
for k in ['name','name_en','product','product_tag','domain','year','city']:
    v = company.get(k,''); L(f'    {k}: "{esc(v)}",')
L("  },")

L("  kpi: {")
for kid, kv in kpi_data.items():
    L(f'    {kid}: {{ value:"{esc(kv["value"])}", unit:"{esc(kv["unit"])}", label:"{esc(kv["label"])}", icon:"{esc(kv.get("icon",""))}" }},')
L("  },")

L("  robots: {")
for rid, rv in robots.items():
    L(f'    {rid}: {{ id:"{esc(rid)}", name:"{esc(rv["name"])}", level:"{esc(rv["level"])}", level_label:"{esc(rv["level_label"])}", desc:"{esc(rv["desc"])}", icon:"{esc(rv["icon"])}", page:"{esc(rv.get("page",""))}", color:"{esc(rv["color"])}" }},')
L("  },")

L("  systems: {")
for sid, sv in systems.items():
    L(f'    {sid}: {{ id:"{esc(sv["name"].split(chr(183))[0].strip())}", name:"{esc(sv["name"])}", hardware:"{esc(sv["hardware"])}", gpu:"{esc(sv["gpu"])}", ram:"{esc(sv["ram"])}", role:"{esc(sv["role"])}", model:"{esc(sv["model"])}", color:"{esc(sv["color"])}" }},')
L("  },")

L("  models: {")
for mid, mv in models.items():
    L(f'    {mid}: {{ name:"{esc(mv["name"])}", full_name:"{esc(mv["full_name"])}", params:"{esc(mv["params"])}", type:"{esc(mv["type"])}", deployment:"{esc(mv["deployment"])}", desc:"{esc(mv["desc"])}", color:"{esc(mv["color"])}" }},')
L("  },")

L("  hardware: {")
for hid, hv in hardware.items():
    L(f'    {hid}: {{ model:"{esc(hv["model"])}", type:"{esc(hv["type"])}", spec:"{esc(hv["spec"])}" }},')
L("  },")

L("  factory: {")
L(f'    product: "{esc(factory_meta.get("product",""))}",')
L(f'    product_pn: "{esc(factory_meta.get("product_pn",""))}",')
L("    zones: [")
for z in zones:
    L(f'      {{ id:"{esc(z["id"])}", name:"{esc(z["name"])}", color:"{esc(z["color"])}", page:"{esc(z["page"])}", stations:"{esc(z["stations"])}", count:{z["count"]} }},')
L("    ],")
L(f'    total_stations: {factory_meta.get("total_stations",0)},')
L(f'    final_inspection: "{esc(factory_meta.get("final_inspection",""))}",')
L("  },")

L("  dds_skills: {")
for sid, sv in dds_skills.items():
    L(f'    {sid}: {{ count:{sv.get("count",0)}, id_range:"{esc(sv.get("id_range",""))}", color:"{esc(sv.get("color",""))}", icon:"{esc(sv.get("icon",""))}", label:"{esc(sv.get("label",""))}", desc:"{esc(sv.get("desc",""))}" }},')
L("  },")

L("  pipeline: {")
L('    name: "数据流水线 · Orin→MAC→4090", version: "2.0",')
L("    phases: [")
for p in pipeline_phases:
    L(f'      {{ name:"{esc(p["name"])}", node:"{esc(p["node"])}", duration:{p["duration"]}, icon:"{esc(p["icon"])}" }},')
L("    ],")
L("  },")

L("  roadmap: [")
for r in roadmap:
    L(f'    {{ version:"{esc(r["version"])}", timeline:"{esc(r["timeline"])}", name:"{esc(r["name"])}", desc:"{esc(r["desc"])}", color:"{esc(r["color"])}" }},')
L("  ],")

L("  links: {")
for k, v in links_data.items():
    L(f'    {k}: "{esc(v)}",')
L("  },")

L("  theme: {")
for k, v in theme.items():
    L(f'    {k}: "{esc(v)}",')
L("  },")

L("};")
L("")
L("window.DDS.getKPI = function(key) { return this.kpi[key]; };")
L("window.DDS.getRobot = function(id) { return this.robots[id]; };")
L("window.DDS.getSystem = function(id) { return this.systems[id]; };")
L("window.DDS.getModel = function(id) { return this.models[id]; };")
L("window.DDS.getZone = function(id) { return this.factory.zones.find(function(z){return z.id===id;}); };")
L("")
L('console.log("DDS Global · SQLite同步 · v" + window.DDS.company.year + " · " + window.DDS.factory.product);')

with open(OUT, 'w') as f: f.write('\n'.join(lines))
print(f"Exported: {OUT} ({os.path.getsize(OUT)} bytes)")
