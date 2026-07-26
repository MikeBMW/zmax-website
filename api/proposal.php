<?php
$format = $_GET['format'] ?? 'pptx';

if ($format === 'docx') {
    header('Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document');
    header('Content-Disposition: attachment; filename="Z700_立项申请书.docx"');
    header('Location: /proposal.html');
    // Fallback - serve the page as HTML
    readfile('/www/wwwroot/datadrive.world/proposal.html');
} elseif ($format === 'pptx') {
    $file = '/www/wwwroot/datadrive.world/proposal.pptx';
    if (file_exists($file)) {
        header('Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation');
        header('Content-Disposition: attachment; filename="Z700_立项申请书.pptx"');
        header('Content-Length: ' . filesize($file));
        readfile($file);
    } else {
        header('Location: /proposal.html');
    }
} else {
    header('Location: /proposal.html');
}
