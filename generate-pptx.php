<?php
// Regenerate PPTX from DDS database and return for download
$out = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx';

// Run the Python generator (reads dds.db directly)
exec("python3 /root/zmax-website/gen_pptx.py 2>&1", $output, $rc);

if ($rc !== 0 || !file_exists($out)) {
    http_response_code(500);
    header('Content-Type: application/json');
    echo json_encode(['error'=>'Generation failed', 'output'=>implode("\n",$output)], JSON_UNESCAPED_UNICODE);
    exit;
}

header('Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation');
header('Content-Disposition: attachment; filename="Z700-立项申请书.pptx"');
header('Content-Length: ' . filesize($out));
readfile($out);
