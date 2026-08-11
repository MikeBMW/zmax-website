<?php
/**
 * Robot Action API
 * GET  /api/robot-action?robot=R3 → 当前动作指标
 * POST /api/robot-action → 写入指标
 * POST /api/action-log    → 写入动作记录
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");
if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") { http_response_code(200); exit; }

$dir = "/root/zmax-website/action-data";
if (!is_dir($dir)) mkdir($dir, 0755, true);
$path = $_SERVER["PATH_INFO"] ?? "/status";

if ($_SERVER["REQUEST_METHOD"] === "GET" && $path === "/status") {
    // Return latest metrics for a robot
    $robot = $_GET["robot"] ?? "R3";
    $file = "$dir/robot_$robot.json";
    if (file_exists($file)) {
        $data = json_decode(file_get_contents($file), true);
        $data["ts"] = date("Y-m-d H:i:s");
        $data["_file"] = $file;
    } else {
        $data = ["robot" => $robot, "stage" => "IDLE", "metrics" => [], "pass" => true];
    }
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $body = file_get_contents("php://input");
    $data = json_decode($body, true);
    if (!$data) { echo json_encode(["error" => "invalid JSON"]); exit; }
    
    if ($path === "/log") {
        // Action log entry
        $data["_received"] = date("Y-m-d H:i:s");
        $logFile = "$dir/action_log.jsonl";
        file_put_contents($logFile, json_encode($data, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND);
        echo json_encode(["ok" => true, "logged" => true]);
    } else {
        // Update robot metrics
        $robot = $data["robot"] ?? "R3";
        $data["_updated"] = date("Y-m-d H:i:s");
        file_put_contents("$dir/robot_$robot.json", json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo json_encode(["ok" => true, "robot" => $robot]);
    }
    exit;
}

echo json_encode(["api" => "robot-action", "endpoints" => ["GET /status?robot=R3", "POST /", "POST /log"]]);
