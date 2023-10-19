import random

class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels=[]
        for i in range(len(neuron_counts)-1):
            self.levels.append(Level(neuron_counts[i], neuron_counts[i+1]))

    @staticmethod
    def feed_forward(given_inputs, network):
        outputs=Level.feed_forward(given_inputs, network.levels[0])
        for i in range(1, len(network.levels)):
            outputs=Level.feed_forward(outputs, network.levels[i])
        return outputs

class Level:
    def __init__(self, input_count, output_count):
        self.inputs=[0]*input_count
        self.outputs=[0]*output_count
        self.biases=[0]*output_count
        self.weights=[]

        #Connect every input node with output nodes
        for _ in range(input_count):
            self.weights.append([0 for _ in range(output_count)])

        # Assign random values to weights and biases for now
        self.randomize(self)

    @staticmethod
    def randomize(level):
        for i in range(len(level.inputs)):
            for j in range(len(level.outputs)):
                level.weights[i][j]=random.uniform(-1,1)

        for i in range(len(level.biases)):
            level.biases[i]=random.uniform(-1,1)

    @staticmethod
    def feed_forward(given_inputs, level):
        for i in range(len(level.inputs)):
            level.inputs[i]=given_inputs[i]

        for i in range(len(level.outputs)):
            sum=0
            for j in range(len(level.inputs)):
                sum+=level.inputs[j]*level.weights[j][i]
           
            if sum>level.biases[i]:
                level.outputs[i]=1
            else:
                level.outputs[i]=0

        return level.outputs
