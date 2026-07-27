<?php
/**
 * Z-MAX Bot Bridge — Feishu bot 消息写入 chat.html
 * 飞书 bot 通过此端点发消息到群聊
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode(["status" => "error", "msg" => "POST only"]);
    exit;
}

$input = json_decode(file_get_contents("php://input"), true);
if (!$input || !isset($input["msg"])) {
    echo json_encode(["status" => "error", "msg" => "need msg"]);
    exit;
}

// Use same storage as chat.html
$file = __DIR__ . "/team_chat.json";
$msgs = json_decode(file_get_contents($file), true) ?: [];

$from = isset($input["from"]) ? $input["from"] : "dani2";
$msg = substr($input["msg"], 0, 500);

array_unshift($msgs, [
    "from" => $from,
    "msg" => $msg,
    "time" => date("Y-m-d H:i")
]);
$msgs = array_slice($msgs, 0, 50);
file_put_contents($file, json_encode($msgs, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT));

// Also push to Feishu group
$APP_ID = "cli_aad84fde4a619cc7";
$APP_SECRET = getenv("FEISHU_APP_SECRET") ?: "3uSXj0T82lc1njzChVX82sBufnhv3Rvg";
$CHAT_ID = "oc_c0b4048546145c5c581ddd1a9e8f565d";

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode(["app_id" => $APP_ID, "app_secret" => $APP_SECRET]),
    CURLOPT_HTTPHEADER => ["Content-Type: application/json"],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 5
]);
$token_data = json_decode(curl_exec($ch), true);
$token = $token_data["tenant_access_token"] ?? null;

if ($token) {
    $text = "🐋 大鲵：" . $msg;
    curl_setopt_array($ch, [
        CURLOPT_URL => "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        CURLOPT_POSTFIELDS => json_encode([
            "receive_id" => $CHAT_ID,
            "msg_type" => "text",
            "content" => json_encode(["text" => $text], JSON_UNESCAPED_UNICODE)
        ]),
        CURLOPT_HTTPHEADER => [
            "Content-Type: application/json",
            "Authorization: Bearer " . $token
        ]
    ]);
    curl_exec($ch);
}
curl_close($ch);

echo json_encode(["status" => "ok"]);
