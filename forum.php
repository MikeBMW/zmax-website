<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$file = __DIR__ . "/team_chat.json";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $input = json_decode(file_get_contents("php://input"), true);
    if ($input && isset($input["from"]) && isset($input["msg"])) {
        $msgs = json_decode(file_get_contents($file), true) ?: [];
        array_unshift($msgs, [
            "from" => $input["from"],
            "msg" => substr($input["msg"], 0, 500),
            "time" => date("Y-m-d H:i")
        ]);
        $msgs = array_slice($msgs, 0, 50);
        file_put_contents($file, json_encode($msgs, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT));
        
        // Push to Feishu
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => "http://127.0.0.1/notify.php",
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode(["from" => $input["from"], "msg" => $input["msg"]]),
            CURLOPT_HTTPHEADER => ["Content-Type: application/json"],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 3
        ]);
        curl_exec($ch);
        curl_close($ch);
        
        echo json_encode(["status" => "ok"]);
    } else {
        echo json_encode(["status" => "error", "msg" => "need from + msg"]);
    }
} else {
    $msgs = json_decode(file_get_contents($file), true) ?: [];
    echo json_encode($msgs, JSON_UNESCAPED_UNICODE);
}
