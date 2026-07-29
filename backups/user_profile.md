用户信息分两类: (1)需执行的指令 (2)知识共享(给全队存档)。共享信息可能无需立即执行,但需全员理解吸收。AI agent间无法直接通信,通过用户中转。
§
ComfyUI铁律v7:回退78f0c92→Python统一改(禁用sed)→部署前grep preset=1+node -e JS→ZF forward z在if外→MuJoCo+GPU分进程(exit139)→env.reset()返回(state,info)需render()取图→render负strides需np.copy()→ASPICE位置对调用TMP三级replace→localStorage保存破坏渲染→手动💾安全→__import__('glob')→AUTO_TRAIN_LIST[False]→WebSocket禁用→后端hang kill-9。侧栏分组无重复,禁toggle折叠。
§
"完成"协议: 任务完成后仅回复"完成"不解释。不说"试试""应该"。用户说"别动了""回退""不折腾了"立即停手。缩放功能已放弃(v4.0重构)。本地保存优先服务器存储。
§
修改ComfyUI铁律: ①git checkout干净版→Python统一改(不用sed)→node -e验证JS→grep -c确认preset→部署 ②绝不直接修改draw()函数(会破坏渲染),用CSS overlay替代 ③未声明变量是头号杀手(connected/stage/pipelineTimer必须var声明) ④重复代码删干净(多个listServerJSON/toggleConnect导致undefined) ⑤缩放用世界坐标+逆变换getPos,不走CSS transform
§
三人团队分工: web(我·4090训练·ComfyUI前端·ECS部署·PM·模型训练)·xspace(总工·4060·Orin真机·GitHub后端·GUI)·小芳(硬件·Mac中转·Orin采集·WebSocket·飞书) 通信链路:Orin(192.168.23.10:8765)→小芳Mac(192.168.23.1:8769)→ECS(39.102.211.79:50053)→4090(50054/50056) 心跳:POST /api/comfy/api/mac/heartbeat每5秒
§
静界Z-MAX CEO。团队:xspace(4060总工)·web(PM/前端/ECS)·小芳(Mac/Orin)。铁律:①链接纯文本禁**②回复简洁"完成"③完整指令无省略号④手机可操控⑤阻塞立即上报⑥3D页面要连贯运动+真实动画+双视角+音乐,打开即自动运行⑦移动端必须能用(点击启动按钮解决AudioContext)⑧UI显示异常立即修正。门户:15840273872/15840273872
§
CEO大倪偏好：首页「它石」→「供应商」；工具按钮要好使、迭代不能超过2轮；功能坏了直接说根因不要绕