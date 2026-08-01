#!/usr/bin/env python3
"""ECS本地通路验证Mock服务 — 根据实际节点检测模型"""
import json, time
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 50058

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

def detect_model(nodes):
    """根据节点名检测模型。节点名中可能包含 ACT/SmolVLA/VLA-T/GR00T。"""
    if not nodes:
        return "ACT"
    node_str = " ".join(nodes) if isinstance(nodes, list) else str(nodes)
    # 按关键词精确匹配，ACT排最后做默认
    for m in ["SmolVLA", "VLA-T", "GR00T"]:
        if m in node_str:
            return m
    return "ACT"  # 默认，也是兜底


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def _ok(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_GET(self):
        if self.path in ('/status', '/api/comfy/status'):
            self._ok({
                'gpu': 'ECS本地通路验证',
                'mode': 'local-passthrough',
                'online': True
            })
        elif self.path in ('/health', '/api/comfy/health'):
            self._ok({'status': 'ok'})
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        cl = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(cl)) if cl > 0 else {}
        if self.path in ('/task', '/api/comfy/task'):
            nodes = body.get('nodes', [])
            model = detect_model(nodes)
            info = INFERENCE_RESULTS.get(model, INFERENCE_RESULTS["ACT"])
            self._ok({
                'id': 'local-' + str(int(time.time() * 1000)),
                'status': 'done',
                'nodes': len(nodes),
                'model': info['model'],
                'hardware': info['hardware'],
                'location': info['location'],
                'steps': info['steps'],
                'result': info['result'],
                'timing': info['timing'],
                'mode': 'local-passthrough'
            })
        elif self.path in ('/debug', '/api/comfy/debug'):
            nodes = body.get('nodes', [])
            model = detect_model(nodes)
            self._ok({
                'step': '调试模式',
                'location': 'ECS-local',
                'model': model,
                'variables': {'nodes': len(nodes), 'model': model}
            })
        else:
            self.send_response(404); self.end_headers()


if __name__ == '__main__':
    import os
    print(f'[mock-comfy] port {PORT} · 模型自动检测: ACT(默认) | SmolVLA | VLA-T | GR00T')
    HTTPServer(('127.0.0.1', PORT), MockHandler).serve_forever()
