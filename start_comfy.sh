#!/bin/bash
# web端 comfy mock 服务启动 (50058, 127.0.0.1)
pkill -f 'comfyui_mock_ecs.py' 2>/dev/null
sleep 1
cd /root/zmax-website
setsid nohup python3 comfyui_mock_ecs.py > comfy_mock.log 2>&1 < /dev/null &
sleep 2
ps aux | grep comfyui_mock | grep -v grep | head -1
tail -2 comfy_mock.log
