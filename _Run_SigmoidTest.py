import Brain
import MRI
import datetime

start = datetime.datetime.now()

# Make our brain. Agents are not yet implemented.
brain = Brain.Brain(2, 1)

for i in range (-100, 100):
    print str(i) + ":\t" + str(brain.sigmoid(i))