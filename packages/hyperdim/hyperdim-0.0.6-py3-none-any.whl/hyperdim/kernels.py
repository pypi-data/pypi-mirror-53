import numpy as np

def gauss_kernel(x, y, std=25):
    res = np.linalg.norm(x - y)
    res = res**2
    res *= -1
    res = n/(2*(std**2))
    res = np.exp(n)
    return res

def poly_kernel(x, y, c=3, d=5):
    return (np.dot(x, y) + c)**d

def cos_kernel(x, y):
    return np.dot(x, y)/(np.linalg.norm(x)*np.linalg.norm(y))

KERNELS = {
        'dot': np.dot,
        'gauss': gauss_kernel,
        'poly': poly_kernel,
        'cos': cos_kernel
}

def get_kernel(kernel):
    """
    Parameters
    ---------
    kernel: string
        Specifies the kernel function for the model. Must be one of {‘dot’,
        ‘gauss’, ‘poly’, 'cos’}.

    Returns
    -------
    kernel: function
        The specified kernel function.
    """
    return KERNELS[kernel]
