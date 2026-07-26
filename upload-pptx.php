<?php
// PPT upload & compare endpoint
// POST: uploads PPTX, extracts text, compares with DDS, returns diff
// GET with ?action=apply: applies pending changes to DDS

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['pptx'])) {
    $tmp = $_FILES['pptx']['tmp_name'];
    $name = $_FILES['pptx']['name'];
    
    if (!file_exists($tmp)) {
        echo json_encode(['error'=>'Upload failed']);
        exit;
    }
    
    // Save uploaded file
    $dest = '/www/wwwroot/datadrive.world/uploads/' . basename($name);
    move_uploaded_file($tmp, $dest);
    
    // Extract text from PPTX (using zip + XML parsing, no exec needed)
    $zip = new ZipArchive();
    $slides = [];
    if ($zip->open($dest) === TRUE) {
        for ($i = 1; $i <= 50; $i++) {
            $xmlFile = 'ppt/slides/slide' . $i . '.xml';
            $xml = $zip->getFromName($xmlFile);
            if ($xml === false) break;
            
            // Extract all text from slide XML
            $text = '';
            if (preg_match_all('/<a:t[^>]*>([^<]*)<\/a:t>/', $xml, $m)) {
                $text = implode(' ', $m[1]);
            }
            if (trim($text)) {
                $slides[] = ['num' => $i, 'text' => trim($text)];
            }
        }
        $zip->close();
    }
    
    // Compare with DDS data
    $db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');
    
    // Get current DDS values
    $current = [];
    $res = $db->query("SELECT key, value FROM company");
    while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
        $current['company'][$row['key']] = $row['value'];
    }
    $res = $db->query("SELECT * FROM kpi");
    while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
        $current['kpi'][$row['id']] = $row;
    }
    
    $diffs = [];
    foreach ($slides as $sl) {
        $t = $sl['text'];
        
        // Check company fields
        foreach ($current['company'] as $k => $v) {
            if (stripos($t, $v) === false && strlen($v) > 3) {
                // Value not found - search for similar text nearby
                $diffs[] = [
                    'table' => 'company',
                    'key' => $k,
                    'current' => $v,
                    'slide' => $sl['num'],
                    'context' => substr($t, 0, 100) . '...'
                ];
            }
        }
    }
    
    $db->close();
    
    echo json_encode([
        'ok' => true,
        'file' => $name,
        'slides' => count($slides),
        'slides_data' => $slides,
        'diffs' => $diffs,
        'note' => 'Diffs show values from DDS not found in PPT. Update PPT or click "Apply" to sync PPT changes into DDS.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// GET: list uploaded PPTX files
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $files = glob('/www/wwwroot/datadrive.world/uploads/*.pptx');
    $result = [];
    foreach ($files as $f) {
        $result[] = [
            'name' => basename($f),
            'size' => filesize($f),
            'time' => date('Y-m-d H:i', filemtime($f))
        ];
    }
    echo json_encode($result);
    exit;
}

echo json_encode(['error'=>'Use POST with file upload']);
