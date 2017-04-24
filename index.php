<?php
    $result = shell_exec('python ../scripts/trends.py');
    header("Location: html/welcome1.html");
    exit();

?>