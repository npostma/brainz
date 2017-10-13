import Brain
import Visualize

# Make our brain. Agents are not yet implemented.
brain = Brain.Brain();

# Class for printing our brain whenever we want (debugging, use visual.show() for printing the brain in its current state)
visual = Visualize.Visualize(brain);

# Goal: Measure/Analyze user behavior before he sends an order to the accountant. Try to predict if my brain can see when he would send it to the accountant. And try to predict if the order will get changed

# Input before of a user sends his order to the accountant
# 1: Order payed (1 or 0)
# 2: Number of how many times the status of the order gets changed (Normal system usage will give us a number between 0 and 10 but higher values are posible)
# 3: Order send to 3th party shipping (1 or 0)
# 4: Number of how many times the order has changed Name,Address,Postal data (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))
# 5: Number of how many times the order has changed order rows (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))
# 6: Number of how many order rows added to the order (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))

# Output:
# 1: Chance that the order will be send to the accountant (Value between 0 and 1)
# 2: Percentage of completeness. (Value between 0 and 1, 1 means that that the order won't be changed and 0 means that the order most certainly will be changed)


# What do we watch? If an oder is paid and is send off to the shipping party  then most likely:
# 1 - The order can go to the accountant
# 2 - The order won't be changed

try:
    for (index) in range(0, 500):
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

except ValueError as err:
    print(err.args)


# Now our brain leared some cases over and over. Now its time to start asking the brain questions
print ('=================================================================================');

output = brain.compute([1, 0.03, 1, 0.00, 0.00, 0.00]);     # I expected someting like: [1, 0]
#output = brain.compute([1, 0.09, 0, 0.04, 0.01, 0.00]);    # I expected someting like: [0, 0.7]
visual.show();

for value in output:
    print str(value);

exit(1);
