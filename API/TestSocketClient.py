import socket

HOST = '127.0.0.1'
PORT = 1337
SIZEOF_UINT32 = 4

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
socket.sendall("{\"command\": \"learn\", \"input\": [1,1], \"expectedOutput\": [0]}" + '\0')
socket.sendall("{\"command\": \"learn\", \"input\": [0,0], \"expectedOutput\": [0]}" + '\0')
socket.sendall("{\"command\": \"learn\", \"input\": [0,1], \"expectedOutput\": [1]}" + '\0')
socket.sendall("{\"command\": \"learn\", \"input\": [1,0], \"expectedOutput\": [1]}" + '\0')

socket.sendall("{\"command\": \"compute\", \"input\": [1,0], \"expectedOutput\": [1]}" + '\0')
