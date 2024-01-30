#v.1.1
import numpy as np

#Layer
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        pass

    def backward(self, output, learning_rate):
        pass


#Dense Layer
class Dense(Layer):  #output = weight*input+bias
    def __init__(self, n_inputs, n_outputs): #n_outouts is number of neurons
        self.weights = np.random.randn(n_outputs, n_inputs)
        self.biases = np.random.randn(n_outputs, 1)
        print(f'WEIGHTS: {self.weights}')
        #print(f'BIAS: {self.biases}')

    def forward(self, input):
        self.input = input
        #print(input)
        return np.dot(self.weights, self.input) + self.biases

    def backward(self, output_gradient, learning_rate):
        pass

#Activation Layer
class Activation(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input):
        self.input = input
        #print(input)
        return self.activation(self.input)

    def backward(self, output_gradient, learning_rate):
        pass

#Rectified Linear Unit
class ReLU(Activation):
    def __init__(self):
        super().__init__(self.relu, self.relu_prime)

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def relu_prime(x):
        pass

class SoftMax(Activation):
    def __init__(self):
        super().__init__(self.softmax, self.softmax_prime)
    @staticmethod
    def softmax(x):
        exp_values = np.exp(x - np.max(x, axis=-1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=-1, keepdims=True)
        return probabilities
    @staticmethod
    def softmax_prime(x):
        pass

class Loss():
    pass




#THE NEURAL NETWORK

class Neural_Network:
    def __init__(self, data):
        self.X = np.array(data)
        self.label = np.array([[0], [1], [2], [3], [4], [5]])

        self.learning_rate = 0.1
        self.error = 0

        self.network = [
            Dense(12,24),
            ReLU(),
            Dense(24,6),
            SoftMax()
        ]

        print(self.X)
        #print(self.X.shape)
        print(self.label)
        #print(self.label.shape)

    def train(self):
        for x, y in zip(self.X, self.label):
            output = x

            for layer in self.network:
                output = layer.forward(output)

            self.error = np.mean((output - y) ** 2)

            print('error=%f' % (self.error))
            print(f'output: {output}')

    def normalize(self):
        pass

    def save(self):
        pass

    def load(self):
        pass