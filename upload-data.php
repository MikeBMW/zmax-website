<?php
header('Access-Control-Allow-Origin: *');
$dir = __DIR__ . '/uploads/data';
if (!is_dir($dir)) mkdir($dir, 0755, true);

// GET: list files
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $files = [];
    foreach (glob($dir . '/*') as $f) {
        if (is_file($f)) {
            $files[] = [
                'name' => basename($f),
                'size' => filesize($f),
                'url' => '/uploads/data/' . basename($f),
                'time' => filemtime($f)
            ];
        }
    }
    usort($files, fn($a,$b) => $b['time'] <=> $a['time']);
    header('Content-Type: application/json');
    echo json_encode($files, JSON_UNESCAPED_UNICODE);
    exit;
}

// POST: upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $f = $_FILES['file'];
    $name = basename($f['name']);
    $dest = $dir . '/' . $name;
    if (move_uploaded_file($f['tmp_name'], $dest)) {
        header('Content-Type: application/json');
        echo json_encode(['ok'=>true, 'name'=>$name, 'size'=>filesize($dest)]);
    } else {
        http_response_code(500);
        echo json_encode(['error'=>'move failed']);
    }
    exit;
}

http_response_code(405);
echo json_encode(['error'=>'method not allowed']);
