from PyQt5.QtCore import *

import json


# Socket server as a worker thread
class SocketClientProcessor(QThread):

    # Register signals that the clientProcessor can emit
    learn = pyqtSignal(list, list, name='learn')
    compute = pyqtSignal(list, name='compute')

    def __init__(self, connection, address, parent=None):
        super(SocketClientProcessor, self).__init__(parent)

        self.connection = connection
        self.address = address

    def sendComputedResult(self, usedInputData, computedOutputData):
        print('Sending response')

        for(brainNr, brainResult) in enumerate(computedOutputData):
            self.connection.sendall((''.join(str(element) for element in brainResult) + '\n').encode());

        self.connection.sendall('exit\0'.encode());
        return

    def run(self):
        incomingBuffer = ''

        while True:

            # For now accepting max message size of 2048 (Individual message!)

            try:
                dataStringRaw = self.connection.recv(2048)
            except ConnectionResetError as err:
                # Client hung up ..... (not in a nice way) stop thread
                print("Houston we've lost a client.")
                return

            dataString = dataStringRaw.decode()

            if not dataString:
                break

            print('SocketServer: Input received.')

            incomingBuffer = incomingBuffer + dataString
            strings = incomingBuffer.split('\n')
            for message in strings[:-1]:
                try:
                    data = json.loads(message)

                    if data['command'] == 'learn':
                        self.learn.emit(data['input'], data['expectedOutput'])
                    elif data['command'] == 'compute':
                        self.compute.emit(data['input'])

                except ValueError as err:
                    print('Data received (' + message + ') was in incorrect format.')

            incomingBuffer = strings[-1]

        # Don't close connection. Client closed it in a graceful way
        return
