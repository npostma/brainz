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


def deNormalize(normalized, maxValue, minValue):
    deNormalized = (normalized * (maxValue - minValue) + minValue)

    return deNormalized;

cases = [
    [2, 10, 250, 300, 1],
    [4, 5, 350, 350, 0],
    [5, 10, 500, 450, 1],
    [3, 10, 1000, 450, 0],
    [2, 10, 250, 300, 1]
]

inputData = cases[0]

numBedRooms = normalize(inputData[0], 0, 6)
distanceFromCityCenter = normalize(inputData[1], 0, 100)
squareFeetGround = normalize(inputData[2], 200, 25000)
cubicFeetContent = normalize(inputData[3], 200, 1000)
gardenFacingSouth = normalize(inputData[4], 0, 1)

print('Sending data')
# Slaapkamers, Afstand van centrum, Perceel oppervlakte, Inhoud, Tuin op zuinden, Groen
socket.sendall(
    str("{\"command\": \"compute\", \"input\": [" + str(numBedRooms) + ", " + str(
        distanceFromCityCenter) + ", " + str(squareFeetGround) + ", " + str(cubicFeetContent) + ", " + str(
        gardenFacingSouth) + "]}" + '\n').encode())

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
        returnValue = float(message)
        print(str(deNormalize(returnValue, 0, 20000000)))

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
