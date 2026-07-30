<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$file = $_GET['file'] ?? '';
if (!$file) { echo json_encode(['error'=>'no file']); exit; }

$dir = __DIR__ . '/diagrams';
$path = $dir . '/' . basename($file);
if (!file_exists($path)) { echo json_encode(['error'=>'not found']); exit; }

$raw = file_get_contents($path);

// Extract encoded diagram
preg_match('/content="([^"]*)"/', $raw, $m);
if (!$m) { echo json_encode(['error'=>'no content']); exit; }

$decoded = html_entity_decode($m[1]);
preg_match('/<diagram[^>]*>(.*?)<\/diagram>/s', $decoded, $dm);
if (!$dm) { echo json_encode(['error'=>'no diagram']); exit; }

$bin = base64_decode($dm[1]);
$xml = gzinflate(substr($bin, 2)); // strip zlib header
$xml = rawurldecode($xml);

// Parse cells and edges
$nodes = [];
$edges = [];

preg_match_all('/<mxCell([^>]*?)(\/?)>/s', $xml, $cells, PREG_SET_ORDER);

foreach ($cells as $cell) {
    $attrs = $cell[1];
    $isEdge = strpos($attrs, 'edge="1"') !== false;
    $isVertex = strpos($attrs, 'vertex="1"') !== false;

    preg_match('/id="([^"]*)"/', $attrs, $idm);
    $cid = $idm[1] ?? '';

    if ($isEdge) {
        preg_match('/source="([^"]*)"/', $attrs, $sm);
        preg_match('/target="([^"]*)"/', $attrs, $tm);
        if ($sm && $tm) {
            $edges[] = ['source' => $sm[1], 'target' => $tm[1]];
        }
        continue;
    }

    if ($isVertex) {
        preg_match('/value="([^"]*)"/', $attrs, $vm);
        if (!$vm) continue;
        $text = html_entity_decode($vm[1]);
        $text = strip_tags($text);
        $text = html_entity_decode($text);
        $text = trim($text);
        if (!$text) continue;

        // Get geometry from inner mxGeometry
        $x = 0; $y = 0; $w = 0; $h = 0;
        preg_match('/<mxGeometry[^>]*x="([^"]*)"/s', $cell[0], $xm);
        preg_match('/<mxGeometry[^>]*y="([^"]*)"/s', $cell[0], $ym);
        preg_match('/<mxGeometry[^>]*width="([^"]*)"/s', $cell[0], $wm);
        preg_match('/<mxGeometry[^>]*height="([^"]*)"/s', $cell[0], $hm);

        preg_match('/style="([^"]*)"/', $attrs, $stm);
        $style = $stm[1] ?? '';

        $nodes[] = [
            'id' => $cid,
            'text' => $text,
            'x' => $xm ? floatval($xm[1]) : 0,
            'y' => $ym ? floatval($ym[1]) : 0,
            'w' => $wm ? floatval($wm[1]) : 100,
            'h' => $hm ? floatval($hm[1]) : 50,
            'style' => $style
        ];
    }
}

echo json_encode(['nodes' => $nodes, 'edges' => $edges], JSON_UNESCAPED_UNICODE);
