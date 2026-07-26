<?php
// Generate the data-driven proposal page with inline data
header('Content-Type: text/html; charset=utf-8');

$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

$data = ['company'=>[],'kpi'=>[],'robots'=>[],'systems'=>[],'factory_zones'=>[],'roadmap'=>[],'atomic_categories'=>[],'atomic_total'=>0];

$r=$db->query('SELECT key,value FROM company');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['company'][$row['key']]=$row['value'];

$r=$db->query('SELECT * FROM kpi');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['kpi'][$row['id']]=['value'=>$row['value'],'unit'=>$row['unit'],'label'=>$row['label'],'icon'=>$row['icon']];

$r=$db->query('SELECT * FROM robots');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['robots'][]=$row;

$r=$db->query('SELECT * FROM systems');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['systems'][]=$row;

$r=$db->query('SELECT * FROM factory_zones');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['factory_zones'][]=$row;

$r=$db->query('SELECT * FROM roadmap');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['roadmap'][]=$row;

$r=$db->query('SELECT category,COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC');
while($row=$r->fetchArray(SQLITE3_ASSOC))$data['atomic_categories'][]=$row;

$data['atomic_total']=$db->querySingle('SELECT COUNT(*) FROM atomic_skills');
$data['generated_at']=date('Y-m-d H:i:s');
$db->close();

$json=json_encode($data,JSON_UNESCAPED_UNICODE);
?>
<!DOCTYPE html><html lang="zh-CN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Z700 立项申请书 · 数据驱动 | Z-MAX</title>
<style>:root{--c:#00d4aa;--bg:#06080d;--card:#0d1117;--bor:#1a1f2b;--sub:#8b949e;--tx:#c9d1d9;--blue:#58a6ff;--gold:#d4a800;--red:#ff6b6b}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.75}
.wrap{max-width:1100px;margin:0 auto;padding:20px 16px}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.bar a,.bar button{color:var(--c);text-decoration:none;font-size:11px;padding:6px 14px;border:1px solid var(--bor);border-radius:8px;white-space:nowrap;background:transparent;cursor:pointer}
.bar .dl{background:var(--c);color:var(--bg);border-color:var(--c);font-weight:700}
.bar .edit{background:var(--gold);color:var(--bg);border-color:var(--gold)}
.spacer{flex:1}
h1{color:#fff;font-size:24px;text-align:center;font-weight:900;margin:4px 0}
h1 em{color:var(--c);font-style:normal}
.sub{text-align:center;color:var(--sub);font-size:11px;margin-bottom:16px}
.section{margin:24px 0}
.section h2{color:var(--c);font-size:16px;font-weight:800;margin-bottom:8px;padding-bottom:3px;border-bottom:2px solid var(--c)22}
.card{background:var(--card);border:1px solid var(--bor);border-radius:10px;padding:14px 18px;margin:8px 0}
.kpi-row{display:flex;gap:8px;flex-wrap:wrap}
.kpi{flex:1;min-width:100px;background:var(--card);border:1px solid var(--bor);border-radius:8px;padding:12px;text-align:center}
.kpi .v{font-size:22px;font-weight:900;color:var(--c)}.kpi .u{font-size:9px;color:var(--sub)}.kpi .l{font-size:8px;color:var(--sub);margin-top:2px}
.col2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.col3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:6px;overflow:hidden;margin:8px 0;font-size:10px}
th{background:var(--c)22;padding:6px 10px;text-align:left;color:var(--c);font-weight:700}td{padding:5px 10px;border-bottom:1px solid var(--bor)}
[contenteditable]{outline:none;border-bottom:1px dashed transparent;transition:border-color .2s}
[contenteditable]:hover,[contenteditable]:focus{border-bottom-color:var(--c);background:var(--c)08}
[contenteditable].dirty{border-bottom-color:var(--gold)}
.updated{color:var(--c);font-size:9px;text-align:center;margin-top:2px}
.tag{display:inline-block;padding:1px 6px;border-radius:3px;font-size:8px;font-weight:700}
.tg{background:var(--c)22;color:var(--c)}.tb{background:var(--blue)22;color:var(--blue)}.ty{background:var(--gold)22;color:var(--gold)}
@media(max-width:768px){.col2,.col3{grid-template-columns:1fr}.kpi{min-width:80px}.kpi .v{font-size:18px}}
</style></head><body>
<div class="wrap">
<div class="bar">
  <a href="/">← 主页</a>
  <a href="/z700-analysis.html">精品分析</a>
  <a href="/atomic-skills.html">原子技能</a>
  <a href="/dds-editor.html">DDS编辑器</a>
  <span class="spacer"></span>
  <button id="btn-edit" onclick="toggleEdit()">✏️ 编辑</button>
  <a href="/api/proposal.php?format=pptx" class="dl">📊 PPT</a>
  <a href="/api/proposal.php?format=docx" class="dl">📝 Word</a>
</div>
<h1>Z-MAX · <em>Z700</em> 轮式双臂机器人</h1>
<p class="sub">光模块精密制造 · 具身智能旗舰 · 立项申请书</p>
<div class="updated">数据源: DDS全局空间 · <?= date('Y-m-d H:i:s') ?></div>
<div id="content"></div>
</div>
<script>
var D=<?= $json ?>;
var editMode=false;

function toggleEdit(){
  editMode=!editMode;
  document.getElementById('btn-edit').textContent=editMode?'💾 保存':'✏️ 编辑';
  document.getElementById('btn-edit').className=editMode?'bar edit':'bar';
  var els=document.querySelectorAll('[contenteditable]');
  for(var i=0;i<els.length;i++)els[i].contentEditable=editMode?'true':'false';
  if(!editMode)saveChanges();
}

function saveChanges(){
  var changes={},dirty=document.querySelectorAll('[contenteditable].dirty');
  for(var i=0;i<dirty.length;i++){
    var el=dirty[i],key=el.dataset.key;
    if(!key)continue;
    var parts=key.split('.'),table=parts[0],id=parts[1],field=parts[2]||'value';
    if(!changes[table])changes[table]={};
    if(!changes[table][id])changes[table][id]={};
    changes[table][id][field]=el.textContent.trim();
    el.classList.remove('dirty');
  }
  if(!Object.keys(changes).length)return;
  for(var table in changes){
    fetch('/api/dds-all.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({table:table,data:changes[table]})});
  }
}

document.addEventListener('input',function(e){
  if(e.target.contentEditable==='true')e.target.classList.add('dirty');
});

// Render
var co=D.company||{},html='';

html+='<div class="section"><h2>一、项目概述</h2>';
html+='<div class="card"><p style="font-size:11px;color:var(--sub)">AI算力驱动光模块产能扩张。800G/1.6T高速模块产线面临精度/一致性/招工难题。Z700具身智能机器人实现关键工序自主操作。</p></div>';
html+='<div class="kpi-row">';
for(var k in D.kpi){
  var kp=D.kpi[k];
  html+='<div class="kpi"><div class="v" data-key="kpi.'+k+'.value" contenteditable="false">'+kp.value+'</div><div class="u">'+kp.unit+'</div><div class="l" data-key="kpi.'+k+'.label" contenteditable="false">'+kp.label+'</div></div>';
}
html+='</div></div>';

html+='<div class="section"><h2>二、产品与系统架构</h2><div class="col2">';
for(var i=0;i<(D.robots||[]).length;i++){
  var r=D.robots[i],lc=r.level==='L4'?'tg':r.level==='L2'?'tb':'ty';
  html+='<div class="card"><h3><span data-key="robots.'+r.id+'.name" contenteditable="false">'+r.name+'</span> <span class="tag '+lc+'" contenteditable="false"><span data-key="robots.'+r.id+'.level">'+r.level+'</span> <span data-key="robots.'+r.id+'.level_label">'+r.level_label+'</span></span></h3><p style="font-size:10px;color:var(--sub)" data-key="robots.'+r.id+'.desc" contenteditable="false">'+r.desc+'</p></div>';
}
html+='</div></div>';

var fz=D.factory_zones||[];
html+='<div class="section"><h2>三、目标工厂</h2>';
html+='<div class="kpi-row">';
html+='<div class="kpi"><div class="v">'+fz.length+'</div><div class="u">区域</div><div class="l">产线分区</div></div>';
var ts=0;for(var i=0;i<fz.length;i++)ts+=fz[i].stations||0;
html+='<div class="kpi"><div class="v">'+ts+'</div><div class="u">工位</div><div class="l">全流程覆盖</div></div>';
html+='<div class="kpi"><div class="v">'+(D.atomic_total||89)+'</div><div class="u">技能</div><div class="l">原子技能库</div></div>';
html+='<div class="kpi"><div class="v">10</div><div class="u">台</div><div class="l">一期部署</div></div>';
html+='</div>';
html+='<table><tr><th>区域</th><th>工位</th></tr>';
for(var i=0;i<fz.length;i++)html+='<tr><td><b>'+fz[i].name+'</b></td><td>'+fz[i].stations+'</td></tr>';
html+='</table></div>';

var ac=D.atomic_categories||[];
html+='<div class="section"><h2>四、原子技能覆盖（'+(D.atomic_total||89)+'项）</h2><div class="col3">';
for(var i=0;i<ac.length;i++)html+='<div class="card" style="text-align:center"><div style="font-size:20px;font-weight:900;color:var(--c)">'+ac[i].cnt+'</div><div style="font-size:10px;color:var(--sub)">'+ac[i].category+'</div></div>';
html+='</div></div>';

html+='<div class="section"><h2>五、开发路线图</h2>';
for(var i=0;i<(D.roadmap||[]).length;i++){
  var rd=D.roadmap[i];
  html+='<div class="card"><h3 style="color:'+(rd.color||'var(--c)')+'">'+rd.version+': '+rd.name+'</h3><p style="font-size:10px;color:var(--sub)">'+rd.timeline+' · '+rd.desc+'</p></div>';
}
html+='</div>';

html+='<div class="card" style="text-align:center;padding:16px;margin-top:24px">';
html+='<h3 style="color:var(--c);font-size:15px">'+(co.product_tag||'具身智能精密制造')+'</h3>';
html+='<p style="font-size:10px;color:var(--sub);margin-top:4px">'+(co.name||'')+' · '+(co.domain||'datadrive.world')+' · '+(co.year||'2026')+'</p>';
html+='</div>';

document.getElementById('content').innerHTML=html;
</script></body></html>
