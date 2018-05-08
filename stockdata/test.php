<?php
//echo strtotime('2016-07-18 15:05');
//echo date('Y-m-d H:i:s', 1468497600);
//$map['a'] = 3;
//var_dump($map);

//echo time() - strtotime('20170124');
//echo '<br />';
//echo date('Y-m-d', 1486915200);

exec('python c:/test.py', $output);
foreach($output as $show)
    echo $show . '<br />';