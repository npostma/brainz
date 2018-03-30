import socket

HOST = '127.0.0.1'
PORT = 9010

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
socket.connect((HOST, PORT))


def normalize(value, minValue, maxValue):
    if (maxValue - minValue) <= 0:
        return 0

    normalized = (value - minValue) / (maxValue - minValue)

    return normalized


def deNormalize(normalized, minValue, maxValue):
    deNormalized = ((normalized * (maxValue - minValue)) + minValue)

    return deNormalized;

cases = [
    [0, 0],
    [1, 1],
    [1, 0],
    [0, 1],
]

print('Sending data')

for (caseNr, case) in enumerate(cases):
    # Slaapkamers, Afstand van centrum, Perceel oppervlakte, Inhoud, Tuin op zuinden, Groen
    socket.sendall(
        str("{\"command\": \"compute\", \"input\": [" + str(case[0]) + ", " + str(
            case[1]) + "]}" + '\n').encode())

    print('Wait for return')
    incomingBuffer = ''
    running = True
    while running:

        # For now accepting max message size of 2048 (Individual message!)
        dataStringRaw = socket.recv(2048)
        dataString = dataStringRaw.decode()

        if not dataString:
            break

        incomingBuffer = incomingBuffer + dataString
        strings = incomingBuffer.split('\n')
        for message in strings[:-1]:
            print ('Response for case' + str(case) + ': ')
            print(message)

            if '\0' in message:
                running = False

        incomingBuffer = strings[-1]

        # One response with a termination found.
        if '\0' in incomingBuffer:
            print(str(incomingBuffer))
            running = False

print('Shutting down')
# Graceful shutdown
socket.shutdown(1)
socket.close()

print('Exit')
