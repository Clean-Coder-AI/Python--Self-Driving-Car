Simple Neural Network with the same idea we will be using for our Self Driving Car.

Weights are numerical values associated with the connections between neurons in different layers of a neural network.
Each connection between two neurons has a weight that represents the strength of that connection. So, they control the contribution of input values to the final prediction. 

Weights are random from -1 to 1.
Biases are random from 0 to 1.

When input*weight'>'bias, output is 1 (Activate)
Else, input*weight'<'bias, output is 0 (Deactivate)

Our self Driving Car will be pressing one of the 4 keys(Forward,left,right,reverse) according to; if some sum is greater than bias or not, as well.