#!/bin/bash
# Z-MAX 三库协同自动推送
# 用法: bash sync_all.sh "变更说明"

MSG="${1:-auto sync}"
DATE=$(date +%Y-%m-%d_%H:%M)
VER="v3.9"

echo "=== Z-MAX 协同推送 $DATE ==="

# 1. zmax-website
cd /root/zmax-website
git add -A
git commit -m "[$VER] $MSG · $DATE" 2>/dev/null
git push origin main 2>&1 | tail -1
echo "✅ zmax-website"

# 2. lerobot-smolvla-lew (web branch)
cd /root/lerobot-smolvla-lew
git add -A
git commit -m "[$VER] $MSG · $DATE" 2>/dev/null
git push origin web 2>&1 | tail -1
echo "✅ lerobot-smolvla-lew"

# 3. zmax-data-pipeline
if [ -d /root/zmax-data-pipeline ]; then
  cd /root/zmax-data-pipeline
  git pull origin main 2>/dev/null
  git add -A
  git commit -m "[$VER] $MSG · $DATE" 2>/dev/null
  git push origin main 2>&1 | tail -1
  echo "✅ zmax-data-pipeline"
fi

echo "=== 推送完成 ==="
