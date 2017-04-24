<?php
    session_start();
    $url = $_GET['sfield'];
    $result = shell_exec('python ../scripts/currentSearch.py '.escapeshellarg($url));
    $_SESSION['choice'] = $url;
    header("Location: ../html/Demographic.html"); /* Redirect browser */
    exit();
?>