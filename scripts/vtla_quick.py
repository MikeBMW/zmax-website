#!/usr/bin/env python3.12
"""VTLA quick validation — direct model load via transformers"""
import sys, time, json, os
sys.path.insert(0, '/root/lerobot-smolvla-lew/src')

import torch, numpy as np
DEVICE = torch.device("cuda")

print("=" * 60)
print("Z-MAX Sys2 · VTLA 4090 验证 (Python 3.12)")
print("=" * 60)

# GPU
gpu = torch.cuda.get_device_properties(0)
print(f"\n[1] GPU: {gpu.name}")
print(f"    VRAM: {gpu.total_memory/1e9:.1f}GB total, {torch.cuda.mem_get_info()[0]/1e9:.1f}GB free")

# Load model
print("\n[2] Loading SmolVLA...")
t0 = time.time()
torch.cuda.reset_peak_memory_stats()

from lerobot.policies.smolvla import SmolVLAPolicy
model = SmolVLAPolicy.from_pretrained("/root/models/smolvla_base")
model.to(DEVICE).eval()

params = sum(p.numel() for p in model.parameters()) / 1e6
vram = torch.cuda.max_memory_allocated() / 1e9
load_t = time.time() - t0
print(f"    Params: {params:.0f}M")
print(f"    VRAM:   {vram:.2f}GB")
print(f"    Load:   {load_t:.1f}s")

# Inference benchmark
print("\n[3] Inference benchmark...")
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolVLM2-500M-Video-Instruct")
from lerobot.policies.smolvla.modeling_smolvla import resize_with_pad
from lerobot.utils.constants import OBS_LANGUAGE_TOKENS, OBS_LANGUAGE_ATTENTION_MASK

B = 1
img = resize_with_pad(torch.rand(B, 3, 480, 640, device=DEVICE), 512, 512, pad_value=0) * 2 - 1
enc = tokenizer("insert optical module", return_tensors="pt", padding="max_length", max_length=48, truncation=True)
batch = {
    "observation.images.camera1": img,
    "observation.images.camera2": torch.ones(B, 3, 512, 512, device=DEVICE) * -1,
    "observation.images.camera3": torch.ones(B, 3, 512, 512, device=DEVICE) * -1,
    "observation.state": torch.randn(B, 14, device=DEVICE),
    OBS_LANGUAGE_TOKENS: enc["input_ids"].to(DEVICE),
    OBS_LANGUAGE_ATTENTION_MASK: enc["attention_mask"].to(torch.bool).to(DEVICE),
}

# Warmup
for _ in range(5):
    with torch.no_grad(): model.predict_action_chunk(batch)
torch.cuda.synchronize()

# Test
lats = []
for _ in range(50):
    t0 = time.time()
    with torch.no_grad():
        action = model.predict_action_chunk(batch)
    torch.cuda.synchronize()
    lats.append((time.time()-t0)*1000)

lats = np.array(lats)
print(f"    Mean:  {lats.mean():.1f}ms")
print(f"    P50:   {np.percentile(lats,50):.1f}ms")
print(f"    P99:   {np.percentile(lats,99):.1f}ms")
print(f"    FPS:   {1000/lats.mean():.1f}")
print(f"    Action: {list(action.shape)}")

# Check target
checks = []
if vram < 3: checks.append(("✅", f"VRAM {vram:.1f}GB < 3GB"))
else: checks.append(("❌", f"VRAM {vram:.1f}GB >= 3GB"))
if lats.mean() < 100: checks.append(("✅", f"Latency {lats.mean():.0f}ms < 100ms"))
else: checks.append(("⚠️", f"Latency {lats.mean():.0f}ms >= 100ms"))

print(f"\n{'='*60}")
print("📊 验证结果")
print(f"{'='*60}")
for icon, msg in checks: print(f"  {icon} {msg}")

result = {"gpu": gpu.name, "params_M": round(params), "vram_gb": round(vram,2),
          "load_s": round(load_t,1), "latency_ms": round(lats.mean(),1),
          "p99_ms": round(np.percentile(lats,99),1), "fps": round(1000/lats.mean(),1)}
os.makedirs("outputs", exist_ok=True)
json.dump(result, open("outputs/vtla_validation.json","w"), indent=2)
print(f"\n📄 outputs/vtla_validation.json")
print("✅ VTLA validation complete!")
