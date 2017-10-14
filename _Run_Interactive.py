import Brain
import random

# Make our brain. Agents are not yet implemented.
brain = Brain.Brain(1, 1)

userName = raw_input("Hi I am your househelp. I will kee you warm. What is your name? \n")

successCounter = 0
biggestSuccessStreak = 0;
tryCounter = 0;
iteration = 0;

def learn(brain, autoLearn = None):
    global successCounter
    global biggestSuccessStreak;
    global tryCounter;
    global iteration;

    iteration += 1;

    currentTemperature = round(random.uniform(13, 27), 1);
    brain.compute([currentTemperature])
    enableHeater = (brain.getOutput()[0] > 0.5)

    text = "I think the awnswer to the question 'Sould I turn the heater on'. Is:"
    if(enableHeater) :
        text = text + "[J/n] am I correct?"
    else:
        text = text + "[j/N] am i correct?"

    if(autoLearn == None):
        answerText = raw_input ("Hi " + userName + ", it is now " + str(currentTemperature) + ". " + text + "\n")
        answer = answerText == 'j' if 1 else 0
    else:
        print("Hi " + userName + ", it is now " + str(currentTemperature) + ". " + text + "\n")
        answer = currentTemperature < autoLearn;

    if(answer == enableHeater):
        successCounter += 1
    else:
        tryCounter += 1
        if (successCounter > biggestSuccessStreak):
            biggestSuccessStreak = successCounter;
        successCounter = 0

    if(answer == 1):
        brain.learn([currentTemperature], [1])
    elif(answer == 0):
        brain.learn([currentTemperature], [0])
    else:
        print ('Sorry sir, i do not know what you mean. XoXo')


print ("Hello " + userName + "! I will help you keep warm. \n")

while 1:
    learn(brain, 20);
    print("iteration:" + str(iteration) + "\ttryCounter:" + str(tryCounter) + "\tbiggestSuccessStreak:" + str(biggestSuccessStreak))

exit(1)