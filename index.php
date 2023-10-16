<?php

$tuCurl = curl_init();

curl_setopt($tuCurl, CURLOPT_URL, "https://example.com/path/for/soap/url/");

$tuData = curl_exec($tuCurl);

if(!curl_errno($tuCurl)){

    $info = curl_getinfo($tuCurl);

    echo 'Took ' . $info['total_time'] . ' seconds to send a request to ' . $info['url'];

} else {

    echo 'Curl error: ' . curl_error($tuCurl);

}
