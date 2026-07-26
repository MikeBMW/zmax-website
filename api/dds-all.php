<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

// POST: save data (editable mode)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input || !isset($input['table']) || !isset($input['data'])) {
        echo json_encode(['error'=>'invalid input']); exit;
    }
    $db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');
    $table = $input['table'];
    $data = $input['data'];
    
    if ($table === 'kpi') {
        foreach ($data as $key => $val) {
            $db->exec("UPDATE kpi SET value='".$db->escapeString($val['value'])."', unit='".$db->escapeString($val['unit'])."', label='".$db->escapeString($val['label'])."' WHERE id='".$db->escapeString($key)."'");
        }
    } elseif ($table === 'company') {
        foreach ($data as $key => $val) {
            $db->exec("UPDATE company SET value='".$db->escapeString($val)."' WHERE name='".$db->escapeString($key)."'");
        }
    } elseif ($table === 'systems') {
        foreach ($data as $key => $val) {
            $exists = $db->querySingle("SELECT COUNT(*) FROM systems WHERE id='".$db->escapeString($key)."'");
            if ($exists) {
                $db->exec("UPDATE systems SET name='".$db->escapeString($val['name'])."', hardware='".$db->escapeString($val['hardware'])."', gpu='".$db->escapeString($val['gpu'])."', ram='".$db->escapeString($val['ram'])."', role='".$db->escapeString($val['role'])."', model='".$db->escapeString($val['model'])."', color='".$db->escapeString($val['color'])."' WHERE id='".$db->escapeString($key)."'");
            }
        }
    } elseif ($table === 'robots') {
        foreach ($data as $key => $val) {
            $sets = [];
            if (isset($val['name'])) $sets[] = "name='".$db->escapeString($val['name'])."'";
            if (isset($val['level'])) $sets[] = "level='".$db->escapeString($val['level'])."'";
            if (isset($val['level_label'])) $sets[] = "level_label='".$db->escapeString($val['level_label'])."'";
            if (isset($val['desc'])) $sets[] = "desc='".$db->escapeString($val['desc'])."'";
            if (!empty($sets)) {
                $db->exec("UPDATE robots SET ".implode(',',$sets)." WHERE id='".$db->escapeString($key)."'");
            }
        }
    } elseif ($table === 'factory_zones') {
        foreach ($data as $key => $val) {
            $db->exec("UPDATE factory_zones SET stations=".intval($val['stations'])." WHERE id='".$db->escapeString($key)."'");
        }
    }
    echo json_encode(['status'=>'ok']);
    $db->close();
    exit;
}

// GET: serve all proposal data
$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

$data = [
    'company' => [],
    'kpi' => [],
    'robots' => [],
    'systems' => [],
    'factory_zones' => [],
    'roadmap' => [],
    'atomic_categories' => [],
    'generated_at' => date('Y-m-d H:i:s'),
];

// Company
$r = $db->query('SELECT key, value FROM company');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['company'][$row['key']] = $row['value'];
}

// KPI
$r = $db->query('SELECT * FROM kpi');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['kpi'][$row['id']] = [
        'value' => $row['value'], 'unit' => $row['unit'],
        'label' => $row['label'], 'icon' => $row['icon']
    ];
}

// Robots
$r = $db->query('SELECT * FROM robots');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['robots'][] = $row;
}

// Systems
$r = $db->query('SELECT * FROM systems');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['systems'][] = $row;
}

// Factory Zones
$r = $db->query('SELECT * FROM factory_zones');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['factory_zones'][] = $row;
}

// Roadmap
$r = $db->query('SELECT * FROM roadmap');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['roadmap'][] = $row;
}

// Pipeline
$r = $db->query('SELECT * FROM pipeline');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['pipeline'][] = $row;
}

// Atomic skills summary
$r = $db->query('SELECT category, COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['atomic_categories'][] = $row;
}
$data['atomic_total'] = $db->querySingle('SELECT COUNT(*) FROM atomic_skills');

// Links
$r = $db->query('SELECT * FROM links');
while ($row = $r->fetchArray(SQLITE3_ASSOC)) {
    $data['links'][] = $row;
}

$db->close();
echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
