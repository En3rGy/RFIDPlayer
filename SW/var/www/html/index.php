<?php

// configuration
$url = 'index.php';

$rep = array("\n", "\r");
$last_rfid = file_get_contents("/var/www/html/last_rfid.txt");
$last_rfid = str_replace($rep, "", $last_rfid);

// read the textfile
$file = '/var/www/html/rfid.json';
$text = file_get_contents($file);
$jsonData = json_decode($text, true);
$rfid_config = $jsonData["rfid"];

$sonosText = file_get_contents("/var/www/html/sonos.json");
$sonosData = json_decode($sonosText, true);

$testKey = key($rfid_config) . "album";


function getAlbumsOptions($selection) {
    // albums -> uri, title
    global $sonosData;

    $albums = $sonosData["albums"];
    foreach($albums as $album){
        echo '<option value="' . $album["title"] . '"';

        if ( $selection == $album["title"]) {
            echo ' selected="selected"';
        }
        echo '>' . $album["title"] . '</option>';
    }
}

// check if form has been submitted
if (isset($_POST['timeout']))
{
    // build json
    // config parma
    $jsonData["timeout"] = $_POST["timeout"];
    $jsonData["volume"] = $_POST["volume"];
    $jsonData["sonos_ip"]= $_POST["sonosip"];

    // save the text contents
    file_put_contents($file, str_replace("\r", '', json_encode($jsonData, JSON_PRETTY_PRINT)));

    // redirect to form again
    header(sprintf('Location: %s', $url));
    printf('<a href="%s">Moved</a>.', htmlspecialchars($url));
    exit();
}
elseif (isset($_POST[$testKey])) {
    // build json
    foreach( $rfid_config as $key => $value) {
        // album
        $rfid_config[$key]["album"] = $_POST[$key . "album"];
        // random
        $rfid_config[$key]["random"] = $_POST[$key . "random"];
    }

    $jsonData["rfid"] = $rfid_config;

    // save the text contents
    file_put_contents($file, str_replace("\r", '', json_encode($jsonData, JSON_PRETTY_PRINT)));

    // redirect to form again
    header(sprintf('Location: %s', $url));
    printf('<a href="%s">Moved</a>.', htmlspecialchars($url));
    exit();
}
?>

<html>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<head>
  <link rel="stylesheet" type="text/css" href="styles.css">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="manifest" href="/site.webmanifest">
</head>

<body>
<section id=menu>
<div>
<a href="#progconfig">Einstellungen</a>
<a href="#rfidconfig">RFID-Konfiguration</a>
<a href="#info">?</a>
</div>
</section>


<section id=maintitle>
<h1>RFID Player</h1>
<a id="progconfig"/></a>
</section>


<section id=progconfig>
<h2>Einstellungen</h2>
<p><form action="" method="post">
    <label for="timeout">Timeout zur Erkennung der gleichen RFID
        <input class="field-long" type="number" name="timeout" value="<?php echo $jsonData["timeout"] ?>"></input>
    </label>
    <label for="volume">Lautstärke
        <input class="field-long" type="number" name="volume" value="<?php echo $jsonData["volume"] ?>"></input>
    </label>
    <label for="sonosip">Lautsprecher
    <?php
    $speaker_data = $sonosData["speaker"];
    echo '<select name="sonosip" class="field-select">';
    echo '<option value="">--- Leer ---</option>';

    foreach($speaker_data as $speaker){
        echo '<option value="' . $speaker["ip_address"] . '"';

        if ($jsonData["sonos_ip"] == $speaker["ip_address"]) {
            echo ' selected="selected"';
        }
        echo '>' . $speaker["name"] . ' (' .$speaker["ip_address"] . ')</option>';
    }

    echo '</select></label><br>';
    ?>
    </label>

    <input type="submit" class="field-divided"/>
    <input type="reset" class="field-divided"/>
</form>
</p>
<a id="rfidconfig"></a>
</section>


<section id=rfidconfig>
<h2>RFID Konfiguration</h2>
<p><form action="" method="post">

<?php
$rfid_cfg = $jsonData["rfid"];


foreach ($rfid_cfg as $key => $val) {
    if (strcmp($last_rfid, $key) == 0) {
        echo '<fieldset class="last">';
        echo '<legend>' . $key . ' - Zuletzt verwendet</legend>';
    }
    else {
        echo '<fieldset>';
        echo '<legend>' . $key . '</legend>';
    }

    // Album
    echo '<label for="' . $key . 'album">Album<br>';
    //echo '<input class="field-long" name="' . $key . 'album" type ="text" value="' . $val["album"] . '"></input>';
    echo '<select name="' . $key . 'album" class="field-select">';
    echo '<option value="">--- Leer ---</option>';

    getAlbumsOptions( $val["album"]);

    echo '</select></label><br>';

    // random
    echo '<label for="' . $key . 'random">';
    echo '<input type="checkbox" name="' . $key . 'random" ';
    if ($val["random"]) {
        echo 'checked';
    }
    echo '>Zufällige Wiedergabe</input>';
    echo '</label>';
    echo '</fieldset>';
}
?>

    <input type="submit" class="field-divided"/>
    <input type="reset" class="field-divided"/>
</form>
</p>
<a id="info"></a>
</section>


<section id=info>
<h2>Info</h2>
<p>Copyright (c) 2020 Tobias Paul</p>
<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>
<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. </p>
</section>


</body>
</html>
