#!/usr/bin/env python3
"""
Z-MAX 任务看板自动更新脚本
每小时运行一次，更新任务状态并推送 kanban.html 到 ECS

用法: python3 update_kanban.py
"""
import os
import json
import subprocess
import datetime

ECS = "root@39.102.211.79"
ROOT = "/www/wwwroot/datadrive.world"
ECS_PASS = "Nix19789"
LOCAL_KANBAN = "/root/zmax-website/kanban.html"

def get_git_status():
    """获取各仓库状态"""
    repos = {
        "zmax-website": "/root/zmax-website",
        "lerobot-smolvla-lew": "/root/lerobot-smolvla-lew",
        "Isaac-GR00T": "/root/Isaac-GR00T",
    }

    status = {}
    for name, path in repos.items():
        if not os.path.isdir(path):
            status[name] = {"status": "not_found"}
            continue
        try:
            # Current branch
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=path, text=True
            ).strip()

            # Last commit
            commit = subprocess.check_output(
                ["git", "log", "--oneline", "-1", "--format=%h %s"],
                cwd=path, text=True
            ).strip()

            # Modified files
            mod = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=path, text=True
            ).strip()

            status[name] = {
                "branch": branch,
                "last_commit": commit,
                "dirty": bool(mod),
                "modified": mod[:200] if mod else "",
            }
        except Exception as e:
            status[name] = {"status": f"error: {e}"}

    return status

def update_kanban_html():
    """
    更新 kanban.html 中的任务数据
    读取本地状态并注入到 HTML
    """
    status = get_git_status()
    now = datetime.datetime.now()  # 系统本地已是 CST，不需要额外加偏移

    # 读取模板
    with open(LOCAL_KANBAN, 'r') as f:
        html = f.read()

    # 注入更新时间戳（刷新缓存用）—— 每次替换整行避免累积
    ts = now.strftime("%Y-%m-%d %H:%M CST")
    import re
    html = re.sub(
        r'id="update-time">.*?</span>',
        f'id="update-time">🔄 {ts}</span>',
        html,
        flags=re.DOTALL
    )

    # 添加仓库状态注释
    status_json = json.dumps(status, ensure_ascii=False, indent=2)
    status_comment = f"\n<!-- AUTO-GENERATED STATUS\n{status_json}\n-->"

    # 确保不重复注入
    if "<!-- AUTO-GENERATED STATUS" in html:
        import re
        html = re.sub(r'<!-- AUTO-GENERATED STATUS.*?-->', status_comment, html, flags=re.DOTALL)
    else:
        html = html.replace('</body>', f'{status_comment}\n</body>')

    with open(LOCAL_KANBAN, 'w') as f:
        f.write(html)

    return html

def deploy():
    """部署到 ECS"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Updating kanban...")

    # 更新 HTML
    update_kanban_html()

    # 上传到 ECS
    try:
        subprocess.run([
            "sshpass", "-p", ECS_PASS,
            "scp", "-o", "StrictHostKeyChecking=no",
            LOCAL_KANBAN,
            f"{ECS}:{ROOT}/kanban.html"
        ], check=True, timeout=30)
        print(f"  ✅ kanban.html → {ECS}:{ROOT}/kanban.html")

        # 设置权限
        subprocess.run([
            "sshpass", "-p", ECS_PASS,
            "ssh", "-o", "StrictHostKeyChecking=no",
            ECS,
            f"chmod 644 {ROOT}/kanban.html"
        ], check=True, timeout=10)
        print("  ✅ permissions set")

    except subprocess.CalledProcessError as e:
        print(f"  ❌ Deploy failed: {e}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    deploy()
