/**
 * Z-MAX Shared Pipeline State · v1.0
 * 三页同步: comfyui.html / simulink.html / cicd.html
 * 每 3 秒轮询 relay + orin，存入 localStorage，跨页共享
 */
(function(){
  if(window.__ZMAX_PIPE_LOADED)return;window.__ZMAX_PIPE_LOADED=true;

  const API={relay:"/api/relay/status",orin:"/orin/status"};
  let _state={relay:null,orin:null,lastUpdate:null};

  function _save(){localStorage.setItem("zmax_pipe_state",JSON.stringify(_state))}
  function _notify(){window.dispatchEvent(new CustomEvent("zmax_pipe_update",{detail:_state}))}

  async function poll(){
    try{
      const [rr,ro]=await Promise.all([
        fetch(API.relay).then(r=>r.json()).catch(()=>null),
        fetch(API.orin).then(r=>r.json()).catch(()=>null)
      ]);
      if(rr){_state.relay=rr;_state.relay._ts=Date.now()}
      if(ro){_state.orin=ro;_state.orin._ts=Date.now()}
      _state.lastUpdate=Date.now();
      _save();_notify();
    }catch(e){}
  }
  poll();setInterval(poll,3000);

  // Expose
  window.ZMAX={getState:()=>_state,onUpdate:fn=>window.addEventListener("zmax_pipe_update",e=>fn(e.detail)),refresh:poll};
})();
