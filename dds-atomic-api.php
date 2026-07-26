<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$db = new SQLite3('/www/wwwroot/datadrive.world/dds.db');

$action = $_GET['action'] ?? 'list';

if ($action === 'list') {
    $cat = $_GET['cat'] ?? '';
    $sql = 'SELECT * FROM atomic_skills';
    if ($cat) {
        $stmt = $db->prepare($sql . ' WHERE category = :cat ORDER BY id');
        $stmt->bindValue(':cat', $cat, SQLITE3_TEXT);
        $result = $stmt->execute();
    } else {
        $result = $db->query($sql . ' ORDER BY category, id');
    }
    $skills = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $skills[] = $row;
    }
    echo json_encode($skills, JSON_UNESCAPED_UNICODE);
} elseif ($action === 'categories') {
    $result = $db->query('SELECT category, COUNT(*) as cnt FROM atomic_skills GROUP BY category ORDER BY cnt DESC');
    $cats = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $cats[] = $row;
    }
    echo json_encode($cats, JSON_UNESCAPED_UNICODE);
} elseif ($action === 'stats') {
    $total = $db->querySingle('SELECT COUNT(*) FROM atomic_skills');
    $cats = $db->querySingle('SELECT COUNT(DISTINCT category) FROM atomic_skills');
    echo json_encode(['total'=>$total, 'categories'=>$cats], JSON_UNESCAPED_UNICODE);
}

$db->close();
