import datetime

from MRI import CLI
from AI import Brain

start = datetime.datetime.now()

# Make our brain. Agents are not yet implemented.
brain = Brain.Brain(2, 1)

# Class for printing our brain whenever we want (debugging, use visual.show() for printing the brain in its current state)
visual = CLI.CLI(brain)
visual.show()

try:
    for (index) in range(0, 2500):
        brain.learn([0, 0], [0])
        brain.learn([1, 0], [1])
        brain.learn([0, 1], [1])
        brain.learn([1, 1], [0])

except ValueError as err:
    print(err.args)


# Now our brain leared some cases over and over. Now its time to start asking the brain questions
print ('=================================================================================')

brain.compute([0, 0]) # I expected someting like: [0]
brain.measureFitness([0])
visual.showOutput()

brain.compute([1, 0]) # I expected someting like: [1]
brain.measureFitness([1])
visual.showOutput()

brain.compute([0, 1])  # I expected someting like: [1]
brain.measureFitness([1])
visual.showOutput()

brain.compute([1, 1])  # I expected someting like: [0]
brain.measureFitness([0])
visual.showOutput()

end = datetime.datetime.now()
print('Duration:' + str(end-start))
exit(1)