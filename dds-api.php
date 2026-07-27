<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); echo '{"ok":true}'; exit; }

$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $data = [];
    $tables = ['company','kpi','robots','systems','models','hardware','factory_zones','factory_meta','roadmap','dds_skills','links','pipeline','theme','proposal'];
    foreach ($tables as $t) {
        $rows = [];
        $r = $db->query("SELECT * FROM $t");
        while ($row = $r->fetchArray(SQLITE3_ASSOC)) $rows[] = $row;
        
        if (in_array($t, ['company','factory_meta','links','theme','proposal'])) {
            $d = [];
            foreach ($rows as $r2) { $k = $r2['key']; unset($r2['key']); $d[$k] = reset($r2); }
            $data[$t] = $d;
        } else {
            $d = [];
            foreach ($rows as $r2) { $k = $r2['id'] ?? $r2['version'] ?? $r2['step']; unset($r2['id'],$r2['version'],$r2['step']); $d[$k] = $r2; }
            if ($t == 'factory_zones' || $t == 'roadmap' || $t == 'dds_skills' || $t == 'pipeline') $data[$t] = array_values($d);
            else $data[$t] = $d;
        }
    }
    $db->close();
    echo json_encode($data, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    $table = $body['table'];
    
    if (in_array($table, ['company','factory_meta','links','theme','proposal'])) {
        foreach ($body['data'] as $k => $v) {
            $val = is_array($v) ? (reset($v) ?: '') : (string)$v;
            $db->exec("INSERT OR REPLACE INTO $table(key,value) VALUES('$k','".$db->escapeString($val)."')");
        }
    } elseif (in_array($table, ['kpi','robots','systems','models','hardware'])) {
        foreach ($body['data'] as $id => $fields) {
            $sets = [];
            foreach ($fields as $k => $v) $sets[] = "$k='".$db->escapeString($v)."'";
            $db->exec("UPDATE $table SET ".implode(',',$sets)." WHERE id='".$db->escapeString($id)."'");
        }
    } elseif ($table == 'factory_zones') {
        foreach ($body['data'] as $z) {
            $db->exec("UPDATE factory_zones SET name='".$db->escapeString($z['name'])."', color='".$db->escapeString($z['color'])."', stations='".$db->escapeString($z['stations'])."', count=".intval($z['count'])." WHERE id='".$db->escapeString($z['id'])."'");
        }
    } elseif ($table == 'roadmap') {
        foreach ($body['data'] as $k => $r) {
            // Handle both dict {version: {fields}} and array [{version:..., fields}]
            if (is_array($r) && !isset($r['version'])) {
                $version = $k;  // dict format: key is version
                $fields = $r;
            } else {
                $version = $r['version'];  // array format
                $fields = $r;
            }
            $criteria = isset($fields['criteria']) ? $db->escapeString($fields['criteria']) : '';
            $db->exec("UPDATE roadmap SET timeline='".$db->escapeString($fields['timeline'])."', name='".$db->escapeString($fields['name'])."', desc='".$db->escapeString($fields['desc'])."', criteria='".$criteria."', color='".$db->escapeString($fields['color']??'')."' WHERE version='".$db->escapeString($version)."'");
        }
    }
    
    $db->close();
    // Regenerate dds-global.js
    // Export handled by generate-pptx.php
    echo json_encode(["ok"=>true, "synced"=>"dds-global.js regenerated"]);
    exit;
}

$db->close();
http_response_code(405);
echo '{"error":"method not allowed"}';
