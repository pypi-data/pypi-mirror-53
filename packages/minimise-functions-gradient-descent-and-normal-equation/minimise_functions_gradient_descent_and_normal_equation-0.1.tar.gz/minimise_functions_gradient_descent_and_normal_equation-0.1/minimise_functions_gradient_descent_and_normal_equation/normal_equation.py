import numpy as np
import matplotlib.pyplot as plt

from .minimise_function import MinimiseFunction
from numpy.linalg import inv

class NormalEquation(MinimiseFunction):
    """ NormalEquation class to minimise a generic function
        
    Attributes:
        X (n*m feature matrix) representing the feature matrix of the observations. 
            n is the number of observations
            m is the number of features in an observation 
        Y (n*1 vector) representing the observed output value of our observations
        
    """
    
    def __init__(self, X = None, Y = None):
        """Gradient descent class to minimise a generic function 
        
        Attributes:
            X (n*m feature matrix) representing the feature matrix of the observations. 
                n is the number of observations
                m is the number of features in an observation 
                X should be provided without the extra column of 1s 
            Y (n*1 vector) representing the observed output value of our observations
            
        """
        MinimiseFunction.__init__(self, X, Y)
        
        
    def minimise(self):
        """ Method which starts the normal equation method
        
        Args:
            None
            
        Return:
            theta_vector : theta_value vector corresponding to our best hypothesis
            
        """
        X_transpose = self.X.T  
        self.theta_vector = inv(X_transpose.dot(self.X)).dot(X_transpose).dot(self.Y)  
        
        hypothesis_output_vector = self.calculate_hypothesis_output()
        
        #Plot the curve
        plt.plot(self.X[:, 1], self.Y, 'ro')
        plt.plot(self.X[:, 1], hypothesis_output_vector)
        plt.show()
      
        return self.theta_vector
    