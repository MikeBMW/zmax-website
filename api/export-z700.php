<?php
$format = $_GET['format'] ?? 'pptx';

if ($format === 'docx') {
    header('Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document');
    header('Content-Disposition: attachment; filename="Z700_轮式双臂_精品分析报告.docx"');
    
    $html = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="UTF-8"><style>
body{font-family:SimSun;font-size:12pt;line-height:1.8;color:#333}
h1{font-size:22pt;color:#00d4aa;text-align:center;margin-bottom:10pt}
h2{font-size:16pt;color:#00d4aa;border-bottom:2pt solid #00d4aa33;padding-bottom:4pt;margin-top:20pt}
h3{font-size:13pt;color:#333;margin-top:14pt}
table{width:100%;border-collapse:collapse;margin:10pt 0}
th{background:#00d4aa22;padding:6pt 10pt;text-align:left;color:#00d4aa;font-weight:bold;border:1pt solid #ccc}
td{padding:5pt 10pt;border:1pt solid #ccc}
.sub{text-align:center;color:#888;font-size:10pt}
.kpi-table td{text-align:center;font-size:14pt;font-weight:bold;padding:12pt}
.kpi-table .val{font-size:22pt;color:#00d4aa}
.highlight{color:#00d4aa;font-weight:bold}
</style></head><body>';

    $html .= '<h1>Z700 轮式双臂 · 精品分析报告</h1>';
    $html .= '<p class="sub">光模块精密制造 · 具身智能旗舰 · 对比它石智航 TARS</p>';
    
    // KPI
    $html .= '<h2>核心性能指标</h2>';
    $html .= '<table class="kpi-table"><tr>';
    $kpis = [
        ['±0.02','mm','重复定位精度'],
        ['&gt;99','%','关键工序良率'],
        ['&gt;10','kHz','力控闭环带宽'],
        ['&lt;15','s','单次插拔节拍'],
        ['≤0.1','N','接触力控制'],
        ['&gt;50','kg','双臂负载']
    ];
    foreach ($kpis as $k) {
        $html .= '<td><div class="val">'.$k[0].'</div>'.$k[1].'<br><small>'.$k[2].'</small></td>';
    }
    $html .= '</tr></table>';
    
    // Product Architecture
    $html .= '<h2>产品架构</h2>';
    $html .= '<p><span class="highlight">Z700 轮式双臂精密操作机器人</span> — L4旗舰 · 全自主执行+自适应+自恢复</p>';
    $html .= '<p>轮式底盘AMR自主导航 · 双臂6轴×2协同操作 · 8+传感器融合 · 力控闭环>10kHz</p>';
    
    // Scenarios
    $html .= '<h2>五大应用场景</h2>';
    $html .= '<table><tr><th>场景</th><th>工位</th><th>工艺</th><th>KPI</th><th>阶段</th></tr>';
    $scenarios = [
        ['FW固件烧录','下载FW · SN识别','扫码→烧录→校验→追溯','节拍≤15s','Phase1'],
        ['上下料','COC上料 · BI上下料 · 贴片备料','识别→取件→放置→满空交换','零损伤','Phase1'],
        ['老化箱插拔','COC BI-01 · 模块BI · DA烘烤','定位→插入→力控→锁止','力≤0.1N','Phase1'],
        ['热海柜操作','TCT温变 · 热岛立柜','开柜→取放→关柜→监控','±0.05mm','Phase2'],
        ['ATS自动测试','MPD测试 · OE测试 · OE/TRX','装夹→插拔→测试→分Bin','≥99%良率','Phase2'],
    ];
    foreach ($scenarios as $s) {
        $html .= '<tr><td><b>'.$s[0].'</b></td><td>'.$s[1].'</td><td>'.$s[2].'</td><td>'.$s[3].'</td><td>'.$s[4].'</td></tr>';
    }
    $html .= '</table>';
    
    // TARS Comparison
    $html .= '<h2>它石智航 TARS 对标分析</h2>';
    $html .= '<p>智蜂创元(苏州) × 它石智航 TARS(上海) · 一期10台(5自研+5它石) · 1000万预算 · 白盒交付</p>';
    $html .= '<table><tr><th>对比维度</th><th>Z700 智蜂自研</th><th>TARS 它石智航</th><th>分析</th></tr>';
    $comparisons = [
        ['力控精度','≤0.1N · 10kHz闭环','≤0.5N · 1kHz典型','Z700领先5×'],
        ['重复定位','±0.02mm','±0.05mm','Z700领先2.5×'],
        ['插拔节拍','<15s/次','20-30s/次','Z700快1.5-2×'],
        ['自主导航','AMR · 多工位自由移动','需轨道/固定安装','Z700独有优势'],
        ['双臂协同','原生双臂 · 协同装配','单臂为主 · 需定制','Z700架构优势'],
        ['软件生态','89原子技能 · 全栈自研','ROS2通用框架','Z700专用性强'],
        ['交付模式','白盒 · 全栈技术转让','黑盒 · SDK接口','Z700战略优势'],
        ['部署周期','2-4周/工站','4-8周/工站','Z700更快'],
    ];
    foreach ($comparisons as $c) {
        $html .= '<tr><td><b>'.$c[0].'</b></td><td>'.$c[1].'</td><td>'.$c[2].'</td><td><span class="highlight">'.$c[3].'</span></td></tr>';
    }
    $html .= '</table>';
    
    // SWOT
    $html .= '<h2>SWOT分析</h2>';
    $html .= '<h3>优势 S</h3><p>光模块行业深度定制，89项原子技能覆盖全产线；力控闭环>10kHz行业领先；轮式AMR+双臂多工位调度；白盒交付客户获全栈能力。</p>';
    $html .= '<h3>劣势 W</h3><p>品牌知名度低于它石/珞石等老牌；量产成熟度待验证；供应链依赖外部；单行业聚焦需额外投入跨行业。</p>';
    $html .= '<h3>机会 O</h3><p>光模块800G/1.6T升级需求；AI算力驱动产能扩张；精密电子"机器换人"红利；白盒模式可复制半导体/汽车电子。</p>';
    $html .= '<h3>威胁 T</h3><p>它石可能自研光模块方案；成熟厂商向下整合；行业周期波动；技术人才竞争；价格战风险。</p>';
    
    // Roadmap
    $html .= '<h2>交付路线图</h2>';
    $html .= '<table><tr><th>阶段</th><th>时间</th><th>Z700交付</th><th>TARS交付</th><th>验收标准</th></tr>';
    $html .= '<tr><td>Phase1</td><td>2026.07-11</td><td>5台 · FW/上下料/老化箱</td><td>5台同步</td><td>成功率≥99%</td></tr>';
    $html .= '<tr><td>Phase2</td><td>2026.12-2027.04</td><td>热海柜+ATS+全线串联</td><td>补充优化</td><td>节拍达标</td></tr>';
    $html .= '<tr><td>Phase3</td><td>2027.05+</td><td>跨行业复制</td><td>评估续约</td><td>ROI验证</td></tr>';
    $html .= '</table>';
    
    // Business Value
    $html .= '<h2>商业价值</h2>';
    $html .= '<p>人工效率提升 <span class="highlight">3-5×</span> · 连续运行 <span class="highlight">24/7</span> · 投资回收期 <span class="highlight"><12月</span></p>';
    
    $html .= '<p style="text-align:center;margin-top:30pt;color:#888">Z-MAX · 智蜂创元 (苏州) × 它石智航 TARS (上海) · 2026</p>';
    $html .= '</body></html>';
    
    echo $html;
    
} elseif ($format === 'pptx') {
    // Use python-pptx to generate real PPTX
    $pyScript = '/tmp/gen_z700_pptx.py';
    $pyCode = <<<'PYEOF'
import sys
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    print("ERROR: python-pptx not installed")
    sys.exit(1)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
C = RGBColor(0x00, 0xD4, 0xAA)
DARK = RGBColor(0x06, 0x08, 0x0D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x8B, 0x94, 0x9E)

def add_slide(title, content_lines):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK
    
    # Title
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = txBox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = C
    
    # Content
    txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(12), Inches(5.5))
    tf2 = txBox2.text_frame; tf2.word_wrap = True
    for i, line in enumerate(content_lines):
        if i == 0:
            p = tf2.paragraphs[0]
        else:
            p = tf2.add_paragraph()
        p.text = line
        p.font.size = Pt(16)
        p.font.color.rgb = GRAY
        p.space_after = Pt(4)

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg = slide.background; bg.fill.solid(); bg.fill.fore_color.rgb = DARK
txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
tf = txBox.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Z700 轮式双臂 · 精品分析报告"; p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = C; p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph(); p2.text = "光模块精密制造 · 具身智能旗舰 · 对比它石智航 TARS"; p2.font.size = Pt(18); p2.font.color.rgb = GRAY; p2.alignment = PP_ALIGN.CENTER
p3 = tf.add_paragraph(); p3.text = "智蜂创元 (苏州) × 它石智航 TARS (上海) · 2026"; p3.font.size = Pt(14); p3.font.color.rgb = GRAY; p3.alignment = PP_ALIGN.CENTER; p3.space_before = Pt(20)

# Slide 2: KPI
add_slide("核心性能指标", [
    "±0.02mm 重复定位精度 | >99% 关键工序良率 | >10kHz 力控闭环带宽",
    "<15s 单次插拔节拍 | ≤0.1N 接触力控制 | >50kg 双臂负载",
    "", "Z700 轮式双臂 · L4 旗舰 · 全自主执行+自适应+自恢复",
    "轮式底盘AMR + 双臂6轴×2 + 8+传感器融合 + 力控闭环"
])

# Slide 3: Scenarios
add_slide("五大应用场景", [
    "1. FW固件烧录 — 扫码→烧录→校验→追溯 | 节拍≤15s | Phase1",
    "2. 上下料 — 识别→取件→放置→满空交换 | 零损伤 | Phase1",
    "3. 老化箱插拔 — 定位→插入→力控→锁止 | 力≤0.1N | Phase1",
    "4. 热海柜操作 — 开柜→取放→关柜→监控 | ±0.05mm | Phase2",
    "5. ATS自动测试 — 装夹→插拔→测试→分Bin | ≥99%良率 | Phase2"
])

# Slide 4: TARS Comparison
add_slide("它石智航 TARS 对标分析", [
    "智蜂创元(苏州) × 它石智航 TARS(上海) · 一期10台(5自研+5它石) · 1000万 · 白盒交付",
    "",
    "力控精度: Z700 ≤0.1N/10kHz  vs  TARS ≤0.5N/1kHz — Z700领先5×",
    "重复定位: Z700 ±0.02mm  vs  TARS ±0.05mm — Z700领先2.5×",
    "插拔节拍: Z700 <15s  vs  TARS 20-30s — Z700快1.5-2×",
    "自主导航: Z700 AMR多工位  vs  TARS 需轨道 — Z700独有优势",
    "双臂协同: Z700 原生双臂  vs  TARS 需定制 — Z700架构优势",
    "交付模式: Z700 白盒全栈  vs  TARS 黑盒SDK — Z700战略优势"
])

# Slide 5: SWOT
add_slide("SWOT 分析", [
    "S 优势: 光模块深度定制 · 89原子技能 · 力控领先 · 白盒交付 · 苏州产业集群",
    "W 劣势: 品牌知名度低 · 量产待验证 · 供应链外部依赖 · 单行业聚焦",
    "O 机会: 800G/1.6T升级 · AI算力扩张 · 机器换人红利 · 跨行业复制",
    "T 威胁: 它石自研方案 · 成熟厂商整合 · 行业周期 · 人才竞争 · 价格战"
])

# Slide 6: Atomic Skills
add_slide("89项原子技能覆盖", [
    "感知定位 15项: P001-P015 对象识别/位姿估计/缺陷检测/视觉伺服",
    "操作执行 15项: A001-A015 夹取/插入/装配/锁付/点胶/焊接/贴装",
    "装配工艺 15项: P056-P070 COC共晶/WB打线/UV固化/耦合/分板/绑定",
    "质量检测 10项: Q001-Q010 目检/AOI/3D测量/GRR/追溯",
    "安全集成 10项: S001-S010 力控/碰撞/急停/区域监控",
    "载具物流 9项: H001-H009 识别/接驳/交换/追溯",
    "学习泛化 8项: L001-L008 迁移/校准/少样本/多模态",
    "移动导航 7项: M001-M007 SLAM/路径/避障/对接"
])

# Slide 7: Roadmap
add_slide("交付路线图", [
    "Phase1 (2026.07-11): 首批样机 · 5台Z700+5台TARS · FW/上下料/老化箱 · 成功率≥99%",
    "Phase2 (2026.12-2027.04): 全线部署 · 热海柜+ATS+全线串联 · 节拍达标",
    "Phase3 (2027.05+): 规模复制 · 跨行业(3C/汽车电子) · ROI验证"
])

# Slide 8: Business Value
add_slide("商业价值", [
    "人工效率提升: 3-5×",
    "连续运行: 24/7",
    "投资回收期: <12个月",
    "",
    "Z-MAX · 智蜂创元 (苏州) × 它石智航 TARS (上海) · 2026"
])

prs.save('/tmp/z700_analysis.pptx')
print("PPTX_OK")
PYEOF;
    
    file_put_contents($pyScript, $pyCode);
    $out = shell_exec("python3 $pyScript 2>&1");
    
    if (strpos($out, 'PPTX_OK') !== false) {
        header('Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation');
        header('Content-Disposition: attachment; filename="Z700_轮式双臂_精品分析报告.pptx"');
        header('Content-Length: ' . filesize('/tmp/z700_analysis.pptx'));
        readfile('/tmp/z700_analysis.pptx');
    } else {
        // Fallback: redirect to HTML page
        header('Location: /z700-analysis.html');
    }
}
