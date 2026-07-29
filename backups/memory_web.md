工艺文档铁律: 绝对禁止编造数据。所有数字(重量/节拍/人数)必须有用户提供的产线数据支撑，没有来源就标注"待确认"或留空。用户曾追问"50kg""1盘2~3kg"来源，全部是编的。800G DR8真实工序: DA1~DA4贴片+WB金线键合+PEI Cover+隔离器+激光分板，不存在"Adapter""分晶""FVI"。
§
dds-skill-master中D435已修复为D405(Orin实际用RealSense D405)。首页性能铁律:永不嵌入实时3D iframe(多WebGL上下文导致滚动延迟)，用静态预览+点击跳转。
§
首页规范: Hero→KPI(±0.05/>99%/>1kHz/<15s)→产品→核心技术→流水线→研发→数据空间(上传区)→全站导航(6类30+链接)→Footer。手机:顶部PPTX/Word操作条+footer大字。禁技术参数/打赏/3D iframe。
§
CEO偏好(07-27最终): Z700品牌·首页禁技术参数·链接纯文本·全静态HTML·contenteditable全绑定·工具栏底部·聊天全DeepSeek LLM禁模板·不@不说话·名无@也识别·30条全量上下文·纯数30以下接龙·像朋友聊天·不确定就说不知道
§
制造原子技能242条·11大类(XPO59/NPO51/载具43/装配15/操作15/感知15/质量10/安全10/物流9/泛化8/导航7)。数据源:制造业场景_具身机器人原子技能库0724.xlsx(19sheet)。API:dds-atomic-api.php。所有技能ID/描述保持一致。
§
PPT/提案v2.7.5: 智蜂模板·白底蓝强调·21页(10+11附录)·Pt()不双重传参·PHP禁shell_exec→Python预生成。factory5页。聊天室ws代理8765。飞书文档: 4种API全失败→用户粘贴唯一路径。Draw.io程序化生成已验证(dds-architecture.drawio 21KB)。
§
产线: COC(18道·储翰·15人),OE(72站·苏州·75人),MOD(26站·114人),WH(7站)。机器人:Z100L(L3轮式双臂≤10kg搬运),Z700F(L2固定插拔),Z700F+AOI(L2目检),Z700(L4立项申请·轮式≤10kg·泛化)。分配:目检→Z700F+AOI,上下料→Z100L,自动化设备→固定L2,巡检泛化→Z700。双臂≤10kg,推理<70ms。
§
dds-editor: 静态HTML·contenteditable全data绑定·autoSave800ms+batchPOST·changelog100条可恢复·工具栏底部不悬浮
§
聊天v3.1.1-ai: ws-server:8765(asyncLock)→wss://(nginx443)→chat.html+watcher(DeepSeek)。铁律:并发无锁→清空;ufw→wss;PHP→644;中文\\b→(?<![a-zA-Z])name;纯数30以下接龙。脚本:chat-watcher.py参数web|xspace|xiaofang
§
DDS全体系: dds.db(15表)→5个PHP API→cron/2min→dds-global.js(12KB)→全站同步。242条原子技能。dds-3d-space.html硬编码需改SQLite驱动。架构图: dds-architecture.drawio(5层)+dds-model-pipeline.drawio。Draw.io程序化: Python写XML→ElementTree验证。<Array>内mxPoint自闭合需</Array>闭合。
§
飞书文档API全部失败: curl→登录页, tenant_token→404, app_token→404, docx API→1770002 not found。根因: app未安装到dataworld企业。唯一路径: 用户复制粘贴内容或设"互联网公开"。
§
draw.io postMessage API 导出格式: html|xmlsvg|svg|xmlpng|png|jpeg，没有xml格式。保存用xmlsvg原样存服务器(draw.io原生支持加载)，导出.drawio直接fetch服务器文件下载。不需要extractDrawioXml。xmlpng返回data URI会污染文件。
§
更新drawio对应HTML前必须先完整解析.drawio文件(base64→zlib→URL-decode→提取mxCell)。用户会逐项核对架构/箭头/位置。反例:并行汇聚画成串行被纠正2次。箭头必须纯水平,禁斜向/纵向。
§
供应商:供应商A=白盒模型(可解释AI·视觉策略),供应商B=原子动作集成(L2·动作组合引擎)。智蜂=VLA大模型·AI训练R量产。命名v2.8.1:公司概况→产品概况,创立→立项,DDS管线→全局数据管线,专用小模型→工厂适配模型。