#!/usr/bin/env python3
"""DDS SQLite → dds-global.js 同步导出"""
import sqlite3, json, os

DB = '/www/wwwroot/datadrive.world/dds.db'
OUT = '/www/wwwroot/datadrive.world/dds-global.js'

conn = sqlite3.connect(DB)

def row(c, table, key_col='key'):
    c.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in c.description]
    result = {}
    for r in c.fetchall():
        d = dict(zip(cols, r))
        k = d.pop(key_col)
        result[k] = d
    return result

def col(c, table, key_col='key'):
    c.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in c.description]
    result = {}
    for r in c.fetchall():
        d = dict(zip(cols, r))
        k = d.pop(key_col)
        result[k] = d['value']
    return result

c = conn.cursor()

company = col(c, 'company')
kpi_data = row(c, 'kpi', 'id')
robots = row(c, 'robots', 'id')
systems = row(c, 'systems', 'id')
models = row(c, 'models', 'id')
hardware = row(c, 'hardware', 'id')

c.execute("SELECT * FROM factory_zones ORDER BY id")
zones_cols = [d[0] for d in c.description]
zones = [dict(zip(zones_cols, r)) for r in c.fetchall()]

factory_meta = col(c, 'factory_meta')
c.execute("SELECT * FROM roadmap ORDER BY version")
rm_cols = [d[0] for d in c.description]
roadmap = [dict(zip(rm_cols, r)) for r in c.fetchall()]

theme = col(c, 'theme')

c.execute("SELECT * FROM dds_skills")
skills_cols = [d[0] for d in c.description]
skills_raw = [dict(zip(skills_cols, r)) for r in c.fetchall()]
dds_skills = {}
for s in skills_raw:
    dds_skills[s['id']] = {k: v for k, v in s.items() if k != 'id'}

links_data = col(c, 'links')

c.execute("SELECT * FROM pipeline ORDER BY step")
pipe_cols = [d[0] for d in c.description]
pipeline_phases = [dict(zip(pipe_cols, r)) for r in c.fetchall()]

conn.close()

# Build JS
js = f'''/**
 * DDS Global Data Layer · SQLite驱动
 * 
 * 数据源：dds.db (SQLite) → dds-export.py 导出
 * 改数据改数据库，运行 python3 dds-export.py 同步
 * 
 * 版本：v2.6 · 2026-07-26
 */
window.DDS = {{

  company: {{
    name:       "{company.get('name','')}",
    name_en:    "{company.get('name_en','')}",
    product:    "{company.get('product','')}",
    product_tag:"{company.get('product_tag','')}",
    domain:     "{company.get('domain','')}",
    year:       "{company.get('year','')}",
    city:       "{company.get('city','')}",
  }},

  kpi: {{
    precision:  {{ value:"{kpi_data['precision']['value']}", unit:"{kpi_data['precision']['unit']}", label:"{kpi_data['precision']['label']}", icon:"{kpi_data['precision']['icon']}" }},
    yield_rate: {{ value:"{kpi_data['yield_rate']['value']}", unit:"{kpi_data['yield_rate']['unit']}", label:"{kpi_data['yield_rate']['label']}", icon:"{kpi_data['yield_rate']['icon']}" }},
    force_bw:   {{ value:"{kpi_data['force_bw']['value']}", unit:"{kpi_data['force_bw']['unit']}", label:"{kpi_data['force_bw']['label']}", icon:"{kpi_data['force_bw']['icon']}" }},
    cycle_time: {{ value:"{kpi_data['cycle_time']['value']}", unit:"{kpi_data['cycle_time']['unit']}", label:"{kpi_data['cycle_time']['label']}", icon:"{kpi_data['cycle_time']['icon']}" }},
  }},

  robots: {{
    Z700: {{ id:"Z700", name:"{robots['Z700']['name']}", level:"{robots['Z700']['level']}", level_label:"{robots['Z700']['level_label']}", desc:"{robots['Z700']['desc']}", icon:"{robots['Z700']['icon']}", page:"{robots['Z700']['page']}", color:"{robots['Z700']['color']}" }},
    Z700F:{{ id:"Z700F",name:"{robots['Z700F']['name']}",level:"{robots['Z700F']['level']}",level_label:"{robots['Z700F']['level_label']}",desc:"{robots['Z700F']['desc']}",icon:"{robots['Z700F']['icon']}",page:"{robots['Z700F']['page']}",color:"{robots['Z700F']['color']}" }},
    Z100L:{{ id:"Z100L",name:"{robots['Z100L']['name']}",level:"{robots['Z100L']['level']}",level_label:"{robots['Z100L']['level_label']}",desc:"{robots['Z100L']['desc']}",icon:"{robots['Z100L']['icon']}",page:"{robots['Z100L']['page']}",color:"{robots['Z100L']['color']}" }},
    Z700F_AOI:{{ id:"Z700F+AOI",name:"{robots['Z700F_AOI']['name']}",level:"{robots['Z700F_AOI']['level']}",level_label:"{robots['Z700F_AOI']['level_label']}",desc:"{robots['Z700F_AOI']['desc']}",icon:"{robots['Z700F_AOI']['icon']}",page:"{robots['Z700F_AOI']['page']}",color:"{robots['Z700F_AOI']['color']}" }},
  }},

  systems: {{
    sys0: {{ id:"Sys0",name:"{systems['sys0']['name']}",hardware:"{systems['sys0']['hardware']}",gpu:"{systems['sys0']['gpu']}",ram:"{systems['sys0']['ram']}",role:"{systems['sys0']['role']}",model:"{systems['sys0']['model']}",color:"{systems['sys0']['color']}" }},
    sys1: {{ id:"Sys1",name:"{systems['sys1']['name']}",hardware:"{systems['sys1']['hardware']}",gpu:"{systems['sys1']['gpu']}",ram:"{systems['sys1']['ram']}",role:"{systems['sys1']['role']}",model:"{systems['sys1']['model']}",color:"{systems['sys1']['color']}" }},
    sys2: {{ id:"Sys2",name:"{systems['sys2']['name']}",hardware:"{systems['sys2']['hardware']}",gpu:"{systems['sys2']['gpu']}",ram:"{systems['sys2']['ram']}",role:"{systems['sys2']['role']}",model:"{systems['sys2']['model']}",color:"{systems['sys2']['color']}" }},
    edge: {{ id:"Edge",name:"{systems['edge']['name']}",hardware:"{systems['edge']['hardware']}",gpu:"{systems['edge']['gpu']}",ram:"{systems['edge']['ram']}",role:"{systems['edge']['role']}",model:"{systems['edge']['model']}",color:"{systems['edge']['color']}" }},
  }},

  models: {{
{''.join(f'    {k}: {{ name:"{v["name"]}",full_name:"{v["full_name"]}",params:"{v["params"]}",type:"{v["type"]}",deployment:"{v["deployment"]}",desc:"{v["desc"]}",color:"{v["color"]}" }},\n' for k, v in models.items())}  }},

  hardware: {{
{''.join(f'    {k}: {{ model:"{v["model"]}",type:"{v["type"]}",spec:"{v["spec"]}" }},\n' for k, v in hardware.items())}  }},

  factory: {{
    product:      "{factory_meta.get('product','')}",
    product_pn:   "{factory_meta.get('product_pn','')}",
    zones: [
{''.join(f'      {{ id:"{z["id"]}",name:"{z["name"]}",color:"{z["color"]}",page:"{z["page"]}",stations:"{z["stations"]}",count:{z["count"]} }},\n' for z in zones)}    ],
    total_stations: {factory_meta.get('total_stations',0)},
    final_inspection: "{factory_meta.get('final_inspection','')}",
  }},

  dds_skills: {{
{''.join(f'    {k}: {{ count:{v.get("count",0)},id_range:"{v.get("id_range","")}",color:"{v.get("color","")}",icon:"{v.get("icon","")}",label:"{v.get("label","")}",desc:"{v.get("desc","")}" }},\n' for k, v in dds_skills.items())}  }},

  pipeline: {{
    name: "数据流水线 · Orin→MAC→4090",
    version: "2.0",
    phases: [
{''.join(f'      {{ name:"{p["name"]}",node:"{p["node"]}",duration:{p["duration"]},icon:"{p["icon"]}" }},\n' for p in pipeline_phases)}    ],
  }},

  roadmap: [
{''.join(f'    {{ version:"{r["version"]}",timeline:"{r["timeline"]}",name:"{r["name"]}",desc:"{r["desc"]}",color:"{r["color"]}" }},\n' for r in roadmap)}  ],

  links: {{
{''.join(f'    {k}: "{v}",\n' for k, v in links_data.items())}  }},

  theme: {{
{''.join(f'    {k}: "{v}",\n' for k, v in theme.items())}  }},

}};

window.DDS.getKPI = function(key) {{ return this.kpi[key]; }};
window.DDS.getRobot = function(id) {{ return this.robots[id]; }};
window.DDS.getSystem = function(id) {{ return this.systems[id]; }};
window.DDS.getModel = function(id) {{ return this.models[id]; }};
window.DDS.getZone = function(id) {{ return this.factory.zones.find(function(z){{return z.id===id;}}); }};

console.log("DDS Global · SQLite同步 · v" + window.DDS.company.year + " · " + window.DDS.factory.product);
'''

with open(OUT, 'w') as f:
    f.write(js)

print(f"Exported: {OUT}")
print(f"Size: {os.path.getsize(OUT)/1024:.1f} KB")
