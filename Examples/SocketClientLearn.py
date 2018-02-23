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


for (i) in range(0, 1):

    cases = [
        [[2, 10, 250, 300, 1], [120000]],
        [[2, 10, 350, 350, 0], [150000]],
        [[2, 10, 500, 450, 1], [250000]],
        [[2, 10, 1000, 450, 0], [500000]],
        [[3, 10, 250, 300, 1], [140000]],
        [[3, 10, 350, 350, 0], [170000]],
        [[3, 10, 500, 450, 1], [270000]],
        [[3, 10, 1000, 450, 0], [525000]],
        [[3, 5, 250, 300, 1], [240000]],
        [[3, 5, 350, 350, 0], [320000]],
        [[3, 5, 500, 450, 1], [420000]],
        [[3, 5, 1000, 450, 0], [725000]],
        [[4, 5, 250, 300, 1], [245000]],
        [[3, 5, 350, 350, 1], [370000]],
        [[4, 5, 500, 450, 1], [450000]],
        [[3, 5, 1000, 450, 1], [825000]],
        [[4, 25, 2500, 300, 1], [420000]],
        [[5, 1, 350, 350, 1], [1370000]],
        [[5, 5, 500, 550, 1], [650000]],
        [[5, 5, 1500, 550, 1], [1125000]],
        [[4, 25, 2500, 300, 1], [420000]],
        [[3, 25, 4500, 350, 0], [350000]],
        [[3, 25, 5000, 550, 1], [480000]],
        [[4, 35, 12000, 750, 1], [950000]]
    ]

    for (caseNr, case) in enumerate(cases):
        inputData = case[0]
        expectedOutputData = case[1]

        numBedRooms = normalize(inputData[0], 0, 6)
        distanceFromCityCenter = normalize(inputData[1], 0, 100)
        squareFeetGround = normalize(inputData[2], 200, 25000)
        cubicFeetContent = normalize(inputData[3], 200, 1000)
        gardenFacingSouth = normalize(inputData[4], 0, 1)

        priceOfHouse = normalize(expectedOutputData[0], 0, 2000000)

        # Slaapkamers, Afstand van centrum, Perceel oppervlakte, Inhoud, Tuin op zuinden, Groen
        socket.sendall(
            str("{\"command\": \"learn\", \"input\": [" + str(numBedRooms) + ", " + str(
                distanceFromCityCenter) + ", " + str(squareFeetGround) + ", " + str(cubicFeetContent) + ", " + str(
                gardenFacingSouth) + "], \"expectedOutput\": [" + str(priceOfHouse) + "]}" + '\0').encode())

# Graceful shutdown
socket.shutdown(1)
socket.close()
