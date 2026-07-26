<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

$dir = __DIR__ . '/diagrams';
if (!is_dir($dir)) mkdir($dir, 0755, true);

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_GET['file'])) {
        $file = basename($_GET['file']);
        $path = $dir . '/' . $file;
        if (!file_exists($path)) { http_response_code(404); echo json_encode(['error'=>'not found']); exit; }
        header('Content-Type: application/xml');
        readfile($path);
        exit;
    }
    $files = [];
    foreach (glob($dir . '/*.drawio') as $f) {
        $files[] = ['name' => basename($f), 'size' => filesize($f), 'time' => filemtime($f)];
    }
    usort($files, fn($a,$b) => $b['time'] <=> $a['time']);
    echo json_encode($files);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw = file_get_contents('php://input');
    $json = json_decode($raw, true);
    if (!$json || empty($json['name']) || empty($json['xml'])) {
        http_response_code(400); echo json_encode(['error'=>'name and xml required']); exit;
    }
    $name = basename($json['name']);
    if (!str_ends_with($name, '.drawio')) $name .= '.drawio';
    file_put_contents($dir . '/' . $name, $json['xml']);
    echo json_encode(['ok'=>true, 'name'=>$name, 'size'=>strlen($json['xml'])]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
    $raw = file_get_contents('php://input');
    $json = json_decode($raw, true);
    if (!$json || empty($json['name'])) {
        http_response_code(400); echo json_encode(['error'=>'name required']); exit;
    }
    $name = basename($json['name']);
    $path = $dir . '/' . $name;
    if (file_exists($path)) unlink($path);
    echo json_encode(['ok'=>true]);
    exit;
}

http_response_code(405); echo json_encode(['error'=>'method not allowed']);
