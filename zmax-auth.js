// Z-MAX 全站认证 — 所有受保护页面引用此脚本
(function(){
  if(localStorage.getItem('zmax_auth')) return; // 已登录

  // 注入登录浮层
  var overlay = document.createElement('div');
  overlay.id = 'zmax-auth-overlay';
  overlay.innerHTML = '<div style="background:#0d1117;border:1px solid #00d4aa44;border-radius:12px;padding:40px 36px;text-align:center;max-width:360px;width:90%">'+
    '<div style="font-size:28px;color:#00d4aa;font-weight:800;margin-bottom:6px">Z-MAX</div>'+
    '<div style="font-size:12px;color:#8b949e;margin-bottom:28px">静界科技 · 内部系统</div>'+
    '<input id="zmax-auth-user" type="text" value="15840273872" placeholder="用户名" style="width:100%;padding:12px 14px;margin-bottom:10px;background:#06080d;border:1px solid #1a1f2b;border-radius:8px;color:#c8d1d9;font-size:14px;outline:none" autocomplete="off">'+
    '<input id="zmax-auth-pass" type="password" placeholder="密码" style="width:100%;padding:12px 14px;margin-bottom:6px;background:#06080d;border:1px solid #1a1f2b;border-radius:8px;color:#c8d1d9;font-size:14px;outline:none">'+
    '<div id="zmax-auth-err" style="color:#ff4444;font-size:11px;min-height:20px;margin-bottom:12px"></div>'+
    '<button id="zmax-auth-btn" style="width:100%;padding:12px;background:#00d4aa;color:#06080d;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer">🔐 登 录</button>'+
    '<div style="margin-top:16px"><a href="/" style="color:#8b949e;text-decoration:none;font-size:11px">← 返回主页</a></div>'+
  '</div>';
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(6,8,13,0.97);z-index:9999;display:flex;align-items:center;justify-content:center';
  document.body.appendChild(overlay);

  // 登录逻辑
  document.getElementById('zmax-auth-btn').onclick = function(){
    var u = document.getElementById('zmax-auth-user').value;
    var p = document.getElementById('zmax-auth-pass').value;
    if(u==='15840273872' && p==='15840273872'){
      localStorage.setItem('zmax_auth','1');
      overlay.style.display = 'none';
    } else {
      document.getElementById('zmax-auth-err').innerText = '⛔ 用户名或密码错误';
    }
  };

  // 回车登录
  document.getElementById('zmax-auth-pass').addEventListener('keydown',function(e){
    if(e.key==='Enter') document.getElementById('zmax-auth-btn').click();
  });
})();
