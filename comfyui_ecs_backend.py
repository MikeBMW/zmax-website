#!/usr/bin/env python3
"""Z-MAX ComfyUI Backend · ECS部署 · 端口50053"""
import json, time, os, http.server

TASKS, JOBS, LOGS = {}, {}, []
START = time.time()

def log(m):
    e = f"[{time.strftime('%H:%M:%S')}] {m}"
    LOGS.append(e); print(e, flush=True)
    if len(LOGS) > 200: LOGS.pop(0)

class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        self.send_response(200); self.send_header("Content-Type", "application/json"); self._cors(); self.end_headers()

        if path == "/status":
            self.wfile.write(json.dumps({"gpu":"ECS (无GPU·代理模式)","vtla_online":False,"active_tasks":len(TASKS),"uptime":time.time()-START},ensure_ascii=False).encode())
        elif path == "/tasks":
            self.wfile.write(json.dumps(list(TASKS.values()),ensure_ascii=False).encode())
        elif path == "/jobs":
            self.wfile.write(json.dumps(list(JOBS.values()),ensure_ascii=False).encode())
        elif path == "/logs":
            self.wfile.write(json.dumps(LOGS[-30:],ensure_ascii=False).encode())
        else:
            self.wfile.write(json.dumps({"comfyui":"Z-MAX ECS Backend v2","endpoints":["/status","/tasks","POST /task"]}).encode())

    def do_POST(self):
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        self.send_response(200); self.send_header("Content-Type", "application/json"); self._cors(); self.end_headers()

        if path == "/task":
            tid = f"task_{int(time.time())}"
            nodes = body.get("nodes", body.get("type", "custom"))
            task = {"id":tid, "nodes":nodes, "status":"created", "created":time.strftime("%H:%M:%S"),
                    "steps":["📝 任务定义","🧠 模型加载(需4090)","🔮 潜空间推理","⚡ Action输出"],
                    "result": "⚠️ 4090离线 · SSH启动: python3 sys2_prod_server.py"}
            TASKS[tid] = task
            log(f"📝 任务: {tid} | 节点:{len(nodes) if isinstance(nodes,list) else 1}")
            self.wfile.write(json.dumps(task,ensure_ascii=False).encode())
        else:
            self.wfile.write(json.dumps({"error":"unknown endpoint"}).encode())

if __name__ == "__main__":
    port = 50053
    log(f"🚀 ComfyUI ECS Backend @ :{port}")
    http.server.HTTPServer(("0.0.0.0", port), H).serve_forever()
