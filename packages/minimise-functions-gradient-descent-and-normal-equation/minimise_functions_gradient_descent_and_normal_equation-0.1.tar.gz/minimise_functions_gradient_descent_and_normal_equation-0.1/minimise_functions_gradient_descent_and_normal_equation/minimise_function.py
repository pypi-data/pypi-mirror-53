import numpy as np
import matplotlib.pyplot as plt

class MinimiseFunction:
    
    def __init__(self, X = None, Y = None):
        
        """ Base implementation for the Gradient Descent and Normal Equation methods.
        this base class will be responsible for making sure that we have the input data
        
        Attributes:
        X (n*m feature matrix) representing the feature matrix of the observations. 
            n is the number of observations
            m is the number of features in an observation 
        Y (n*1 vector) representing the observed output value of our observations
        
        """
        if X:
            self.X = builder.X
            self.num_examples = self.X.shape[0]
            self.num_features = self.X.shape[1] - 1
        else:
            self.num_examples = 100
            self.num_features = 1
            self.X = self.default_single_feature_X()
        
        if Y:
            self.Y = Y
        else:
            self.Y = self.default_linear_related_Y()
            
        self.theta_vector = None
            
            
            
    def default_single_feature_X(self):
        """ Method to create some some sample values of X
            
        Args: 
            None
        
        Returns:
            return a 100*2 matrix with first column made of all 1s 
            and second column represents random observed values of the only feature involved
            
        """
        X = 2 * np.random.rand(self.num_examples, self.num_features)
        ones = np.ones((self.num_examples, 1))
        return np.concatenate((ones, X), axis=1)
    
    
    def default_linear_related_Y(self):
        """ Method to generate some linearly related values to the observed feature matrix X
        
        Args:
            None
            
        Returns:
            Returns a vector with randomised values linearly related to X. 
            Number of vales/rows in vector Y is equal to the number of observations (number of rows) in feature matrix X
            
        """
        
        Y = np.random.randn(self.num_examples, 1)

        for i in range(self.num_features + 1):
            rand = np.random.randint(1,10)
            col = self.X[:,i].reshape(self.num_examples, 1)
            Y = np.add(Y, col * rand)
        
        #Plot the curve
        plt.plot(self.X[:, 1], Y, 'ro')
        plt.show()
        
        return Y
    
    
    def calculate_hypothesis_output(self):
        """ Method to calculate the output vector of our current hypothesis 
            which is represented by the theta_vector
            
        Args:
            None
            
        Returns:
            h(theta_vector) : vector of predicted values for observed feature matrix X
            
        """
        return np.matmul(self.X, self.theta_vector)
    