<?php
$db=new SQLite3('/www/wwwroot/datadrive.world/dds.db');
$data=['company'=>[],'kpi'=>[],'robots'=>[],'systems'=>[],'factory_zones'=>[],'roadmap'=>[],'atomic_categories'=>[],'atomic_total'=>0];
$r=$db->query('SELECT key,value FROM company');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['company'][$row['key']]=$row['value'];
$r=$db->query('SELECT * FROM kpi');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['kpi'][$row['id']]=['value'=>$row['value'],'unit'=>$row['unit'],'label'=>$row['label'],'icon'=>$row['icon']];
$r=$db->query('SELECT * FROM robots');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['robots'][]=$row;
$r=$db->query('SELECT * FROM systems');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['systems'][]=$row;
$r=$db->query('SELECT * FROM factory_zones');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['factory_zones'][]=$row;
$r=$db->query('SELECT * FROM roadmap');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['roadmap'][]=$row;
$r=$db->query('SELECT category,COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC');while($row=$r->fetchArray(SQLITE3_ASSOC))$data['atomic_categories'][]=$row;
$data['atomic_total']=$db->querySingle('SELECT COUNT(*) FROM atomic_skills');
$data['generated_at']=date('Y-m-d H:i:s');$db->close();
$json=json_encode($data,JSON_UNESCAPED_UNICODE);
?><!DOCTYPE html><html lang="zh-CN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Z700 立项书 · 在线编辑 | Z-MAX</title>
<style>:root{--c:#00d4aa;--bg:#06080d;--card:#0d1117;--bor:#1a1f2b;--sub:#8b949e;--tx:#c9d1d9;--blue:#58a6ff;--gold:#d4a800;--red:#ff6b6b}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.75;padding-bottom:80px}
.wrap{max-width:1100px;margin:0 auto;padding:16px 14px}
.bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.bar a,.bar button{color:var(--c);text-decoration:none;font-size:10px;padding:5px 10px;border:1px solid var(--bor);border-radius:6px;white-space:nowrap;background:transparent;cursor:pointer}
.bar .dl{background:var(--c);color:var(--bg);border-color:var(--c);font-weight:700}
.spacer{flex:1}
h1{color:#fff;font-size:22px;text-align:center;font-weight:900;margin:4px 0}
h1 em{color:var(--c);font-style:normal}
.sub{text-align:center;color:var(--sub);font-size:10px;margin-bottom:12px}
.section{margin:20px 0}
.section h2{color:var(--c);font-size:15px;font-weight:800;margin-bottom:6px;padding-bottom:2px;border-bottom:2px solid var(--c)22}
.card{background:var(--card);border:1px solid var(--bor);border-radius:10px;padding:12px 16px;margin:6px 0}
.kpi-row{display:flex;gap:6px;flex-wrap:wrap}
.kpi{flex:1;min-width:90px;background:var(--card);border:1px solid var(--bor);border-radius:8px;padding:10px;text-align:center}
.kpi .v{font-size:20px;font-weight:900;color:var(--c)}.kpi .u{font-size:8px;color:var(--sub)}.kpi .l{font-size:8px;color:var(--sub);margin-top:1px}
.col2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.col3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:6px;overflow:hidden;margin:6px 0;font-size:9px}
th{background:var(--c)22;padding:5px 8px;text-align:left;color:var(--c);font-weight:700}td{padding:4px 8px;border-bottom:1px solid var(--bor)}
.editable{position:relative}
.editable::after{content:'✎';position:absolute;right:2px;top:0;font-size:8px;color:var(--sub);opacity:0;transition:opacity .2s}
.editable:hover::after,.editable:focus::after{opacity:.6}
.editable:focus{outline:2px solid var(--c);outline-offset:2px;border-radius:3px;background:var(--c)08}
.editable.dirty{outline-color:var(--gold)}
.updated{color:var(--c);font-size:8px;text-align:center;margin-top:1px}
.tag{display:inline-block;padding:1px 5px;border-radius:3px;font-size:7px;font-weight:700}
.tg{background:var(--c)22;color:var(--c)}.tb{background:var(--blue)22;color:var(--blue)}.ty{background:var(--gold)22;color:var(--gold)}
#edit-bar{position:fixed;bottom:0;left:0;right:0;z-index:100;background:rgba(13,17,23,.97);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:1px solid var(--bor);padding:10px 14px;padding-bottom:max(10px,env(safe-area-inset-bottom));display:flex;gap:8px}
#edit-bar button{flex:1;padding:12px;border-radius:10px;border:none;font-size:13px;font-weight:700;cursor:pointer}
#edit-bar .btn-edit{background:var(--gold);color:var(--bg)}
#edit-bar .btn-edit.active{background:var(--c);color:var(--bg)}
#edit-bar .btn-save{background:var(--c);color:var(--bg);display:none}
#edit-bar .btn-save.show{display:block}
#edit-bar .btn-gen{background:transparent;border:1px solid var(--bor);color:var(--sub);flex:.6}
@media(max-width:768px){.col2,.col3{grid-template-columns:1fr}.kpi{min-width:70px}.kpi .v{font-size:17px}}
</style></head><body>
<div class="wrap">
<div class="bar">
  <a href="/">← 主页</a><a href="/atomic-skills.html">技能</a>
  <span class="spacer"></span>
  <a href="/api/proposal.php?format=pptx" class="dl">📊 PPT</a>
  <a href="/api/proposal.php?format=docx" class="dl">📝 Word</a>
</div>
<h1>Z-MAX · <em>Z700</em> 立项申请书</h1>
<p class="sub">数据驱动 · 点击编辑 · 自动同步PPT</p>
<div class="updated">DDS全局空间 · <?=date('Y-m-d H:i:s')?></div>
<div id="content"></div>
</div>

<div id="edit-bar">
  <button class="btn-gen" onclick="location.href='/api/proposal.php?format=pptx'">📊 生成PPT</button>
  <button class="btn-edit" id="btn-edit" onclick="toggleEdit()">✏️ 开启编辑</button>
  <button class="btn-save" id="btn-save" onclick="saveNow()">💾 保存</button>
</div>

<script>
var D=<?=$json?>,editing=false;

function toggleEdit(){
  editing=!editing;
  document.getElementById('btn-edit').textContent=editing?'✅ 编辑中':'✏️ 开启编辑';
  document.getElementById('btn-edit').className=editing?'btn-edit active':'btn-edit';
  document.getElementById('btn-save').className=editing?'btn-save show':'btn-save';
  var els=document.querySelectorAll('.editable');
  for(var i=0;i<els.length;i++)els[i].contentEditable=editing?'true':'false';
  if(editing){var f=document.querySelector('.editable');if(f)f.focus()}
}

function saveNow(){
  var ch={},dirty=document.querySelectorAll('.editable.dirty');
  for(var i=0;i<dirty.length;i++){
    var el=dirty[i],key=el.dataset.key;if(!key)continue;
    var p=key.split('.'),t=p[0],id=p[1],f=p[2]||'value';
    if(!ch[t])ch[t]={};if(!ch[t][id])ch[t][id]={};
    ch[t][id][f]=el.textContent.trim();el.classList.remove('dirty');
  }
  if(!Object.keys(ch).length){alert('没有修改');return}
  for(var t in ch){
    fetch('/api/dds-all.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({table:t,data:ch[t]})});
  }
  alert('已保存！点击「生成PPT」下载最新版本');
}

document.addEventListener('input',function(e){if(e.target.classList.contains('editable'))e.target.classList.add('dirty')});

// Mobile: double-tap to edit
document.addEventListener('touchend',function(e){
  if(!editing){var el=e.target.closest('.editable');if(el){toggleEdit();setTimeout(function(){el.focus()},100)}}
});

var co=D.company||{},html='';

html+='<div class="section"><h2>一、项目概述</h2>';
html+='<div class="card"><p style="font-size:10px;color:var(--sub)">AI算力驱动光模块产能扩张。Z700具身智能机器人实现关键工序自主操作。一期10台(5自研+5它石)·白盒交付。</p></div>';
html+='<div class="kpi-row">';
for(var k in D.kpi){var kp=D.kpi[k];
  html+='<div class="kpi"><div class="v editable" data-key="kpi.'+k+'.value">'+kp.value+'</div><div class="u">'+kp.unit+'</div><div class="l editable" data-key="kpi.'+k+'.label">'+kp.label+'</div></div>';
}
html+='</div></div>';

html+='<div class="section"><h2>二、产品架构</h2><div class="col2">';
for(var i=0;i<(D.robots||[]).length;i++){var r=D.robots[i],lc=r.level==='L4'?'tg':r.level==='L2'?'tb':'ty';
  html+='<div class="card"><h3><span class="editable" data-key="robots.'+r.id+'.name">'+r.name+'</span> <span class="tag '+lc+'"><span class="editable" data-key="robots.'+r.id+'.level">'+r.level+'</span> <span class="editable" data-key="robots.'+r.id+'.level_label">'+r.level_label+'</span></span></h3><p style="font-size:9px;color:var(--sub)" class="editable" data-key="robots.'+r.id+'.desc">'+r.desc+'</p></div>';
}
html+='</div></div>';

var fz=D.factory_zones||[];
html+='<div class="section"><h2>三、目标工厂</h2>';
html+='<div class="kpi-row">';
html+='<div class="kpi"><div class="v">'+fz.length+'</div><div class="u">区域</div><div class="l">产线分区</div></div>';
var ts=0;for(var i=0;i<fz.length;i++)ts+=fz[i].stations||0;
html+='<div class="kpi"><div class="v">'+ts+'</div><div class="u">工位</div><div class="l">全流程</div></div>';
html+='<div class="kpi"><div class="v">'+(D.atomic_total||89)+'</div><div class="u">技能</div><div class="l">原子技能</div></div>';
html+='<div class="kpi"><div class="v">10</div><div class="u">台</div><div class="l">一期部署</div></div>';
html+='</div><table><tr><th>区域</th><th>工位</th></tr>';
for(var i=0;i<fz.length;i++)html+='<tr><td><b>'+fz[i].name+'</b></td><td>'+fz[i].stations+'</td></tr>';
html+='</table></div>';

var ac=D.atomic_categories||[];
html+='<div class="section"><h2>四、原子技能（'+(D.atomic_total||89)+'项）</h2><div class="col3">';
for(var i=0;i<ac.length;i++)html+='<div class="card" style="text-align:center"><div style="font-size:18px;font-weight:900;color:var(--c)">'+ac[i].cnt+'</div><div style="font-size:9px;color:var(--sub)">'+ac[i].category+'</div></div>';
html+='</div></div>';

html+='<div class="section"><h2>五、路线图</h2>';
for(var i=0;i<(D.roadmap||[]).length;i++){var rd=D.roadmap[i];
  html+='<div class="card"><h3 style="color:'+(rd.color||'var(--c)')+'">'+rd.version+': '+rd.name+'</h3><p style="font-size:9px;color:var(--sub)">'+rd.timeline+' · '+rd.desc+'</p></div>';
}
html+='</div>';

html+='<div class="card" style="text-align:center;padding:14px;margin-top:20px">';
html+='<h3 style="color:var(--c);font-size:14px">'+(co.product_tag||'具身智能精密制造')+'</h3>';
html+='<p style="font-size:9px;color:var(--sub);margin-top:3px">'+(co.name||'')+' · '+(co.domain||'datadrive.world')+' · '+(co.year||'2026')+'</p>';
html+='</div>';

document.getElementById('content').innerHTML=html;
</script></body></html>
