#!/usr/bin/env python3
"""
Z-MAX Sys2 — VTLA 模型 4090 仿真验证脚本

验证项:
1. 模型加载测试 (GPU内存+加载时间)
2. 推理延迟测试 (P50/P99)
3. 触觉融合推理测试
4. 动作精度验证
"""
import sys, os, time, json
import numpy as np
import torch

sys.path.insert(0, '/root/lerobot-smolvla-lew/src')

RESULTS = {}
DEVICE = torch.device("cuda")

def test_gpu():
    """GPU 基础信息"""
    gpu = torch.cuda.get_device_properties(0)
    return {
        "gpu_name": gpu.name,
        "vram_total_gb": round(gpu.total_memory / 1e9, 1),
        "vram_free_gb": round(torch.cuda.mem_get_info()[0] / 1e9, 1),
    }

def test_model_load():
    """VTLA 模型加载"""
    from lerobot.policies.smolvla import SmolVLAPolicy
    from transformers import AutoTokenizer
    
    t0 = time.time()
    torch.cuda.reset_peak_memory_stats()
    
    model = SmolVLAPolicy.from_pretrained("lerobot/smolvla_base")
    model.to(DEVICE)
    model.eval()
    
    load_time = time.time() - t0
    vram_used = torch.cuda.max_memory_allocated() / 1e9
    params = sum(p.numel() for p in model.parameters()) / 1e6
    
    tokenizer = AutoTokenizer.from_pretrained(
        model.config.vlm_model_name if hasattr(model.config, 'vlm_model_name') 
        else "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
    )
    
    return {
        "load_time_s": round(load_time, 2),
        "vram_gb": round(vram_used, 2),
        "params_M": round(params, 0),
        "model": model,
        "tokenizer": tokenizer,
    }

def test_inference_latency(model, tokenizer, n_warmup=5, n_test=100):
    """推理延迟基准"""
    from lerobot.policies.smolvla.modeling_smolvla import resize_with_pad
    from lerobot.utils.constants import OBS_LANGUAGE_TOKENS, OBS_LANGUAGE_ATTENTION_MASK
    
    # 构造测试输入
    B = 1
    img = torch.rand(B, 3, 512, 512, device=DEVICE) * 2 - 1
    
    encoded = tokenizer("pick up the module", return_tensors="pt",
                        padding="max_length", max_length=48, truncation=True)
    
    batch = {
        "observation.images.camera1": img,
        "observation.images.camera2": torch.ones(B, 3, 512, 512, device=DEVICE) * -1,
        "observation.images.camera3": torch.ones(B, 3, 512, 512, device=DEVICE) * -1,
        "observation.state": torch.randn(B, 14, device=DEVICE),
        OBS_LANGUAGE_TOKENS: encoded["input_ids"].to(DEVICE),
        OBS_LANGUAGE_ATTENTION_MASK: encoded["attention_mask"].to(torch.bool).to(DEVICE),
    }
    
    # Warmup
    for _ in range(n_warmup):
        with torch.no_grad():
            _ = model.predict_action_chunk(batch)
    torch.cuda.synchronize()
    
    # Benchmark
    latencies = []
    for _ in range(n_test):
        t0 = time.time()
        with torch.no_grad():
            action = model.predict_action_chunk(batch)
        torch.cuda.synchronize()
        latencies.append((time.time() - t0) * 1000)
    
    latencies = np.array(latencies)
    return {
        "latency_mean_ms": round(latencies.mean(), 1),
        "latency_p50_ms": round(np.percentile(latencies, 50), 1),
        "latency_p99_ms": round(np.percentile(latencies, 99), 1),
        "latency_min_ms": round(latencies.min(), 1),
        "latency_max_ms": round(latencies.max(), 1),
        "fps": round(1000 / latencies.mean(), 1),
        "action_shape": list(action.shape),
    }

def test_tactile_fusion():
    """触觉编码器测试 (Sys2 VTLA 独有)"""
    try:
        sys.path.insert(0, '/root/lerobot-smolvla-lew/src')
        from lerobot.policies.zmax_sys2.modeling_zmax_sys2 import SimFeedback, VTLAInferenceEngine
        from lerobot.policies.zmax_sys2.configuration_zmax_sys2 import ZmaxSys2Config
        
        config = ZmaxSys2Config(vtla_model_path="lerobot/smolvla_base", enable_tactile=True)
        engine = VTLAInferenceEngine(config, DEVICE)
        engine.load()
        
        sim = SimFeedback(
            camera_rgb=np.random.rand(3, 480, 640).astype(np.float32),
            force_torque=np.array([0.1, 0.2, -2.5, 0.01, 0.02, 0.03], dtype=np.float32),
            tactile=np.random.rand(16).astype(np.float32) * 0.5,
            joint_states=np.zeros(14, dtype=np.float32),
            gripper_pos=0.5,
            task_text="insert the optical module into test chamber",
        )
        
        t0 = time.time()
        result = engine.predict(sim)
        elapsed = (time.time() - t0) * 1000
        
        return {
            "tactile_fusion_ok": True,
            "latency_ms": round(elapsed, 1),
            "action_dim": len(result.action),
            "task_type": result.task_type,
            "model_used": result.model_used,
        }
    except Exception as e:
        return {"tactile_fusion_ok": False, "error": str(e)}

def main():
    print("=" * 60)
    print("Z-MAX Sys2 · VTLA模型 4090 仿真验证")
    print("=" * 60)
    
    # 1. GPU
    print("\n[1/4] GPU 检测...")
    gpu = test_gpu()
    print(f"  GPU: {gpu['gpu_name']}")
    print(f"  VRAM: {gpu['vram_total_gb']} GB total, {gpu['vram_free_gb']} GB free")
    RESULTS['gpu'] = gpu
    
    # 2. 模型加载
    print("\n[2/4] VTLA 模型加载...")
    load = test_model_load()
    print(f"  参数量: {load['params_M']:.0f}M")
    print(f"  加载时间: {load['load_time_s']}s")
    print(f"  GPU显存: {load['vram_gb']} GB")
    RESULTS['load'] = {k: v for k, v in load.items() if k not in ('model', 'tokenizer')}
    
    # 3. 推理延迟
    print("\n[3/4] 推理延迟基准测试...")
    lat = test_inference_latency(load['model'], load['tokenizer'])
    print(f"  平均延迟: {lat['latency_mean_ms']}ms")
    print(f"  P99延迟:  {lat['latency_p99_ms']}ms")
    print(f"  帧率:     {lat['fps']} FPS")
    RESULTS['latency'] = lat
    
    # 4. 触觉融合
    print("\n[4/4] 触觉融合推理...")
    tactile = test_tactile_fusion()
    if tactile.get('tactile_fusion_ok'):
        print(f"  ✅ 触觉融合成功: {tactile['latency_ms']}ms, task={tactile['task_type']}")
    else:
        print(f"  ⚠️ 触觉融合: {tactile.get('error', 'unknown')}")
    RESULTS['tactile'] = tactile
    
    # 评估
    print("\n" + "=" * 60)
    print("📊 验证报告")
    print("=" * 60)
    
    checks = []
    if load['vram_gb'] < 3.0:
        checks.append(("✅", f"GPU显存 {load['vram_gb']}GB < 3GB 目标"))
    else:
        checks.append(("❌", f"GPU显存 {load['vram_gb']}GB > 3GB 目标"))
    
    if lat['latency_p99_ms'] < 100:
        checks.append(("✅", f"推理延迟 P99={lat['latency_p99_ms']}ms < 100ms 目标"))
    else:
        checks.append(("⚠️", f"推理延迟 P99={lat['latency_p99_ms']}ms > 100ms 目标"))
    
    if tactile.get('tactile_fusion_ok'):
        checks.append(("✅", "触觉融合推理正常"))
    else:
        checks.append(("⚠️", f"触觉融合: {tactile.get('error')}"))
    
    for icon, msg in checks:
        print(f"  {icon} {msg}")
    
    # 保存报告
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/vtla_validation.json", "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    print(f"\n📄 报告已保存: outputs/vtla_validation.json")

if __name__ == "__main__":
    main()
