import numpy as np

class Layer:

    def __init__(self, layer_number, size, initial_weight, bias=True):
        self.layer_number = layer_number
        self.has_bias = bias
        self.size = size # The size of the non-bias neurons
        self.a = np.zeros(size)
        self.initial_weight = initial_weight

    # An iterator to loop through all thetas (Unused)
    # def __iter__(self):
    #     n = self.size
    #     if self.has_bias:
    #         n += 1
    #     if hasattr(self, 'theta'):
    #         for i in range(n):
    #             for j in range(self.next_size):
    #                 yield self.get_theta_at_index(i,j), lambda y: self.set_theta_at_index(i, j, y)
    #     else:
    #         yield None
    #         return

    # Initializes theta randomly, taking into account the initial weight constant and the
    # bias unit
    def initialize_theta(self, size):
        self.next_size = size
        if self.has_bias:
            self.theta = self.initial_weight*np.random.rand(self.size + 1, self.next_size)
        else:
            self.theta = self.initial_weight*np.random.rand(self.size, self.next_size)

    def fire(self):

        # Fires normally by returning g(theta*a')
        if hasattr(self, 'theta'):
            return self.sigmoid(np.dot(self.a, self.theta))
        # Fires abnormally by just returning a (usually happens on last layer)
        else:
            return self.a

    def iter_theta(self):
        # An iterator to loop through all thetas (Unused)
        n = self.size
        if self.has_bias:
            n += 1
        if hasattr(self, 'theta'):
            for i in range(n):
                for j in range(self.next_size):
                    yield self.theta[i,j]
        else:
            yield None

    def get_regularization(self):
        regularization = np.copy(self.theta)
        if self.has_bias:
            regularization[:,0] = np.zeros(regularization.shape[0])
        return regularization

    @property
    def a(self):
        return self.__a

    # A setter that takes into account the bias unit
    @a.setter
    def a(self, a):
        # m is the number of training examples
        m = a.size//self.size
        a = np.reshape(a,(m, self.size))
        if self.has_bias:
            # Appends a 1 to the beginning to account for bias
            a = np.concatenate((np.ones((m,1)),a),axis=1)
        # Transforms to column vector
        self.__a = a

    # Used with the lambda function in the "theta_unrolled" function in nn
    # def set_theta_at_index(self, i, j, value):
    #     self.theta[i,j] = value
    #
    # def get_theta_at_index(self, i, j):
    #     return self.theta[i,j]

    # Sigmoid and derivative of sigmoid functions for utility purposes

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_der(self):
        return np.multiply(self.a, (1-self.a))

    def display(self):
        print("Layer " + str(self.layer_number) + ":")
        print("Activations: ")
        print(self.a)
        if hasattr(self, 'theta'):
            print("Theta:\n" + str(self.theta))
        print("="*20)
