<?php
/**
 * PHP Example how to connect to the socketserver after running _Run_GUIMode_
 * Created by PhpStorm.
 * User: npostma
 * Date: 12/29/2017
 * Time: 8:43 AM
 */
error_reporting(E_ALL);

/* Allow the script to hang around waiting for connections. */
set_time_limit(0);

/* Turn on implicit output flushing so we see what we're getting
 * as it comes in. */
ob_implicit_flush(1);
ob_end_flush();

echo "<h2>TCP socket Connection</h2><br/>";

$port = 9010;

/* Get the IP address for the target host. */
$address = '10.102.10.69';

echo "Attempting to create a socket ... ";
/* Create a TCP/IP socket. */
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
	echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "<br/>";
} else {
	echo " OK.<br/>";
}

echo "Attempting to connect to '". $address . "' on port '" . $port . "' ... ";
$result = socket_connect($socket, $address, $port);
if ($result === false) {
	echo "socket_connect() failed.<br/>Reason: ($result) " . socket_strerror(socket_last_error($socket)) . "<br/>";
} else {
	echo " OK.<br/>";
}

echo "Sending request ... ";
for ($i = 0; $i < 1000; $i++) {
	$in = "{\"command\": \"learn\", \"input\": [1,1], \"expectedOutput\": [0]}\n";
	socket_write($socket, $in, strlen($in));
	echo $in . "<br/>";
	$in = "{\"command\": \"learn\", \"input\": [0,0], \"expectedOutput\": [0]}\n";
	socket_write($socket, $in, strlen($in));
	echo $in . "<br/>";
	$in = "{\"command\": \"learn\", \"input\": [0,1], \"expectedOutput\": [1]}\n";
	socket_write($socket, $in, strlen($in));
	echo $in . "<br/>";
	$in = "{\"command\": \"learn\", \"input\": [1,0], \"expectedOutput\": [1]}\n";
	socket_write($socket, $in, strlen($in));
	echo $in . "<br/>";
	$in = "{\"command\": \"compute\", \"input\": [1,0], \"expectedOutput\": [1]}\n";
	socket_write($socket, $in, strlen($in));
	echo $in . "<br/>";


}

echo " OK.<br/>";

echo "Reading response ...<br/><br/>";


while($out = socket_read($socket, 2048)) {
	if (strpos($out, "\n") !== false)  {
		# Empty buffer? done for today!
		echo 'Done for today';
		break;
	}
	echo $out . ", ";
}

echo "<br/><br/>";

echo "Gracefull shutdown off connection...";
socket_shutdown($socket);
echo "OK.<br/><br/>";

echo "Closing socket...";
socket_close($socket);
echo "OK.<br/><br/>";

flush();
exit;
