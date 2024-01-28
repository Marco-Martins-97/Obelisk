#v.1.2
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
        #print(input)
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
        #print(input)
        return self.activation(self.input)

    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient, self.activation_prime(self.input))

#Tanh Activation Layer
class Tanh(Activation):
    def __init__(self):
        super().__init__(self.tanh, self.tanh_prime)

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def tanh_prime(x):
        return 1 - np.tanh(x) ** 2


class ReLU(Activation):
    def __init__(self):
        super().__init__(self.relu, self.relu_prime)

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def relu_prime(x):
        return np.where(x > 0, 1, 0)

        
class SoftMax(Activation):
    def __init__(self):
        super().__init__(self.softmax, self.softmax_prime)
    @staticmethod
    def softmax(x):
        max_val = np.max(x, axis=0, keepdims=True)
        exp_values = np.exp(x - max_val)
        probabilities = exp_values / np.sum(exp_values, axis=0, keepdims=True)
        return probabilities
    @staticmethod
    def softmax_prime(x):
        # Adjust as needed
        return np.ones_like(x)

#Error
#Mean Squared Error
def mse(y_true, y_pred):    
    return np.mean(np.power(y_true - y_pred, 2))

#Mean Squared Error Derivative
def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / np.size(y_true)

# Cross-Entropy Loss
def cross_entropy(y_true, y_pred):
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.sum(y_true * np.log(y_pred)) / len(y_true)

# Cross-Entropy Loss Derivative
def cross_entropy_prime(y_true, y_pred):
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -(y_true / y_pred) / len(y_true)

