import datetime

from AI import Population

start = datetime.datetime.now()

def trainPopulation(population):
    for (index) in range(0, 10):
        # visual.show() # Show can be placed after every learn or compute to show output the Population.
        # Traning set 0, No shipment and some order changes: Order won't go to the accountant. Order does not get changed anymore
        population.learn([1, 0.09, 0, 0.04, 0.01, 0.00], [0, 0.3])
        # Training set 1, unsure: Order won't go to the accountant. Order does get changed anymore
        population.learn([1, 0.03, 0, 0.15, 0.80, 0.40], [0, 0.5])
        # Training set 2, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        population.learn([1, 0.05, 0, 0.02, 0.02, 0.40], [1, 0.8])
        # Training set 3,  minimal change, order not payed:  Order won't go to the accountant. Order does not get changed anymore
        population.learn([0, 0.04, 1, 0.01, 0.03, 0.03], [0, 1.0])
        # Training set 4, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        population.learn([1, 0.03, 0, 0.00, 0.01, 0.03], [1, 0.8])
        # Training set 5, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        population.learn([1, 0.03, 1, 0.00, 0.00, 0.00], [1, 1.0])
        # Training set 6, order not payed, no shipping party:  Order won't go to the accountant. Order will get changed
        population.learn([0, 0.01, 0, 0.01, 0.02, 0.02], [0, 0.4])
        # Training set 7, empty order: Order won't go to the accountant. Order will get changed
        population.learn([0, 0.00, 0, 0.00, 0.00, 0.00], [0, 1.0])
        # Training set 8, order not payed, no shipping party:  Order won't go to the accountant. Order will get changed
        population.learn([0, 0.01, 0, 0.04, 0.00, 0.02], [0, 0.4])

# Create a random population
originalPopulation = Population.Population()
#Train them
trainPopulation(originalPopulation)
# Determine fitness
originalPopulation.compute([1, 0.09, 0, 0.04, 0.01, 0.00], [0, 0.3]) # I expected someting like: [0, 0.3]

nextGeneration = originalPopulation
for(generationNr) in range(1, 100) :
    nextGeneration = nextGeneration.breed()

    #Train them
    trainPopulation(nextGeneration)
    # Determine fitness
    nextGeneration.compute([1, 0.09, 0, 0.04, 0.01, 0.00], [0, 0.3]) # I expected someting like: [0, 0.3]

    thirdGeneration = nextGeneration.breed()
    print('===============================GENERATION ' + str(generationNr) + '================================')
    nextGeneration.showOutput()

end = datetime.datetime.now()
print('Duration:' + str(end-start))
exit(1)