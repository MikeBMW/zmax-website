<?php
// 架构图上传处理
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$upload_dir = '/www/wwwroot/datadrive.world/uploads/';
if (!is_dir($upload_dir)) mkdir($upload_dir, 0755, true);

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['image'])) {
    $file = $_FILES['image'];
    if ($file['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['ok'=>false, 'error'=>'upload error '.$file['error']]);
        exit;
    }
    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $allowed = ['jpg','jpeg','png','gif','webp','svg'];
    if (!in_array(strtolower($ext), $allowed)) {
        echo json_encode(['ok'=>false, 'error'=>'unsupported format']);
        exit;
    }
    $name = 'arch_' . time() . '_' . bin2hex(random_bytes(4)) . '.' . $ext;
    $dest = $upload_dir . $name;
    if (move_uploaded_file($file['tmp_name'], $dest)) {
        chmod($dest, 0644);
        echo json_encode(['ok'=>true, 'url'=>'/uploads/'.$name, 'name'=>$name]);
    } else {
        echo json_encode(['ok'=>false, 'error'=>'move failed']);
    }
    exit;
}

// 列出已上传图片
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $images = [];
    if (is_dir($upload_dir)) {
        foreach (glob($upload_dir . 'arch_*.{jpg,jpeg,png,gif,webp,svg}', GLOB_BRACE) as $f) {
            $images[] = [
                'url' => '/uploads/' . basename($f),
                'name' => basename($f),
                'time' => filemtime($f)
            ];
        }
    }
    usort($images, function($a,$b){ return $b['time'] - $a['time']; });
    echo json_encode(['ok'=>true, 'images'=>$images]);
    exit;
}

echo json_encode(['ok'=>false, 'error'=>'invalid request']);
