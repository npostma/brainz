import Brain
import Visualize

# Make our brain. Agents are not yet implemented.
brain = Brain.Brain();

# Class for printing our brain whenever we want (debugging, use visual.show() for printing the brain in its current state)
visual = Visualize.Visualize(brain);

try:
    for (index) in range(0, 5000):
        #visual.show(); # Show can be placed after every learn or compute to show output the brain.
        # Traning set 0, No shipment and some order changes: Order won't go to the accountant. Order does not get changed anymore
        brain.learn([1, 0.09, 0, 0.04, 0.01, 0.00], [0, 0.3]);
        # Training set 1, unsure: Order won't go to the accountant. Order does get changed anymore
        brain.learn([1, 0.03, 0, 0.15, 0.80, 0.40], [0, 0.5]);
        # Training set 2, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        brain.learn([1, 0.05, 0, 0.02, 0.02, 0.40], [1, 0.8]);
        # Training set 3,  minimal change, order not payed:  Order won't go to the accountant. Order does not get changed anymore
        brain.learn([0, 0.04, 1, 0.01, 0.03, 0.03], [0, 1.0]);
        # Training set 4, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        brain.learn([1, 0.03, 0, 0.00, 0.01, 0.03], [1, 0.8]);
        # Training set 5, minimal change, order payed: Order goes to the accountant. Order does not get changed anymore
        brain.learn([1, 0.03, 1, 0.00, 0.00, 0.00], [1, 1.0]);
        # Training set 6, order not payed, no shipping party:  Order won't go to the accountant. Order will get changed
        brain.learn([0, 0.01, 0, 0.01, 0.02, 0.02], [0, 0.4]);
        # Training set 7, empty order: Order won't go to the accountant. Order will get changed
        brain.learn([0, 0.00, 0, 0.00, 0.00, 0.00], [0, 1.0]);
        # Training set 8, order not payed, no shipping party:  Order won't go to the accountant. Order will get changed
        brain.learn([0, 0.01, 0, 0.04, 0.00, 0.02], [0, 0.4]);

except ValueError as err:
    print(err.args)


# Now our brain leared some cases over and over. Now its time to start asking the brain questions
print ('=================================================================================');

brain.compute([1, 0.09, 0, 0.04, 0.01, 0.00]); # I expected someting like: [0, 0.3]
visual.showOutput();

brain.compute([1, 0.03, 0, 0.15, 0.80, 0.40]); # I expected someting like: [0, 0.5]
visual.showOutput();

brain.compute([0, 0.01, 0, 0.02, 0.02, 0.40]);  # I expected someting like: [1, 0.8]
visual.showOutput();


exit(1);
