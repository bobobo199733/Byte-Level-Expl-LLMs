import numpy as np

def matrix_multiply(A, B):
    """
    This function multiplies two matrices A and B.
    
    Parameters:
    A (list of lists): The first matrix
    B (list of lists): The second matrix
    
    Returns:
    list of lists: The product of the two matrices
    """
    A = np.array(A)
    B = np.array(B)
    if A.shape[1] != B.shape[0]:
        raise ValueError('Matrices cannot be multiplied')
    product = np.matmul(A, B)
    return product.tolist()