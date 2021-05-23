import cvxpy as cp
import numpy as np

def BVLS(y, eps, batch=False):
    """Computes the bounded variable least squares solution for a given problem.

    Setting batch to true constrains the final solution to be have its first
    value equal to the first measurement. This is essential in batch-based
    filtering, where the first value of the next batch should be equal to the 
    last value of the last filtered batch.

    Args:
        y: List of measurements.
        eps: Universal relative bound.
        batch: If true, the first value of the measurements is constrained to be
            equal to the first value in the measurements. Else, both end points
            are unconstrained.
    
    Returns:
        The filtered signal.
    """
    n = len(y)
    
    y = np.asarray(y)
    y = y.reshape((n,1))
        
    C = np.zeros((2*n-2, n))
    
    for k in range(1,n-1):
        C[2*k-1,k] = 1
        C[2*k-1,k+1] = -1
        C[2*k,k] = 1
        C[2*k,k-1] = -1
        
    eps = np.asarray(eps)
    eps = eps.reshape((2*n-2,1))
    
    x = cp.Variable((len(y),1))
    objective = cp.Minimize(cp.norm(x - y,2))
    
    if batch:
        constraints = [cp.abs(C*x) <= eps]
    else:
        constraints = [cp.abs(C*x) <= eps, x[0] == y[0]]
    
    prob = cp.Problem(objective, constraints)

    result = prob.solve()
    
    return (x, result)