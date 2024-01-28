#v.1.0
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
        self.weights = 0.000001*np.random.randn(n_outputs, n_inputs)
        self.biases = np.random.randn(n_outputs, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.biases

    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * output_gradient
        return np.dot(self.weights.T, output_gradient)

#Activation Layer
class Activation(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input):
        self.input = input
        return self.activation(self.input)

    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient, self.activation_prime(self.input))

#Tanh Activation Layer
class Tanh(Activation):
    def __init__(self):
        tanh = lambda x: np.tanh(x)
        tanh_prime = lambda x: 1- np.tanh(x) ** 2
        super().__init__(tanh, tanh_prime)

#Error
def mse(y_true, y_pred):    #Mean Squared Error
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / np.size(y_true)



'''
def solve_XOR():
    X = np.reshape([[0, 0], [0, 1], [1, 0], [1, 1]], (4, 2, 1))
    Y = np.reshape([[0], [1], [1], [0]], (4, 1, 1))
    
    network = [
        Dense(2,3),
        Tanh(),
        Dense(3,1),
        Tanh()
    ]
    epochs = 3000
    learning_rate = 0.1

    #train
    for e in range(epochs):
        error = 0
        for x, y in zip(X, Y):
            #forward
            output = x
            for layer in network:
                output = layer.forward(output)

            #error
            error = mse(y, output)

            #backward
            grad = mse_prime(y, output)
            for layer in reversed(network):
                grad = layer.backward(grad, learning_rate)
        error /= len(x)
        print('%d/%d, error=%f' %(e+1, epochs, error))



#solve_XOR()
'''