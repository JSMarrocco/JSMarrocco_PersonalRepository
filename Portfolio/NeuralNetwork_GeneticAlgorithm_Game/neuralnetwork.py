import numpy as np

class NeuralNetwork():


    def __init__(self, sizeLayers):

        self.sizeLayers = sizeLayers
        self.nbLayers = len(sizeLayers)

        self.initHiddenLayers()


    def initHiddenLayers(self):
        '''
            initialize the hiddenLayers of the neural net by given them random weights and biases
        '''
        self.hiddenLayers = []
        sizeNextLayers = self.sizeLayers.copy()
        sizeNextLayers.pop(0)

        for i, sizeLayer in enumerate(sizeNextLayers):
            tmpLayer = []
            for j in range(0, sizeLayer):
                tmpWeights = []
                for k in range(0, self.sizeLayers[i]):
                    tmpWeights.append(np.random.uniform(-1, 1))
                tmpLayer.append({
                    'weights': tmpWeights,
                    'bias': np.random.uniform(-1, 1)
                })
            self.hiddenLayers.append(tmpLayer)


    def predict(self, inputs):
        '''
            calculate a prediction for the next move
        :param inputs: array of distances between the player and a wall
        :return: prediction
        '''
        prediction = inputs.copy()
        for layer in self.hiddenLayers:
            prediction = self.feedForward(prediction, layer)

        return prediction

    def feedForward(self, inputs, layer):
        '''

        :param inputs:
        :param layer: contains the outputs of the last layer
        :return: output
        '''
        tmpOutput = []
        for node in layer:

            z = 0
            for i in range(0, len(inputs)):
                v = (inputs[i] / 800) * 6 if inputs[i] > 6 else inputs[i]
                z += v * node['weights'][i]
            z += node['bias']

            tmpOutput.append(self.sigmoid(z))

        return tmpOutput


    def sigmoid(self, z):
        '''
            Activation function
        :param z: (x * weight) + bias
        :return: value between 0 and 1
        '''
        result = 1.0 / (1.0 + np.exp(-z))
        return result