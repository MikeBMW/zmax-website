#!/bin/bash
# Orin 自动推流 — 每秒抓一帧推到 ECS
# 在 Orin 上运行: nohup bash orin_stream.sh &
ECS_HOST="root@39.102.211.79"
ECS_PATH="/www/wwwroot/datadrive.world/orin_realtime.jpg"
ECS_PASS="Nix19789"

while true; do
  # 抓取 RealSense D405 当前帧
  python3 -c "
import pyrealsense2 as rs, numpy as np, cv2
p=rs.pipeline();p.start()
f=p.wait_for_frames()
c=f.get_color_frame()
img=np.asanyarray(c.get_data())
_,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,60])
with open('/tmp/orin_frame.jpg','wb') as fh:fh.write(buf)
p.stop()
" 2>/dev/null
  
  # 推到 ECS
  sshpass -p "$ECS_PASS" scp -o StrictHostKeyChecking=no -o ConnectTimeout=3 \
    /tmp/orin_frame.jpg ${ECS_HOST}:${ECS_PATH} 2>/dev/null
  
  sleep 1
done
