from pathlib import Path

from collections import defaultdict, namedtuple

from sklearn.preprocessing import normalize
import numpy as np

from . import encoders
from . import kernels

class HDModel:
    def __init__(self,
            features,
            classes,
            encoder='nonlinear',
            encoder_args = dict(),
            d=20000,
            use_multiprocessing=True,
            learning_rate=0.035,
            kernel='cos',
            kernel_args = dict()):
        """ Initializes the HD model.

        Parameters
        -----------

        features: integer >= 1
            Number of features for the (unencoded) input data.

        classes: integer >= 1
            Number of classes for the target data.

        encoder: string, optional (default='nonlinear')
            Specifies the encoder type. Must be one of 'linear' or 'nonlinear'.
            See encoders.

        d: integer >= 1.
            Number of dimensions for the encoder.

        learning_rate: float >= 0.
            Learning rate.

        kernel: string, optional (default='dot')
            Specifies the kernel function for the model. Must be one of {‘dot’,
            ‘gauss’, ‘poly’, 'cos’}.

        kernel: dictionary, optional (default=None)
            Parameter dictionary for the kernel function.

        use_multiprocessing: Boolean.
            If true the generator will use multiprocessing for creating the
            basis.
        """
        try: assert learning_rate >= 0
        except: raise ValueError("Invalidad training rate {}".format(learning_rate))
        try: assert d >= 1 and int(d) == d
        except: raise ValueError("Invalid number of dimensions {}".format(d))
        try: assert features >= 1 and int(features) == features
        except: raise ValueError("Invalid number of features {}".format(features))
        try: assert classes >= 1 and int(classes) == classes
        except: raise ValueError("Invalid number of features {}".format(classes))
        # Initialize core attributes
        self.features = features
        self.classes = classes
        self.d = d
        self.weights = np.zeros((self.classes, self.d))

        self.learning_rate = learning_rate
        self.encoder = encoders.get_class(encoder)(d, features, **encoder_args)
        self.encoder.create_basis()
        self.kernel = kernels.get_kernel(kernel)
        self.kernel_args = kernel_args

    def fit(self,
            x,
            y,
            epochs=1,
            initial_epoch=0,
            verbose=1,
            validation_split=0.,
            sample_weight=None,
            class_weight=None,
            encode=True,
            **kwargs):
        """
        Trains the model on the given data.

        Parameters
        ----------
        encode: Boolean.
            If false the data wont be encoded (for already encoded data). Most
            of the use cases wont have to worry about this.

        x: iterable.
            Data to train on. Must have shape compatible with
            (len(x), self.features) if encode = True (default) or
            (len(x), self.d) if encode = False

        y: iterable.
            Target categorical labels (i.e. with shape (len(x), classes))

        epochs: integer >= 1.
            Number of epochs (including one shot training).

        verbose: 0 or 1.
            If 0 no messages will be printed.

        validation_split:  Float between 0 and 1.
            Fraction of the training data to be used as validation data. The
            model will set apart this fraction of the training data, will
            not train on it, and will evaluate the loss and any model
            metrics on this data at the end of each epoch. The validation
            data is selected from the last samples in the x and y data
            provided, before shuffling.

        class_weight: dictionary, optional.
            A dictionary mapping class indices (integers) to a weight (float)
            value, used for weighting the samples during training only. This can
            be useful to tell the model to "pay more attention" to samples from
            an under-represented class.

        sample_weight: iterable of floats, optional.
            Optional array of weights for the training samples, used for
            weighting during training only. Pass a flat (1D) array with
            the same length as the input samples (1:1 mapping between weights
            and samples)

        Returns:
        -------

        history: Dictionary with keys ["acc","val_acc"]
            Dictionary mapping metrics to arrays of size epochs with the
            corresponding values for each epoch.
        """
        # Ensure valid arguments
        x, y = self.standarize_data(x,y, encode, verbose = verbose)

        if sample_weight is None: sample_weight = [1 for _ in range(len(x))]
        if class_weight is None: class_weight = {i : 1 for i in range(self.classes)}
        try: assert len(sample_weight) == len(x)
        except: raise ValueError("Invalid sample_weight with len {}".format(len(sample_weight)))

        try: assert set(class_weight.keys()) == set([i for i in range(self.classes)])
        except: raise ValueError("Invalid class_weight keys")

        try: assert len(x) == len(y)
        except: raise ValueError("Input and target data length does not match")

        try: assert epochs >= 1
        except: raise ValueError("Invalid number of epochs: {}".format(epochs))

        try: assert verbose in [0,1]
        except: raise ValueError("Verbose level {} invalid".format(verbose))

        try:
            assert validation_split <= 1
            assert validation_split >= 0
        except: raise ValueError("Invalid validation_split {}".format(validation_split))

        # Split data
        data = [(x[i],y[i]) for i in range(len(x))]
        data_val = data[:int(len(data)*validation_split)]
        data = data[int(len(data)*validation_split):]
        xyize = lambda xys: ([d[0] for d in xys], [d[1] for d in xys])

        x, y = xyize(data)
        x_val, y_val = xyize(data_val)

        print("Training on {} samples validate on {}".format(len(x),len(x_val)))

        history = {"acc" : []}
        if len(x_val) > 0:
            history["val_acc"] = []

        for j in range(initial_epoch, initial_epoch + epochs):
            # One shot fit
            if verbose == 1: print("Epoch {}/{}".format(j+1, epochs))
            if j == 0:
                for i,(xi, yi) in enumerate(zip(x,y)):
                    label = np.argmax(yi)
                    xi_weight = self.learning_rate*class_weight[label]*sample_weight[i]
                    self.weights[label] += xi_weight*xi

            else:
                # Epoch train
                for i, (xi, yi) in enumerate(zip(x,y)):
                    guess = np.argmax(self.predict([xi], encode = False)[0])
                    label = np.argmax(yi)

                    # If the guess was wrong, update weights
                    if guess != label:
                        xi_weight_g = self.learning_rate*class_weight[guess]*sample_weight[i]
                        xi_weight_l = self.learning_rate*class_weight[label]*sample_weight[i]
                        self.weights[guess] -= xi_weight_g*xi
                        self.weights[label] += xi_weight_l*xi

            # Calculate metrics
            acc = self.evaluate(x, y, encode=False, verbose = verbose)
            history["acc"].append(acc)

            if len(x_val) > 0:
                val_acc = self.evaluate(x_val, y_val, encode=False, verbose = verbose)
                history["val_acc"].append(val_acc)
                if verbose == 1: print("acc: {}, val_acc: {}".format(acc, val_acc))

        
        History = namedtuple('History', ['history'])
        h = History(history)
        return h

    def predict(self, x, encode=True, verbose = 1):
        """
        Predict on the data using the model.

        Parameters
        ----------
        encode: Boolean.
            If false the data wont be encoded (for already encoded data).

        x: iterable. Data to predict on. Must have shape compatible with
            (len(x), self.features) if encode = True (default) or
            (len(x), self.d) if encode = False

        verbose: 0 or 1.
            If 0 no messages will be printed.

        Returns
        --------

        predictions: Numpy array of shape (len(x), len(classes)) with the distances of
        each sample to the hypervector of each class.
        """
        x = self.standarize_data(x,None,encode, verbose = verbose)
        predictions = list()
        for xi in x:
            predictions.append([self.kernel(self.weights[m], xi,
                **self.kernel_args) for m in range(self.classes)])
        return np.array(predictions)

    def evaluate(self, x, y, encode=True, verbose = 1):
        """
        Predict on the data using the model.

        Parameters
        ----------
        encode: Boolean.
            If false the data wont be encoded (for already encoded data).

        x: iterable. Data to predict on. Must have shape compatible with
            (len(x), self.features) if encode = True (default) or
            (len(x), self.d) if encode = False

        y: iterable.
            Target categorical labels (i.e. with shape (len(x), classes))

        verbose: 0 or 1.
            If 0 no messages will be printed.

        Returns
        -------

        acc: fraction on the input on which the models correctly predicted the
        target data.
        """
        yp = self.predict(x, encode=encode, verbose = verbose)
        yp = [np.argmax(yi) for yi in yp]
        y = [np.argmax(yi) for yi in y]

        hits = sum([int(ypi == yi) for ypi, yi in zip(yp, y)])

        return hits/len(x)

    def standarize_data(self, x, y, encode, verbose = 1):
        """
        For internal use.

        Converts x and y to numpy arrays and encodes x (if encode is True).
        Performs checks on the data which will raise ValueError.

        Parameters
        ----------
        encode: Boolean.
            If false the data wont be encoded (for already encoded data).

        x: iterable. Data to predict on. Must have shape compatible with
            (len(x), self.features) if encode = True (default) or
            (len(x), self.d) if encode = False

        y: iterable, or None.
            Target categorical labels (i.e. with shape (len(x), classes))

        verbose: 0 or 1.
            If 0 no messages will be printed.

        Returns
        -------

        acc: fraction on the input on which the models correctly predicted the
        target data.
        """
        if y is not None:
            y = np.array(y)
            try: y.shape == (len(x), self.classes)
            except: raise ValueError("Invalid target data shape with y shape {}\
            should be {}".format(y.shape, (len(x), self.classes)))

        if x is not None:
            x = np.array(x)
            if encode:
                try: assert x.shape == (len(x), self.features)
                except: raise ValueError("Input x shape {} incomptible with shape\
                        {}".format(x.shape, (len(x), self.features)))
                x = normalize(x, norm='l2')
                x = self.encoder.encode(x, verbose=verbose)
            else:
                try: assert x.shape == (len(x), self.d)
                except: raise ValueError("Input x shape {} incompatible with shape\
                        {} (encode=False was given)".format(x.shape, (len(x), self.d)))

        if y is not None and x is not None: return x, y
        elif x is not None: return x
        else: return y

    def summary(self):
        print("HDModel with dimension {} and classes {}. Input dimensions {}".format(self.d, self.classes, self.features))
