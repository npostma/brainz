import random

from MRI import CLI
from AI import Brain

# This is not realy working. I think i need to much Q & A to get any result.

userName = input("Hi I am your househelp. I will keep you comfortable. What is your name? \n")

# [Statement, Min, Max, roundingOnDecimals]
inputDefinition = list()
inputDefinition.append(['The wind is blowing {} Bft', 0, 10, 0]) # Bft
inputDefinition.append(['The temperature is {}C indoors', -10, 33, 1]) # Degrees celcius indoors
inputDefinition.append(['It is {} percent sunny', 0, 100, 0]), # percentage of sun
inputDefinition.append(['It is raining {} mm per second', 0, 3, 2]) # Intensity mm per second outdoors :-)
#inputDefinition.append(['The air has a humidity of {}%', 20, 100, 1]) # Percentage of relative humidity indoors
#inputDefinition.append(['The barometric pressure is {} bar', 0.980, 1.050, 0]) # Air pressure is not uniform across the Earth however. The normal range of the Earth's air pressure is from 980 millibars (mb) to 1050 mb. These differences are the result of low and high air pressure systems which are caused by unequal heating across the Earth's surface and the pressure gradient force.

# [Answer, threshold]
outputDefinition = list()
outputDefinition.append(['I will turn on the heater', 0.5]) # If output is over 0.5 the heater will turn on
outputDefinition.append(['I will open the door to the garden', 0.5]) # If output is over 0.5 the doors will open

brain = Brain.Brain(len(inputDefinition), len(outputDefinition))

MRI = CLI.CLI(brain)
MRI.show()

successCounter = 0
biggestSuccessStreak = 0
tryCounter = 0
iteration = 0

def learn(brain):
    # Give answer.
    # Only learn from user input
    # Heater on / door open
    global successCounter
    global biggestSuccessStreak
    global tryCounter
    global iteration
    global inputDefinition

    iteration += 1

    inputs = list()
    for(inputRowNr, inputRow) in enumerate(inputDefinition):
        currentValue = round(random.uniform(inputRow[1], inputRow[2]), inputRow[3])
        inputs.append(currentValue)
        print(inputRow[0].format(currentValue))

    brain.compute(inputs)

    enableHeater = int(brain.getOutput()[0] > 0.5)
    openDoor = int(brain.getOutput()[1] > 0.5)

    print("\n================================================")

    text = "I know what to do! I will "

    if(enableHeater) :
        text += "enable the heater"
    else:
        text += "leave the heater off"

    text += " and "

    if (openDoor):
        text += "open the door to the garden"
    else:
        text += "leave the door to the garden closed"

    print(text)

    inputError = False
    allCorrect = True

    heaterAnswer = input("Was I right about the heater? [j/n]")
    if (heaterAnswer == 'n'):
        enableHeater = 1 - enableHeater # Flip the action
        allCorrect = False
    elif (heaterAnswer != 'j'):
        inputError = True
        allCorrect = False

    doorAnswer = input("Was I right about the door? [j/n]")
    if (doorAnswer == 'n'):
        openDoor = 1 - openDoor # Flip the action
    elif (doorAnswer != 'j'):
        inputError = True

    if(inputError):
        print("Input error. Cant learn from it")
    else:
        print("Learning output: [" + str(enableHeater) + ", " + str(openDoor) + "]")

        if(allCorrect):
            successCounter += 1
        else:
            tryCounter += 1
            if (successCounter > biggestSuccessStreak):
                biggestSuccessStreak = successCounter
            successCounter = 0

        brain.learn(inputs, [enableHeater, openDoor])

    print("\n\n")

print(("Dear " + userName + ", I will try to make you comfortable. \n"))

for(i) in range(0, 500):
    # Wind, Temp, Sun, Rain, Hum
    brain.learn([0, -10, 0, 0], [1, 0])
    brain.learn([4, 16, 0, 0], [1, 0])
    brain.learn([5, 20, 0, 0], [0, 1])
    brain.learn([8, 25, 0, 0], [0, 0])
    brain.learn([10, 30, 0, 0], [0, 0])

    # Wind, Temp, Sun, Rain, Hum
    brain.learn([5, 20, 37.5, 1], [0, 1])

    brain.learn([0, 20, 50, 1.5], [0, 0])
    brain.learn([0, 25, 50, 1.5], [0, 0])

    brain.learn([3, 10, 50, 2], [1, 0])

    brain.learn([4, 16, 62.5, 2.5], [1, 1])

    brain.learn([0, -10, 100, 3], [1, 0])
    brain.learn([4, 16, 100, 3], [1, 1])
    brain.learn([5, 20, 100, 3], [0, 0])
    brain.learn([10, 30, 100, 3], [0, 0])

    print(".")

    MRI.show()

while 1:
    learn(brain)
    print(("iteration:" + str(iteration) + "\ttryCounter:" + str(tryCounter) + "\tbiggestSuccessStreak:" + str(biggestSuccessStreak)))

exit(1)