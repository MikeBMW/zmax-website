<?php
header('Content-Type: application/json; charset=utf-8');
$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

$rows = [];
$res = $db->query('SELECT * FROM changelog ORDER BY id DESC LIMIT 100');
while ($r = $res->fetchArray(SQLITE3_ASSOC)) $rows[] = $r;
echo json_encode($rows, JSON_UNESCAPED_UNICODE);
