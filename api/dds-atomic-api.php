<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

// GET: list all atomic skills
$result = [];
$res = $db->query('SELECT * FROM atomic_skills ORDER BY category, id');
while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
    $result[] = $row;
}

echo json_encode($result, JSON_UNESCAPED_UNICODE);
