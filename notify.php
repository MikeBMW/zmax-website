<?php
/**
 * Z-MAX 飞书通知桥 v3 — 简化 text 格式
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode(["status" => "error", "msg" => "POST only"]);
    exit;
}

$input = json_decode(file_get_contents("php://input"), true);
if (!$input || !isset($input["from"]) || !isset($input["msg"])) {
    echo json_encode(["status" => "error", "msg" => "need from + msg"]);
    exit;
}

$from = $input["from"];
$msg = $input["msg"];

$NAMES = ["dani" => "大倪", "xspace" => "静静", "web" => "web", "xiaofang" => "小芳"];
$AVATARS = ["dani" => "👑", "xspace" => "🟢", "web" => "🟣", "xiaofang" => "🟠"];
$sender = isset($NAMES[$from]) ? $NAMES[$from] : $from;
$avatar = isset($AVATARS[$from]) ? $AVATARS[$from] : "💬";
$hasAll = preg_match('/@all\b/i', $msg);

// Build simple text
$text = $avatar . " " . $sender . "：" . $msg;
if ($hasAll) $text = "📢 " . $text;
$text .= "\n👉 https://datadrive.world/chat.html";

// Feishu API
$APP_ID = "getenv('FEISHU_APP_ID','cli_aad84fde4a619cc7')";
$APP_SECRET = "getenv('FEISHU_APP_SECRET','')";
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
$token = isset($token_data["tenant_access_token"]) ? $token_data["tenant_access_token"] : null;

if (!$token) {
    echo json_encode(["status" => "error", "msg" => "auth failed"]);
    curl_close($ch);
    exit;
}

$content = json_encode(["text" => $text], JSON_UNESCAPED_UNICODE);

$body = json_encode([
    "receive_id" => $CHAT_ID,
    "msg_type" => "text",
    "content" => $content
], JSON_UNESCAPED_UNICODE);

curl_setopt_array($ch, [
    CURLOPT_URL => "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $body,
    CURLOPT_HTTPHEADER => [
        "Content-Type: application/json",
        "Authorization: Bearer " . $token
    ]
]);

$send_resp = curl_exec($ch);
curl_close($ch);

$send_data = json_decode($send_resp, true);
$success = isset($send_data["code"]) && $send_data["code"] === 0;

echo json_encode([
    "status" => $success ? "ok" : "error",
    "code" => isset($send_data["code"]) ? $send_data["code"] : -1,
    "msg" => isset($send_data["msg"]) ? $send_data["msg"] : ""
], JSON_UNESCAPED_UNICODE);
