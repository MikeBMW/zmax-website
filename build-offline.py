import os, json, re

pages = [
    ('🏠 主页','index.html'),
    ('⚡ 算力指标','performance.html'),
    ('🏭 工厂调研','survey.html'),
    ('🔩 Orin管线','orin-pipeline.html'),
    ('🔌 系统接口','system-interfaces.html'),
    ('📝 复盘','retrospective.html'),
    ('✅ 验收','acceptance.html'),
    ('🔄 恢复指南','recovery.html'),
]

def extract_body(html):
    # Extract <style> blocks from head
    styles = ''
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.DOTALL):
        styles += m.group(0)
    # Extract <body> content (everything between <body> and </body>)
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    body = m.group(1) if m else html
    return styles + body

tabs = []
for name, path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    tabs.append({'name': name, 'body': extract_body(html)})

tabs_json = json.dumps(tabs, ensure_ascii=False)

offline = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Z-MAX 离线包</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#06080d;color:#c8d1d9}}
.tab-bar{{display:flex;flex-wrap:wrap;gap:4px;padding:10px 14px;background:#0d1117;border-bottom:2px solid #00d4aa33;position:sticky;top:0;z-index:999;overflow-x:auto}}
.tab{{background:transparent;border:1px solid #1a1f2b;color:#8b949e;padding:6px 12px;border-radius:6px;font-size:12px;cursor:pointer;white-space:nowrap;transition:.2s;flex-shrink:0}}
.tab:hover{{background:#00d4aa11;border-color:#00d4aa44;color:#00d4aa}}
.tab.active{{background:#00d4aa22;border-color:#00d4aa;color:#00d4aa}}
.page{{display:none;padding:20px 24px;min-height:100vh}}
.page.active{{display:block}}
</style>
</head>
<body>
<div class="tab-bar" id="tabbar"></div>
<div id="container"></div>
<script>
var TABS = {tabs_json};
var bar=document.getElementById("tabbar"), con=document.getElementById("container");
TABS.forEach(function(t,i){{
  bar.innerHTML+='<div class="tab'+(i===0?' active':'')+'" onclick="switchTab(this,'+i+')">'+t.name+'</div>';
  con.innerHTML+='<div class="page'+(i===0?' active':'')+'" id="page'+i+'">'+t.body+'</div>';
}});
function switchTab(tab,idx){{
  document.querySelectorAll(".tab").forEach(function(t){{t.classList.remove("active")}});
  tab.classList.add("active");
  document.querySelectorAll(".page").forEach(function(p){{p.classList.remove("active")}});
  document.getElementById("page"+idx).classList.add("active");
}}
</script>
</body>
</html>'''

with open('offline.html','w',encoding='utf-8') as f:
    f.write(offline)
print(f'✅ {os.path.getsize("offline.html")/1024:.0f}KB')
