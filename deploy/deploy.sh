#!/bin/bash
# ==========================================
# Z-MAX Website 一键部署到 datadrive.world
# 用法:
#   export ECS_PASS="Nix19789"
#   export DB_PASS="Nix2.7@1"
#   bash deploy.sh
# 依赖: sshpass
# ==========================================
set -e

ECS="root@39.102.211.79"
ROOT="/www/wwwroot/datadrive.world"
NGINX_CONF="/www/server/panel/vhost/nginx/datadrive.world.conf"
REWRITE_CONF="/www/server/panel/vhost/rewrite/datadrive.world.conf"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

SSH="sshpass -p '${ECS_PASS:?请 export ECS_PASS}' ssh -o StrictHostKeyChecking=no"
SCP="sshpass -p '${ECS_PASS:?请 export ECS_PASS}' scp -o StrictHostKeyChecking=no"
SQL="mysql -u xSpace -p'${DB_PASS:?请 export DB_PASS}' -h 127.0.0.1 xSpace"

echo "=== Z-MAX Website Deploy ==="

echo "[1/5] 上传动画..."
$SCP "$REPO_DIR/animations/robot.html"  "$ECS:$ROOT/robot.html"
$SCP "$REPO_DIR/animations/robot2.html" "$ECS:$ROOT/robot2.html"
$SSH "$ECS" "chmod 644 $ROOT/robot.html $ROOT/robot2.html"
echo "  ✅ robot.html + robot2.html"

echo "[2/5] 同步到 uploads..."
$SSH "$ECS" "cp $ROOT/robot.html $ROOT/wp-content/uploads/robot.html; cp $ROOT/robot2.html $ROOT/wp-content/uploads/robot2.html 2>/dev/null; true"
echo "  ✅"

echo "[3/5] 上传 nginx 配置..."
$SCP "$REPO_DIR/nginx/datadrive.world.conf" "$ECS:$NGINX_CONF"
$SCP "$REPO_DIR/nginx/rewrite.conf"         "$ECS:$REWRITE_CONF"
echo "  ✅"

echo "[4/5] 重载 nginx (宝塔)..."
$SSH "$ECS" '/www/server/nginx/sbin/nginx -s reload -c /www/server/nginx/conf/nginx.conf'
echo "  ✅"

echo "[5/5] Bump 版本号..."
CURRENT_V=$($SSH "$ECS" "$SQL -N -e \"SELECT post_content FROM wp_posts WHERE ID=501\"" 2>/dev/null | grep -oP 'robot\.html\?v=\K\d+' || echo 0)
NEW_V=$((CURRENT_V + 1))
echo "  v=$CURRENT_V → v=$NEW_V"

$SSH "$ECS" "
B64=\$($SQL -N -e \"SELECT TO_BASE64(post_content) FROM wp_posts WHERE ID=501\")
DECODED=\$(echo \"\$B64\" | base64 -d)
UPDATED=\$(echo \"\$DECODED\" | sed 's|robot\.html?v=$CURRENT_V|robot.html?v=$NEW_V|g')
NEWB64=\$(echo \"\$UPDATED\" | base64 -w0)
$SQL -e \"UPDATE wp_posts SET post_content=FROM_BASE64('\$NEWB64') WHERE ID=501\"
echo '  ✅ WP 页面已更新'
"

echo ""
echo "========================================"
echo "  部署完成!  https://datadrive.world/z-max"
echo "========================================"
