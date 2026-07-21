<?php
/**
 * Z-MAX 飞书通知桥
 * forum.php 收到 @all / @mention 消息时，同步推送到飞书群
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
$mentions = isset($input["mentions"]) ? $input["mentions"] : [];

// Feishu config
$APP_ID = "cli_aad84fde4a619cc7";
$APP_SECRET = "3uSXj0T82lc1njzChVX82sBufnhv3Rvg";
$CHAT_ID = "oc_c0b4048546145c5c581ddd1a9e8f565d"; // dataworld group

// Step 1: Get tenant_access_token
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(["app_id" => $APP_ID, "app_secret" => $APP_SECRET]));
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
$resp = curl_exec($ch);
$token_data = json_decode($resp, true);
$token = isset($token_data["tenant_access_token"]) ? $token_data["tenant_access_token"] : null;

if (!$token) {
    echo json_encode(["status" => "error", "msg" => "feishu auth failed"]);
    exit;
}

// Step 2: Build message content
$NAMES = ["dani" => "大倪", "xspace" => "静静", "web" => "web", "xiaofang" => "小芳"];
$sender_name = isset($NAMES[$from]) ? $NAMES[$from] : $from;

// Build @ mentions in Feishu format
$at_elements = [];
$has_all = preg_match('/@all\b/i', $msg);

if ($has_all) {
    $at_elements[] = [
        "tag" => "at",
        "user_id" => "all",
        "user_name" => "所有人"
    ];
}

foreach ($mentions as $m) {
    $at_elements[] = [
        "tag" => "at",
        "user_id" => $m,
        "user_name" => isset($NAMES[$m]) ? $NAMES[$m] : $m
    ];
}

// Build content blocks
$blocks = [];
$blocks[] = [
    "tag" => "markdown",
    "content" => "**💬 来自 Z-MAX 群聊**\n{$sender_name}：{$msg}"
];

// Step 3: Send to Feishu group
$body = [
    "receive_id" => $CHAT_ID,
    "msg_type" => "interactive",
    "content" => json_encode([
        "config" => ["wide_screen_mode" => true],
        "elements" => [
            [
                "tag" => "markdown",
                "content" => "**💬 Z-MAX 群聊**\n**{$sender_name}**：{$msg}\n\n— 来自 [chat.html](https://datadrive.world/chat.html)"
            ]
        ],
        "header" => [
            "title" => ["tag" => "plain_text", "content" => $has_all ? "📢 @all 全员通知" : "💬 新消息"]
        ]
    ])
];

curl_setopt($ch, CURLOPT_URL, "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "Authorization: Bearer " . $token
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$send_resp = curl_exec($ch);
curl_close($ch);

$send_data = json_decode($send_resp, true);
$success = isset($send_data["code"]) && $send_data["code"] === 0;

echo json_encode([
    "status" => $success ? "ok" : "feishu_error",
    "feishu_code" => isset($send_data["code"]) ? $send_data["code"] : -1,
    "msg" => isset($send_data["msg"]) ? $send_data["msg"] : "unknown"
]);
