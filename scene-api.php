<?php
/**
 * Scene JSON upload endpoint
 * POST /api/scene/{type} → save to /root/zmax-website/scenes/
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") { http_response_code(200); exit; }

$type = basename($_SERVER["PATH_INFO"] ?? "unknown");
$dir = "/root/zmax-website/scenes";
if (!is_dir($dir)) mkdir($dir, 0755, true);

$body = file_get_contents("php://input");
$data = json_decode($body, true);
if (!$data) { echo json_encode(["error" => "invalid JSON"]); exit; }

$data["_received"] = date("Y-m-d H:i:s");
$data["_type"] = $type;
$file = "$dir/scene_$type.json";
file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo json_encode(["ok" => true, "file" => $file, "size" => strlen($body)]);
