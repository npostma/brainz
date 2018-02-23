from PyQt5.QtCore import *

import json


# Socket server as a worker thread
class SocketClientProcessor(QThread):

    # Register signals that the clientProcessor can emit
    learn = pyqtSignal(list, list, name='learn')
    compute = pyqtSignal(list, list, name='compute')

    def __init__(self, connection, address, parent=None):
        super(SocketClientProcessor, self).__init__(parent)

        self.connection = connection
        self.address = address

    def run(self):
        incomingBuffer = ''

        while True:

            # For now accepting max message size of 2048 (Individual message!)
            dataStringRaw = self.connection.recv(2048)
            dataString = dataStringRaw.decode()

            if not dataString:
                break

            print('SocketServer: Input received.')

            incomingBuffer = incomingBuffer + dataString
            strings = incomingBuffer.split('\0')
            for message in strings[:-1]:
                try:
                    data = json.loads(message)

                    if data['command'] == 'learn':
                        self.learn.emit(data['input'], data['expectedOutput'])
                    elif data['command'] == 'compute':
                        self.compute.emit(data['input'], data['expectedOutput'])

                except ValueError as err:
                    print(('Data received (' + message + ') was in incorrect format.'))

            incomingBuffer = strings[-1]

        print('SocketServer: closing connection on this side.\n')
        self.connection.close()
