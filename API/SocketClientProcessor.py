import socket
from PyQt4.QtCore import *

import json

HOST = '0.0.0.0'
PORT = 1337
SIZEOF_UINT32 = 4


# Socket server as a worker thread
class SocketClientProcessor(QThread):
    def __init__(self, connection, address, parent=None):
        super(SocketClientProcessor, self).__init__(parent)

        self.connection = connection
        self.address = address

    def run(self):
        recvBuffer = ""

        while True:

            # For now accepting max message size of 2048 (Individual message!)
            dataStringRaw = self.connection.recv(2048)
            dataString = dataStringRaw.decode()

            if not dataString:
                break

            print("SocketServer: Input received.")

            recvBuffer = recvBuffer + dataString
            strings = recvBuffer.split('\0')
            for message in strings[:-1]:
                try:
                    data = json.loads(message)

                    self.emit(SIGNAL(data['command']), data['input'], data['expectedOutput'])
                except ValueError as err:
                    print("Data received (" + message + ") was in incorrect format.")

                self.connection.sendall("Thanks");

            recvBuffer = strings[-1]

        print("SocketServer: closing connection on this side.\n")
        self.connection.close()