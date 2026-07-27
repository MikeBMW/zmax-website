<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$file = __DIR__ . "/team_chat.json";
$backup = __DIR__ . "/team_chat.bak.json";

function safeRead($path) {
    if (!file_exists($path)) return [];
    $raw = @file_get_contents($path);
    if ($raw === false || trim($raw) === '') return []; 
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $input = json_decode(file_get_contents("php://input"), true);
    if ($input && isset($input["from"]) && isset($input["msg"])) {
        
        // Lock file to prevent race conditions
        $fp = fopen($file, "c+");
        if (!$fp || !flock($fp, LOCK_EX)) {
            echo json_encode(["status" => "error", "msg" => "lock failed"]);
            if ($fp) fclose($fp);
            exit;
        }
        
        // Backup before write
        $msgs = safeRead($file);
        if (!empty($msgs)) {
            @file_put_contents($backup, json_encode($msgs, JSON_UNESCAPED_UNICODE));
        }
        
        array_unshift($msgs, [
            "from" => $input["from"],
            "msg" => substr($input["msg"], 0, 500),
            "time" => date("Y-m-d H:i")
        ]);
        $msgs = array_slice($msgs, 0, 50);
        
        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, json_encode($msgs, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT));
        fflush($fp);
        
        flock($fp, LOCK_UN);
        fclose($fp);
        
        // Push to Feishu (fire-and-forget, non-blocking)
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => "http://datadrive.world/notify.php",
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
    // GET: read-only, no lock needed
    $msgs = safeRead($file);
    echo json_encode($msgs, JSON_UNESCAPED_UNICODE);
}
