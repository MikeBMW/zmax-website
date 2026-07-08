# Z-MAX Website — datadrive.world

Z-MAX 产品展示网站，部署于阿里云 ECS WordPress (Astra + Elementor)。

```
datadrive.world/z-max  →  Z-MAX 产品页面 (WP ID: 501)
```

## 目录结构

```
zmax-website/
├── README.md
├── .gitignore
├── animations/           # Three.js 3D 动画
│   ├── robot.html        #   5工位产线: 珞石SR5-C + DH夹爪
│   └── robot2.html       #   Z700 轮式双臂 + 老化箱操作
├── nginx/                # Nginx 配置
│   ├── datadrive.world.conf
│   └── rewrite.conf
├── wordpress/            # WordPress 页面内容
│   └── page-501-z-max.html
├── deploy/
│   └── deploy.sh         # 一键部署脚本
└── backups/              # 历史备份
```

## 快速部署

```bash
# 1. 把文件上传到 ECS
bash deploy/deploy.sh

# 2. 刷新 CDN/缓存
# 在 WP 页面里 bump ?v=N 版本号
```

## ECS 连接

| 项目 | 值 |
|------|-----|
| IP | 39.102.211.79 |
| 路径 | /www/wwwroot/datadrive.world/ |
| 宝塔 | https://39.102.211.79:41000/agentFace |
| DB | xSpace / 127.0.0.1 |

## 注意事项

- **两个 nginx**: 只用 宝塔 nginx `/www/server/nginx/sbin/nginx -s reload`
- **WP permalink**: `/index.php/%postname%/` + try_files `/index.php$uri?$args`
- **iframe 缓存**: robot.html 用 `?v=N` 版本号破缓存
- **动画坐标**: robot.html 坐标系 origin=机械臂底座, X↓前 Y←左 Z↑上

## 机械臂动画技术栈

- Three.js 0.157 (CDN: unpkg)
- 手动 IK (2-link, law of cosines)
- 5工位产线循环 (入料→扫码→刷程序→AOI→出料)
- robot2: 8阶段老化箱操作循环
