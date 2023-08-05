import numpy as np
import matplotlib.pyplot as plt

from .minimise_function import MinimiseFunction

class GradientDescent(MinimiseFunction):
    
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
    
    
    def minimise(self, theta_vector = None, alpha = 0.5, threshold = 0.05):
        """ Method which starts the gradient descent algorithm
        
        Args:
            theta_vector : Initial value of theta_vector to use in the algorithm
            
        Return:
            theta_vector : theta_value vector corresponding to our best hypothesis
            
        """
        if theta_vector:
            self.theta_vector = theta_vector
        else:
            self.theta_vector = self.default_theta_vector()
            
        num_iterations = 0
        prev_cost = float(0)
        
        hypothesis_output_vector = self.calculate_hypothesis_output()
        hypothesis_cost = self.calculate_hypothesis_cost(hypothesis_output_vector)
        
        while abs(hypothesis_cost - prev_cost) > threshold:
            num_iterations = num_iterations + 1
            
            self.theta_vector = self.calculate_new_theta_vector(hypothesis_output_vector, alpha)
            
            hypothesis_output_vector = self.calculate_hypothesis_output()
            prev_cost = hypothesis_cost
            hypothesis_cost = self.calculate_hypothesis_cost(hypothesis_output_vector)

            
        #Plot the curve
        plt.plot(self.X[:, 1], self.Y, 'ro')
        plt.plot(self.X[:, 1], hypothesis_output_vector)
        plt.show()
            
        return self.theta_vector
    
    
    def default_theta_vector(self):
        """ Method the generate initial values of theta parameter vector
        
        Args:
            None
            
        Return:
            Return a vector with all values initialised to 0
            
        """
        return np.zeros((self.num_features + 1, 1))
                
        
    def calculate_hypothesis_cost(self, hypothesis_output_vector):
        """ Method to calculate the output vector of our current hypothesis 
            which is represented by the theta_vector
            
        Args:
            hypothesis_output_vector : vector containing predictions for our input feature matrix X and current theta_vector
            
        Returns:
            float : cost of current hypothesis as compared to Y
            
        """
        cost = float(0)

        for index in range(self.num_examples):
            cost = cost + ((hypothesis_output_vector[index][0] - self.Y[index][0]) ** 2)
        
        return cost
        
        
    def calculate_new_theta_vector(self, hypothesis_output_vector, alpha):
        """ Method to calculate new values for the theta_vector based on current hypothesis
        
        Args:
            hypothesis_output_vector : current hypothesis output vector
            alpha : learning rate
            
        Returns:
            theta_vector : vector containing new values of theta
            
        """
        new_theta_vector = self.theta_vector
        
        for index in range(self.num_features + 1):
            diff_term = hypothesis_output_vector - self.Y
            diff_term = np.multiply(diff_term, self.X[:,index].reshape(self.num_examples, 1))
            derivative_term = 1.0 * alpha * np.sum(diff_term) / self.num_examples
            
            new_theta_vector[index][0] = new_theta_vector[index][0] - derivative_term
        
        return new_theta_vector
