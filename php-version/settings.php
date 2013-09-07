<?php

#app settings 

$config = array(
	'API_ACCESS_KEY' => ''
);


if (file_exists('local_settings.php')){
	require_once 'local_settings.php';
}