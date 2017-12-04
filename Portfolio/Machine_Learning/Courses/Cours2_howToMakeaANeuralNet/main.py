###############################################
# Description:
#   Intro to Deep learning #2
#   How to make a neural network
#   from Siraj Raval
#
#
# Author: Jean-Simon Marrocco
# Date: 01-12-2017
################################################
from numpy import exp, array, random, dot

class NeuralNetwork():
    def __init__(self):
        # Seed the random numb gen, so it generates the same
        # numbers every time the program runs
        random.seed(1)
        
        #We model a single neuron, with 3 input connections and 1 output connection
        #We assign random weight to a 3x1 matrix, values in range -1 to 1
        #and mean 0
        self.synaptic_weights = 2 * random.random((3,1)) - 1

        
    #The sigmoid function, which describes an s shaped curves
    # we pass the weighted sum of the inputs through this function
    # to normalise them between 0 and 1
    def __sigmoid(self,x):
        return 1/(1+exp(-x))
    
    #gradient of the sigmoid curve
    def __sigmoid_derivative(self, x):
        return x * (1-x)

    def train(self, training_set_inputs, training_set_outputs,number_of_training_iteractions):
        for iteration in range(number_of_training_iteractions):
            #pass the training set through our neural net
            output = self.predict(training_set_inputs)
            
            #calc the error
            error = training_set_outputs - output
            
            #multiply the error by the input ad again by the gradient of the signmoid curve
            #PS: dot is the product of 2 array. For a 2d arrays its = to a matrix mult
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            
            #adjust the weights
            self.synaptic_weights += adjustment
    
    def predict(self,inputs):
        #pass inputs through our neural net
        return self.__sigmoid(dot(inputs, self.synaptic_weights))
    
        
if __name__ == '__main__':
    #init a single neural networks
    neural_network = NeuralNetwork()
    
    print('Random starting synaptic weighs:')
    print(neural_network.synaptic_weights)

    #The training set. We have 4 examples,each consiting of 3 inputs values
    #and 1 output value
    training_set_inputs = array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
    training_set_outputs = array([[0,1,1,0]]).T
    print('training input: \n',training_set_inputs)	
    print('training output: \n',training_set_outputs)
    #The .T accesses the attribute T of the object, which happens to be a NumPy array. 
    #The T attribute is the transpose of the array, see the documentation.

    #Train the neural network using a training set
    #Do it 10,000 times and make small adjustment each time
    neural_network.train(training_set_inputs,training_set_outputs,10000)

    print('New synaptic weights after training: ')
    print(neural_network.synaptic_weights)

    #test 
the neural network
    print('predicting: ')
    print('[1,0,0]')
    print(neural_network.predict(array([1,0,0])))

