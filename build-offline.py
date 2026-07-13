import os, json

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

# Build tab data as JSON array for inline embedding
tabs = []
for name, path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    tabs.append({'name': name, 'html': html})

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
.tab-bar{{display:flex;flex-wrap:wrap;gap:4px;padding:12px 16px;background:#0d1117;border-bottom:1px solid #1a1f2b;position:sticky;top:0;z-index:100}}
.tab{{background:transparent;border:1px solid #1a1f2b;color:#8b949e;padding:7px 14px;border-radius:6px;font-size:12px;cursor:pointer;white-space:nowrap;transition:.2s}}
.tab:hover{{background:#00d4aa11;border-color:#00d4aa44;color:#00d4aa}}
.tab.active{{background:#00d4aa22;border-color:#00d4aa;color:#00d4aa}}
.content{{display:none;padding:0}}.content.active{{display:block}}
iframe{{width:100%;height:calc(100vh - 70px);border:none;background:#06080d}}
</style>
</head>
<body>
<div class="tab-bar" id="tabbar"></div>
<div id="contents"></div>
<script>
var TABS = {tabs_json};
var bar=document.getElementById("tabbar"), con=document.getElementById("contents");
TABS.forEach(function(t,i){{
  var active=i===0?' active':'';
  bar.innerHTML+='<div class="tab'+active+'" onclick="switchTab(this,'+i+')">'+t.name+'</div>';
  con.innerHTML+='<div id="tab'+i+'" class="content'+active+'"><iframe src="about:blank"></iframe></div>';
}});
function switchTab(tab,idx){{
  document.querySelectorAll(".tab").forEach(function(t){{t.classList.remove("active")}});
  tab.classList.add("active");
  document.querySelectorAll(".content").forEach(function(c){{c.classList.remove("active")}});
  var el=document.getElementById("tab"+idx);el.classList.add("active");
  var iframe=el.querySelector("iframe");
  if(iframe&&iframe.src==="about:blank"){{iframe.srcdoc=TABS[idx].html;iframe.src="about:srcdoc"}}
}}
</script>
</body>
</html>'''

with open('offline.html','w',encoding='utf-8') as f:
    f.write(offline)

size = os.path.getsize('offline.html')
print(f'✅ offline.html: {size/1024:.0f}KB ({size} bytes)')
