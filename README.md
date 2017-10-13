# brainz
brainz

Experimental project to understand the working of a FFNN

### Goal: 
Measure/Analyze user behavior before he sends an order to the accountant. Try to predict if my brain can see when he would send it to the accountant. And try to predict if the order will get changed

### Input:
Input before of a user sends his order to the accountant
- 1: Order payed (1 or 0)
- 2: Number of how many times the status of the order gets changed (Normal system usage will give us a number between 0 and 10 but higher values are posible)
- 3: Order send to 3th party shipping (1 or 0)
- 4: Number of how many times the order has changed Name,Address,Postal data (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))
- 5: Number of how many times the order has changed order rows (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))
- 6: Number of how many order rows added to the order (Normal system usage will give us a number between 0 and 0.1. 1 change = 0.01. 1 means 100 times (max))

### Output:
- 1: Chance that the order will be send to the accountant (Value between 0 and 1)
- 2: Percentage of completeness. (Value between 0 and 1, 1 means that that the order won't be changed and 0 means that the order most certainly will be changed)


### What do we watch? 
If an oder is paid and is send off to the shipping party  then most likely:
- 1 - The order can go to the accountant
- 2 - The order won't be changed
