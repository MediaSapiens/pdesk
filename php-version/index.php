<?php
	
require_once 'vendor/autoload.php';
require_once 'settings.php';

#readmine
$client = new \Redmine\Client('red.mediasapiens.co', $config['API_ACCESS_KEY']);


#$client->api('user')->all();
$test_list = $client->api('user')->listing();
#print_r ($test_list);

$test_user =  $client->api('user')->getIdByUsername('sfelde');
#$client->api('user')->getCurrentUser();

#print_r($test_user);
#$client->api('user')->getIdByUsername('kbsali');
#$client->api('user')->show($userId);



# var_dump($client);

$app = new \Slim\Slim(array(
    'debug' => true
));

$app->get('/hello/:name', function ($name) {
    echo "Hello, $name";

});
$app->run();



/*
$tmpl_folder = 'templates';

$tmpl_name = 'index.html';

$not_find_tmpl = '404.html';

$url_path = (empty($_SERVER['PATH_INFO']) ? @$_SERVER['SCRIPT_URL'] : @$_SERVER['PATH_INFO']);

if (!empty($url_path) && $url_path != "/"){
	$tmpl_name = sprintf('%s.html', substr($url_path, 1));
}

$loader = new Twig_Loader_Filesystem($tmpl_folder);

$twig = new Twig_Environment($loader, array(
    // 'cache' => 'tmp/compilation_cache',
));
//@todo: refactor
if(!file_exists($tmpl_folder . '/' . $tmpl_name)){
	$template = $twig->loadTemplate($not_find_tmpl);
}else{
	$template = $twig->loadTemplate($tmpl_name);
}

echo $template->render(array());

*/

?>
