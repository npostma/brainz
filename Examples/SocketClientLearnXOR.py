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


for (i) in range(0, 5000):

    cases = [
        [[1, 1], [0]],
        [[0, 0], [0]],
        [[1, 0], [1]],
        [[0, 1], [1]],
    ]

    for (caseNr, case) in enumerate(cases):
        inputData = case[0]
        expectedOutputData = case[1]

        # Slaapkamers, Afstand van centrum, Perceel oppervlakte, Inhoud, Tuin op zuinden, Groen
        socket.sendall(
            str("{\"command\": \"learn\", \"input\": [" + str(inputData[0]) + ", " + str(
                inputData[1]) + "], \"expectedOutput\": [" + str(expectedOutputData[0]) + "]}" + '\n').encode())

# Graceful shutdown
socket.shutdown(1)
socket.close()
