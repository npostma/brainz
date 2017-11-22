import socket

HOST = '127.0.0.1'
PORT = 666
SIZEOF_UINT32 = 4

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
socket.send("{learn: {[1,1],[0]}}".encode())
socket.send("{learn: {[0,0],[0]}}".encode())
socket.send("{learn: {[0,1],[1]}}".encode())
socket.send("{learn: {[1,0],[1]}}".encode())

socket.send("{compute: [1,0]}".encode())