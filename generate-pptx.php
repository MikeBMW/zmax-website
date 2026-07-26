<?php
// Serve pre-generated PPTX file (regenerated via cron or manual trigger)
$out = '/www/wwwroot/datadrive.world/Z700-立项申请书.pptx';

if (!file_exists($out)) {
    http_response_code(404);
    header('Content-Type: application/json');
    echo json_encode(['error'=>'PPTX file not found. Contact admin to regenerate.'], JSON_UNESCAPED_UNICODE);
    exit;
}

header('Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation');
header('Content-Disposition: attachment; filename="Z700-立项申请书.pptx"');
header('Content-Length: ' . filesize($out));
readfile($out);
