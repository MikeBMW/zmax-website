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
    $pptxFile = '/www/wwwroot/datadrive.world/api/z700-analysis.pptx';
    if (file_exists($pptxFile)) {
        header('Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation');
        header('Content-Disposition: attachment; filename="Z700_轮式双臂_精品分析报告.pptx"');
        header('Content-Length: ' . filesize($pptxFile));
        readfile($pptxFile);
    } else {
        header('Location: /z700-analysis.html');
    }
}
