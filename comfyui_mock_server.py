#!/usr/bin/env python3
"""Mock inference server for ComfyUI — handles /api/comfy/task and /api/comfy/status"""
import json, time, uuid, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 50053
TASKS = {}  # task_id -> {status, nodes, model, result, created}

INFERENCE_RESULTS = {
    "ACT": {
        "model": "ACT Action Chunking · Sys10 · 4060",
        "hardware": "4060 (xspace)",
        "location": "Sys10",
        "steps": [
            "📷 加载传感器数据: D405 RGB-D + 六维力 + 关节状态",
            "🔀 多模态编码适配: 3路信号→128维特征",
            "🧬 编码器融合: 特征向量→潜空间z=32维",
            "🧠 ACT推理: CVAE解码→Action Chunk [1,50,6]",
            "⚡ 动作解码: 6轴关节轨迹+夹爪",
            "🤖 Orin执行: SR5-C 7轴 → Z700系列机器人"
        ],
        "result": "✅ ACT推理完成 · Action Chunk [1,50,6] · 推理耗时 48ms · 力控精度 ±0.02mm",
        "timing": {"model_load": "120ms", "inference": "48ms", "total": "175ms"}
    },
    "SmolVLA": {
        "model": "SmolVLA · Sys11 · 4060",
        "hardware": "4060 (xspace)",
        "location": "Sys11",
        "steps": ["📷 VLM编码", "🧠 SmolVLA推理", "⚡ 动作解码"],
        "result": "✅ SmolVLA推理完成 · 257ms",
        "timing": {"model_load": "800ms", "inference": "257ms", "total": "1080ms"}
    },
    "VLA-T": {
        "model": "VLA-T Force-Control · Sys21 · 4060",
        "hardware": "4060 (xspace)",
        "location": "Sys21",
        "steps": ["📷 RGB+力触觉融合", "🧠 DiT推理", "⚡ 力控动作"],
        "result": "✅ VLA-T推理完成 · 180ms · 力控精度±0.01mm",
        "timing": {"model_load": "200ms", "inference": "180ms", "total": "400ms"}
    },
    "GR00T": {
        "model": "GR00T N1.7 · Sys2 · 4090",
        "hardware": "4090 (web)",
        "location": "Sys2",
        "steps": ["📷 多模态编码", "🧠 MoE推理", "⚡ 通用动作"],
        "result": "✅ GR00T推理完成 · 1.2s · 6.4GB VRAM",
        "timing": {"model_load": "3000ms", "inference": "1200ms", "total": "4500ms"}
    }
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.rstrip("/")
        # GET /status
        if path == "/status":
            return self._json({
                "gpu": "4060 (xspace mock)",
                "online": True,
                "tasks": len(TASKS),
                "mac_connected": 1,
                "orin_online": True,
                "orin_recording": False,
                "forwarded_mb": 42,
                "disk_gb": 0.5
            })
        # GET /task/{id}
        if path.startswith("/task/"):
            tid = path.split("/")[-1]
            task = TASKS.get(tid)
            if task:
                return self._json(task)
            return self._json({"error": "task not found"}, 404)
        # GET /json-list
        if path == "/json-list":
            import glob
            files = [os.path.basename(f) for f in glob.glob("/root/zmax-website/*.json")]
            return self._json(files)
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = self.path.rstrip("/")
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}

        if path == "/task":
            nodes = body.get("nodes", [])
            node_str = " ".join(nodes) if isinstance(nodes, list) else str(nodes)

            # Detect model from nodes
            model = "ACT"
            for m in ["SmolVLA", "VLA-T", "GR00T", "ACT"]:
                if m in node_str:
                    model = m
                    break

            info = INFERENCE_RESULTS.get(model, INFERENCE_RESULTS["ACT"])
            tid = str(uuid.uuid4())[:8]
            TASKS[tid] = {
                "id": tid,
                "status": "processing",
                "nodes": nodes if isinstance(nodes, list) else [],
                "model": info["model"],
                "hardware": info["hardware"],
                "location": info["location"],
                "steps": info["steps"],
                "created": time.time()
            }
            print(f"  📋 任务 {tid}: {model} · {len(TASKS[tid]['nodes'])}节点")
            # Auto-complete after 2s
            def complete():
                time.sleep(2)
                if tid in TASKS:
                    TASKS[tid]["status"] = "done"
                    TASKS[tid]["result"] = info["result"]
                    TASKS[tid]["timing"] = info["timing"]
                    print(f"  ✅ 任务 {tid} 完成: {model}")
            threading.Thread(target=complete, daemon=True).start()
            return self._json(TASKS[tid])

        if path == "/json-save":
            name = body.get("name", "")
            data = body.get("data", {})
            fpath = os.path.join("/root/zmax-website", os.path.basename(name))
            with open(fpath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return self._json({"ok": True, "name": os.path.basename(name)})

        if path == "/debug":
            nodes = body.get("nodes", [])
            return self._json({
                "step": "调试模式",
                "location": "4060 (xspace)",
                "variables": {"nodes": len(nodes), "model": "ACT"},
                "shapes": "[1,50,6]",
                "model_path": "/root/models/act_policy",
                "params": "52M"
            })

        return self._json({"error": "not found"}, 404)

if __name__ == "__main__":
    # Kill existing
    os.system("fuser -k 50053/tcp 2>/dev/null; sleep 0.5")
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"🧠 ComfyUI Mock Inference Server")
    print(f"   端口: {PORT}  →  nginx: /api/comfy/")
    print(f"   模型: ACT(48ms) | SmolVLA(257ms) | VLA-T(180ms) | GR00T(1.2s)")
    print(f"   Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹ 已停止")
