<?php
/**
 * Z-MAX 已读回执
 * 记录每个用户最后一次读取时间
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$file = __DIR__ . "/team_read.json";
$reads = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Mark user as having read
    $input = json_decode(file_get_contents("php://input"), true);
    if ($input && isset($input["user"])) {
        $reads[$input["user"]] = date("Y-m-d H:i");
        file_put_contents($file, json_encode($reads, JSON_UNESCAPED_UNICODE));
        echo json_encode(["status" => "ok", "reads" => $reads]);
    } else {
        echo json_encode(["status" => "error", "msg" => "need user"]);
    }
} else {
    echo json_encode($reads, JSON_UNESCAPED_UNICODE);
}
