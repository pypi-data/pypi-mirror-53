import numpy as np
from tqdm import tqdm
import multiprocessing
import math

class Encoder:
    def __init__(self, d, features):
        """ Initializes the encoder.

        Parameters
        -----------
        d: integer >= 1.
            Number of dimensions for the encoder. This corresponds to the 

        features: integer >= 1
            Number of hypervectors for the encoders basis. This corresponds to
            the number of features for the (unencoded) input data.
        """
        try: assert d >= 1 and int(d) == d
        except: raise ValueError("Invalid number of dimensions {}".format(d))
        self.d = d
        self.features = features
        self.bases = self.create_basis()

    def create_basis(self):
        raise NotImplementedError

    def encode_sample(self):
        raise NotImplementedError

    def encode(self, samples, use_multiprocessing = True, verbose = 1):
        """
        Trains the model on the given data.

        Parameters
        ----------
        encode: Boolean. 
            If false the data wont be encoded (for already encoded data).

        samples: iterable. 
            Data to encode on. Must have shape
            (len(x), self.featuers) if encode = True (default) or
            (len(x), self.d) if encode = False

        verbose: 0 or 1. 
            If 0 no messages will be printed.

        Returns
        ------

        vectors: iterable
        Encoded samples.
        """
        if verbose == 0: tqdmizer = lambda x: x
        else: tqdmizer = lambda x: tqdm(x)

        if not use_multiprocessing:
            bases = list()
            it = tqdmizer(samples)
            for sample in it:
                bases.append(self.encode_sample(sample))
            return np.asarray(bases)

        with multiprocessing.Pool() as pool:
            it = pool.imap(self.encode_sample, samples, chunksize=100)
            it = tqdm(it, total=len(samples), desc="Encoding")
            res = np.array(list(it))
        return res


class EncoderNonLinear(Encoder):
    def __init__(self,d,features,mu = 0.0, sigma=1.0):
        self.mu = mu
        self.sigma = 1.0
        Encoder.__init__(self,d,features)

    def create_basis(self):
        bases = list()
        it = range(self.d)
        for i in it:
            bases.append(np.random.normal(self.mu, self.sigma, self.features))
        self.base = np.random.uniform(0, 2*math.pi, self.d)
        return np.asarray(bases)

    def encode_sample(self, sample):
        encoded = np.empty(self.d)
        for i in range(self.d):
            encoded[i] = np.cos(np.dot(sample, self.bases[i]) + self.base[i])
            encoded[i] *= np.sin(np.dot(sample, self.bases[i]))
        return encoded

class EncoderLinear(Encoder):
    def create_basis(self):
        base = np.zeros(self.d)
        bases = list()

        for i in range(int(self.d/2)):
            base[i] = 1
        for i in range(int(self.d/2), self.d):
            base[i] = -1

        it = range(self.features)
        for i in it:
            bases.append(np.random.permutation(base))
        return np.asarray(bases)

    def encode_sample(self, sample):
        encoded = np.zeros(self.d)
        for i in range(self.features):
            encoded += sample[i]*self.bases[i]
        return encoded

ENCODERS = {
    'linear':EncoderLinear,
    'nonlinear':EncoderNonLinear,
}

def get_class(encoder):
    try:
        return ENCODERS[encoder]
    except:
        raise ValueError('Could not interpret encoder identifier: ' + str(encoder))
