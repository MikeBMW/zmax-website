/**
 * DDS Global Data Layer · SQLite驱动
 * 数据源：dds.db → dds-export.py 导出
 * 版本：v2.6 · 2026-07-26
 */
window.DDS = {
  company: {
    name: "智蜂创元",
    name_en: "ZFCY",
    product: "Z-700",
    product_tag: "具身智能 · 光模块精密制造",
    domain: "datadrive.world",
    year: "2026",
    city: "",
  },
  kpi: {
    precision: { value:"±0.02", unit:"mm", label:"重复定位精度", icon:"🎯" },
    yield_rate: { value:">99", unit:"%", label:"关键工序良率", icon:"✅" },
    force_bw: { value:">10", unit:"kHz", label:"力控闭环带宽", icon:"⚡" },
    cycle_time: { value:"<15", unit:"s", label:"单次插拔节拍", icon:"⏱️" },
  },
  robots: {
    Z700: { id:"Z700", name:"Z700 轮式双臂机器人", level:"L4", level_label:"L4 旗舰 立项中", desc:"轮式底盘自主导航，双臂协同精细操作。覆盖老化箱插拔、产线巡检、多工位联动作业。全自主执行+自适应+自恢复。", icon:"🤖", page:"/robot2.html", color:"#00d4aa" },
    Z700F: { id:"Z700F", name:"Z700F 固定式精密插拔", level:"L2", level_label:"L2 基线，已到货", desc:"单工位高精度插拔产线。珞石SR5-C机械臂+DH夹爪，5工位循环：入料→扫码→刷程序→AOI检测→出料。", icon:"🔧", page:"/robot.html", color:"#ff6b35" },
    Z100L: { id:"Z100L", name:"Z100L 轮式双臂搬运机器人", level:"L3", level_label:"已立项", desc:"轮式双臂·料笼/料盘搬运专用，双臂负载≤10kg。", icon:"📦", page:"", color:"#58a6ff" },
    Z700F_AOI: { id:"Z700F_AOI", name:"Z系列 + AOI 目检机器人", level:"L2", level_label:"适配中", desc:"精密AOI目检专用。显微镜检、外观检查、缺陷判定。", icon:"🔬", page:"", color:"#a371f7" },
  },
  systems: {
    sys0: { id:"Sys0", name:"Sys0 · 硬件基座", hardware:"Orin Nano", gpu:"—", ram:"8GB", role:"终端执行 · 传感器采集 · 机械臂控制", model:"ROS2 · SR5-C · 6轴+8传感器", color:"#d4a800" },
    sys1: { id:"Sys1", name:"Sys1 · 端边推理", hardware:"RTX 4060", gpu:"8GB", ram:"16GB", role:"边缘推理引擎 · 实时力控闭环", model:"VLA-T / GR00T / ACT / SmolVLA / LeWM 五引擎切换", color:"#58a6ff" },
    sys2: { id:"Sys2", name:"Sys2 · 云端训练", hardware:"RTX 4090", gpu:"24GB", ram:"32GB", role:"大模型训练+推理 · 全产线智能决策", model:"SmolVLA 450M · GR00T 7B · 云端训练闭环", color:"#00d4aa" },
    edge: { id:"Edge", name:"Edge · 端侧", hardware:"Mac M1 · Orin Nano", gpu:"—", ram:"—", role:"现场执行 · 7×24可靠运行", model:"SmolVLA-INT8量化 · <15ms推理", color:"#a371f7" },
  },
  models: {
    SmolVLA: { name:"SmolVLA", full_name:"SmolVLA 视觉-语言-动作模型", params:"450M", type:"视觉-语言-动作", deployment:"Sys11 · Sys2", desc:"端到端视觉-语言-动作。支持零样本泛化。", color:"#a371f7" },
    GR00T: { name:"GR00T", full_name:"GR00T N1.7 通用机器人基础模型", params:"7B", type:"通用机器人基础模型", deployment:"Sys2", desc:"NVIDIA GR00T N1.7-3B。DiT 1.09B。封装16种具身操作。", color:"#00d4aa" },
    ACT: { name:"ACT", full_name:"Action Chunking Transformer", params:"52M", type:"动作分块Transformer", deployment:"Sys1 (4060)", desc:"<10ms推理。实时力控闭环>1kHz。", color:"#58a6ff" },
    LeWM: { name:"LeWM", full_name:"LeWorldModel 世界模型", params:"—", type:"世界模型", deployment:"Sys12", desc:"与SmolVLA深度耦合。感知→预测→决策→执行完整闭环。", color:"#d4a800" },
    VLA_T: { name:"VLA-T", full_name:"VLA-T 触觉力控模型", params:"—", type:"视觉-语言-动作-触觉", deployment:"Sys21", desc:"3D感知+力控+触觉编码器。", color:"#ff6b35" },
  },
  hardware: {
    camera: { model:"RealSense D405", type:"RGB-D深度相机", spec:"1920×1080 · 30fps · 0.1-10m" },
    robot_arm: { model:"珞石 SR5-C", type:"6轴机械臂", spec:"±0.02mm重复精度 · 5kg负载" },
    gripper: { model:"DH夹爪", type:"电动平行夹爪", spec:"" },
    force_sensor: { model:"六维力传感器", type:"F/T传感器", spec:"Fx/Fy/Fz/Tx/Ty/Tz · ±0.1N · 1kHz" },
    tactile: { model:"指尖触觉阵列", type:"16通道触觉", spec:"16bit · 1kHz" },
  },
  factory: {
    product: "800G DR8",
    product_pn: "260-B4103",
    zones: [
      { id:"coc", name:"COC 基板区", color:"#f0a500", page:"/coc-process.html", stations:"I101-I124", count:24 },
      { id:"mod", name:"MOD 模块组装区", color:"#58a6ff", page:"/mod-process.html", stations:"I197-I222", count:26 },
      { id:"oe", name:"OE 光引擎区", color:"#ff6b35", page:"/oe-process.html", stations:"I125-I196", count:72 },
      { id:"wh", name:"WH 仓库物流区", color:"#3fb950", page:"/wh-process.html", stations:"I223-I228+I500", count:7 },
    ],
    total_stations: 228,
    final_inspection: "I500",
  },
  dds_skills: {
    XPO高密可插拔光学: { count:59, id_range:"", color:"#ff6b35", icon:"🔌", label:"XPO高密可插拔光学", desc:"59条 · 均优先382分" },
    NPO近封装光学: { count:51, id_range:"", color:"#a371f7", icon:"🔮", label:"NPO近封装光学", desc:"51条 · 均优先376分" },
    感知定位: { count:15, id_range:"", color:"#58a6ff", icon:"👁️", label:"感知定位", desc:"15条 · 均优先261分" },
    视觉检测: { count:10, id_range:"", color:"#a371f7", icon:"🔬", label:"视觉检测", desc:"10条 · 均优先299分" },
    安全集成: { count:10, id_range:"", color:"#ff4444", icon:"🛡️", label:"安全集成", desc:"10条 · 均优先309分" },
    载具物流: { count:9, id_range:"", color:"#ff6b35", icon:"🚛", label:"载具物流", desc:"9条 · 均优先387分" },
    学习泛化: { count:8, id_range:"", color:"#00d4aa", icon:"🧠", label:"学习泛化", desc:"8条 · 均优先256分" },
    移动导航: { count:7, id_range:"", color:"#58a6ff", icon:"🗺️", label:"移动导航", desc:"7条 · 均优先237分" },
    操作动作: { count:73, id_range:"None", color:"#f0a500", icon:"🤖", label:"操作动作", desc:"机器人操作与载具动作" },
  },
  pipeline: {
    name: "数据流水线 · Orin→MAC→4090", version: "2.0",
    phases: [
      { name:"采集", node:"Orin Nano", duration:30, icon:"📡" },
      { name:"转发", node:"MAC", duration:5, icon:"💻" },
      { name:"训练", node:"4090", duration:60, icon:"🧠" },
    ],
  },
  roadmap: [
    { version:"v1.0", timeline:"2026Q3", name:"单工位验证", desc:"光模块插拔 · 固定轨迹 · Orin Nano边缘部署 · 力控±0.02mm", color:"#00d4aa" },
    { version:"v1.5", timeline:"2026Q4", name:"多工位联线", desc:"抓取→插拔→AOI×6全链条 · Sys1端侧VLA-T力控闭环 · 99%+良率", color:"#58a6ff" },
    { version:"v2.0", timeline:"2027Q2", name:"全产线智能", desc:"多机协同 · 换型自适配 · VLA-T+GR00T · 云端训练闭环", color:"#a371f7" },
  ],
  links: {
    github: "https://github.com/MikeBMW/lerobot-smolvla-lew",
    zmax: "https://github.com/MikeBMW/zmax-website",
    hybrid: "https://github.com/MikeBMW/zmax-website",
    deepseek: "https://platform.deepseek.com/usage",
    gpu_console: "https://console.compshare.cn/uaccount/costcenter",
    wandb: "https://wandb.ai/xspace/zmax-hjepa",
  },
  theme: {
    bg: "#06080d",
    card: "#0d1117",
    border: "#1a1f2b",
    accent: "#00d4aa",
    accent2: "#00ffcc",
    text: "#c8d1d9",
    muted: "#8b949e",
    danger: "#ff4444",
    warning: "#d4a800",
    info: "#58a6ff",
  },
};

window.DDS.getKPI = function(key) { return this.kpi[key]; };
window.DDS.getRobot = function(id) { return this.robots[id]; };
window.DDS.getSystem = function(id) { return this.systems[id]; };
window.DDS.getModel = function(id) { return this.models[id]; };
window.DDS.getZone = function(id) { return this.factory.zones.find(function(z){return z.id===id;}); };

console.log("DDS Global · SQLite同步 · v" + window.DDS.company.year + " · " + window.DDS.factory.product);