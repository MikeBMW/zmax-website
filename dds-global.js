/**
 * DDS Global Data Layer · 全局数据中心
 * 
 * 单文件改一处，全站自动同步。
 * 所有页面引用：<script src="/dds-global.js"></script>
 * 
 * 读取方式：window.DDS.kpi.precision.value
 * 版本：v2.5 · 2026-07-26
 */
window.DDS = {

  /* ═══════════════════════════════════════════
   *  公司信息
   * ═══════════════════════════════════════════ */
  company: {
    name:       "智蜂创元",
    name_en:    "ZFCY",
    product:    "Z-MAX",
    product_tag:"具身智能 · 光模块精密制造",
    domain:     "datadrive.world",
    year:       "2026",
    city:       "",
  },

  /* ═══════════════════════════════════════════
   *  KPI 指标（唯一来源）
   * ═══════════════════════════════════════════ */
  kpi: {
    precision:  { value:"±0.02", unit:"mm",   label:"插拔精度",     icon:"🎯" },
    yield_rate: { value:">99",   unit:"%",    label:"关键工序良率",  icon:"✅" },
    force_bw:   { value:">10",   unit:"kHz",  label:"力控闭环带宽",  icon:"⚡" },
    cycle_time: { value:"<5",    unit:"s",    label:"单次插拔节拍",  icon:"⏱️" },
  },

  /* ═══════════════════════════════════════════
   *  机器人产品线
   * ═══════════════════════════════════════════ */
  robots: {
    Z700: {
      id:          "Z700",
      name:        "Z700 轮式双臂机器人",
      level:       "L4",
      level_label: "L4 旗舰",
      desc:        "轮式底盘自主导航，双臂协同精细操作。覆盖老化箱插拔、产线巡检、多工位联动作业。全自主执行+自适应+自恢复。",
      icon:        "🤖",
      page:        "/robot2.html",
      color:       "#00d4aa",
    },
    Z700F: {
      id:          "Z700F",
      name:        "Z700F 固定式精密插拔",
      level:       "L2",
      level_label: "L2 基线",
      desc:        "单工位高精度插拔产线。珞石SR5-C机械臂+DH夹爪，5工位循环：入料→扫码→刷程序→AOI检测→出料。",
      icon:        "🔧",
      page:        "/robot.html",
      color:       "#ff6b35",
    },
    Z100L: {
      id:          "Z100L",
      name:        "Z100L 料笼搬运机器人",
      level:       "L2",
      level_label: "L2 搬运",
      desc:        "上下料+料笼搬运专用，负载>50kg。OE区统一配置。",
      icon:        "📦",
      page:        "",
      color:       "#58a6ff",
    },
    Z700F_AOI: {
      id:          "Z700F+AOI",
      name:        "Z700F + AOI 目检机器人",
      level:       "L2",
      level_label: "L2 目检",
      desc:        "精密AOI目检专用。显微镜检、外观检查、缺陷判定。",
      icon:        "🔬",
      page:        "",
      color:       "#a371f7",
    },
  },

  /* ═══════════════════════════════════════════
   *  系统节点（三层解耦架构）
   * ═══════════════════════════════════════════ */
  systems: {
    sys0: {
      id:          "Sys0",
      name:        "Sys0 · 硬件基座",
      hardware:    "Orin Nano",
      gpu:         "—",
      ram:         "8GB",
      role:        "终端执行 · 传感器采集 · 机械臂控制",
      model:       "ROS2 · SR5-C · 6轴+8传感器",
      color:       "#d4a800",
    },
    sys1: {
      id:          "Sys1",
      name:        "Sys1 · 端边推理",
      hardware:    "RTX 4060",
      gpu:         "8GB",
      ram:         "16GB",
      role:        "边缘推理引擎 · 实时力控闭环",
      model:       "VLA-T / GR00T / ACT / SmolVLA / LeWM 五引擎切换",
      color:       "#58a6ff",
    },
    sys2: {
      id:          "Sys2",
      name:        "Sys2 · 云端训练",
      hardware:    "RTX 4090",
      gpu:         "24GB",
      ram:         "32GB",
      role:        "大模型训练+推理 · 全产线智能决策",
      model:       "SmolVLA 450M · GR00T 7B · 云端训练闭环",
      color:       "#00d4aa",
    },
    edge: {
      id:          "Edge",
      name:        "Edge · 端侧",
      hardware:    "Mac M1 · Orin Nano",
      gpu:         "—",
      ram:         "—",
      role:        "现场执行 · 7×24可靠运行",
      model:       "SmolVLA-INT8量化 · <15ms推理",
      color:       "#a371f7",
    },
  },

  /* ═══════════════════════════════════════════
   *  模型引擎
   * ═══════════════════════════════════════════ */
  models: {
    SmolVLA: {
      name:        "SmolVLA",
      full_name:   "SmolVLA 视觉-语言-动作模型",
      params:      "450M",
      type:        "视觉-语言-动作",
      deployment:  "Sys11 · Sys2",
      desc:        "端到端视觉-语言-动作。支持零样本泛化。",
      color:       "#a371f7",
    },
    GR00T: {
      name:        "GR00T",
      full_name:   "GR00T N1.7 通用机器人基础模型",
      params:      "7B",
      type:        "通用机器人基础模型",
      deployment:  "Sys2",
      desc:        "NVIDIA GR00T N1.7-3B。DiT 1.09B。封装16种具身操作。",
      color:       "#00d4aa",
    },
    ACT: {
      name:        "ACT",
      full_name:   "Action Chunking Transformer",
      params:      "52M",
      type:        "动作分块Transformer",
      deployment:  "Sys1 (4060)",
      desc:        "<10ms推理。实时力控闭环>1kHz。",
      color:       "#58a6ff",
    },
    LeWM: {
      name:        "LeWM",
      full_name:   "LeWorldModel 世界模型",
      params:      "—",
      type:        "世界模型",
      deployment:  "Sys12",
      desc:        "与SmolVLA深度耦合。感知→预测→决策→执行完整闭环。",
      color:       "#d4a800",
    },
    VLA_T: {
      name:        "VLA-T",
      full_name:   "VLA-T 触觉力控模型",
      params:      "—",
      type:        "视觉-语言-动作-触觉",
      deployment:  "Sys21",
      desc:        "3D感知+力控+触觉编码器。",
      color:       "#ff6b35",
    },
  },

  /* ═══════════════════════════════════════════
   *  硬件规格
   * ═══════════════════════════════════════════ */
  hardware: {
    camera:       { model:"RealSense D405", type:"RGB-D深度相机", spec:"1920×1080 · 30fps · 0.1-10m" },
    robot_arm:    { model:"珞石 SR5-C",     type:"6轴机械臂",     spec:"±0.02mm重复精度 · 5kg负载" },
    gripper:      { model:"DH夹爪",          type:"电动平行夹爪",   spec:"" },
    force_sensor: { model:"六维力传感器",    type:"F/T传感器",     spec:"Fx/Fy/Fz/Tx/Ty/Tz · ±0.1N · 1kHz" },
    tactile:      { model:"指尖触觉阵列",    type:"16通道触觉",    spec:"16bit · 1kHz" },
  },

  /* ═══════════════════════════════════════════
   *  工厂产线
   * ═══════════════════════════════════════════ */
  factory: {
    product:      "800G DR8",
    product_pn:   "260-B4103",
    zones: [
      { id:"coc", name:"COC 基板区",   color:"#f0a500", page:"/coc-process.html", stations:"I101-I124", count:24 },
      { id:"oe",  name:"OE 光引擎区",  color:"#ff6b35", page:"/oe-process.html",  stations:"I125-I196", count:72 },
      { id:"mod", name:"MOD 模块组装区",color:"#58a6ff", page:"/mod-process.html", stations:"I197-I222", count:26 },
      { id:"wh",  name:"WH 仓库物流区", color:"#3fb950", page:"/wh-process.html",  stations:"I223-I228+I500", count:7 },
    ],
    total_stations: 228,
    final_inspection: "I500",
  },

  /* ═══════════════════════════════════════════
   *  DDS 技能体系（条件→模型→动作→安全）
   * ═══════════════════════════════════════════ */
  dds_skills: {
    conditions: {
      count: 38,
      id_range: "C001-C038",
      color: "#a371f7",
      icon: "🟣",
      label: "condition条件",
      desc: "环境输入→模型感知",
    },
    models: {
      count: 7,
      id_range: "M01-M07",
      color: "#58a6ff",
      icon: "🔵",
      label: "model模型",
      desc: "多模态数据→训练输入",
    },
    actions_100g: {
      count_suffix: "100G",
      color: "#58a6ff",
      icon: "🔵",
      label: "100G动作",
    },
    actions_400g: {
      count_suffix: "400G",
      color: "#00d4aa",
      icon: "🟢",
      label: "400G动作",
    },
    actions_800g: {
      count_suffix: "800G",
      color: "#d4a800",
      icon: "🟡",
      label: "800G动作",
    },
    safety: {
      count: 4,
      color: "#ff4444",
      icon: "🛡️",
      label: "安全",
      desc: "五层主动安全保护",
    },
  },

  /* ═══════════════════════════════════════════
   *  数据流水线
   * ═══════════════════════════════════════════ */
  pipeline: {
    name: "数据流水线 · Orin→MAC→4090",
    version: "2.0",
    phases: [
      { name:"采集", node:"Orin Nano", duration:30, icon:"📡" },
      { name:"转发", node:"MAC",       duration:5,  icon:"💻" },
      { name:"训练", node:"4090",      duration:60, icon:"🧠" },
    ],
  },

  /* ═══════════════════════════════════════════
   *  产品迭代路线
   * ═══════════════════════════════════════════ */
  roadmap: [
    { version:"v1.0", timeline:"2026Q3", name:"单工位验证", desc:"光模块插拔 · 固定轨迹 · Orin Nano边缘部署 · 力控±0.02mm", color:"#00d4aa" },
    { version:"v1.5", timeline:"2026Q4", name:"多工位联线", desc:"抓取→插拔→AOI×6全链条 · Sys1端侧VLA-T力控闭环 · 99%+良率", color:"#58a6ff" },
    { version:"v2.0", timeline:"2027Q2", name:"全产线智能", desc:"多机协同 · 换型自适配 · VLA-T+GR00T · 云端训练闭环", color:"#a371f7" },
  ],

  /* ═══════════════════════════════════════════
   *  外部链接
   * ═══════════════════════════════════════════ */
  links: {
    github:     "https://github.com/MikeBMW/lerobot-smolvla-lew",
    zmax:       "https://github.com/MikeBMW/zmax-website",
    hybrid:     "https://github.com/MikeBMW/zmax-website",
    deepseek:   "https://platform.deepseek.com/usage",
    gpu_console:"https://console.compshare.cn/uaccount/costcenter",
    wandb:      "https://wandb.ai/xspace/zmax-hjepa",
  },

  /* ═══════════════════════════════════════════
   *  主题色
   * ═══════════════════════════════════════════ */
  theme: {
    bg:       "#06080d",
    card:     "#0d1117",
    border:   "#1a1f2b",
    accent:   "#00d4aa",
    accent2:  "#00ffcc",
    text:     "#c8d1d9",
    muted:    "#8b949e",
    danger:   "#ff4444",
    warning:  "#d4a800",
    info:     "#58a6ff",
  },

};

/* ── 便捷访问函数 ── */
window.DDS.getKPI = function(key) { return this.kpi[key]; };
window.DDS.getRobot = function(id) { return this.robots[id]; };
window.DDS.getSystem = function(id) { return this.systems[id]; };
window.DDS.getModel = function(id) { return this.models[id]; };
window.DDS.getZone = function(id) { return this.factory.zones.find(function(z){return z.id===id;}); };

console.log("DDS Global · 数据中心已加载 · v" + window.DDS.company.year + " · " + window.DDS.factory.product);
