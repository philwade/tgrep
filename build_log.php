#! /usr/bin/php
<?php
date_default_timezone_set('America/New_York'); //I started to regret using php almost instantly
$start = strtotime("9 Feb 2011 06:52");
$end = strtotime("10 Feb 2011 07:11");

$routes = array("/r/programming", "/r/android", "/r/minecraft", "/r/food", "/r/cooking", "/r/fffffffuuuuuuuuuuuu", "/r/dwarffortress", "/r/hiphopheads", "/r/catpictures");
$requestString = "%s web03 \"GET %s\"\n";

$current = $start;
while($current < $end)
{
    $randRoute = $routes[array_rand($routes)];
    $randTimeStep = rand(0, 1);
    $current += $randTimeStep;
    $randTimeString = date("M d H:i:s", $current);
    echo sprintf($requestString, $randTimeString, $randRoute);
}
