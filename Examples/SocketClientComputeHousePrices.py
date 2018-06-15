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
    [5, 5, 350, 280, 0], # Somewhere around 500 000?
    [3, 10, 450, 350, 0] # Somewhere around 175 000?
]

for (caseNr, case) in enumerate(cases):
    numBedRooms = normalize(case[0], 0, 6)
    distanceFromCityCenter = normalize(case[1], 0, 100)
    squareFeetGround = normalize(case[2], 200, 25000)
    cubicFeetContent = normalize(case[3], 200, 1000)
    gardenFacingSouth = normalize(case[4], 0, 1)

    print('Sending data')
    # Slaapkamers, Afstand van centrum, Perceel oppervlakte, Inhoud, Tuin op zuiden
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
            print('Response for case' + str(case) + ': ')
            returnValue = float(message)
            print(str(deNormalize(returnValue, 0, 2000000)))

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
