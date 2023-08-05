from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from scipy import sparse
from scipy.signal import butter, lfilter
from scipy.stats import norm
from sklearn import base
from statsmodels.distributions.empirical_distribution import ECDF
import logging
import numpy as np
import pandas as pd


NAN_INT = 7535805
logger = logging.getLogger('Kaggler')


class QuantileEncoder(base.BaseEstimator):
    """QuantileEncoder encodes numerical features to quantile values.

    Attributes:
        ecdfs (list of empirical CDF): empirical CDFs for columns
        n_label (int): the number of labels to be created.
    """

    def __init__(self, n_label=10, sample=100000, random_state=42):
        """Initialize a QuantileEncoder class object.

        Args:
            n_label (int): the number of labels to be created.
            sample (int or float): the number or fraction of samples for ECDF
        """
        self.n_label = n_label
        self.sample = sample
        self.random_state = random_state

    def fit(self, X, y=None):
        """Get empirical CDFs of numerical features.

        Args:
            X (pandas.DataFrame): numerical features to encode

        Returns:
            A trained QuantileEncoder object.
        """
        def _calculate_ecdf(x):
            return ECDF(x[~np.isnan(x)])

        if self.sample >= X.shape[0]:
            self.ecdfs = X.apply(_calculate_ecdf, axis=0)
        elif self.sample > 1:
            self.ecdfs = X.sample(n=self.sample,
                                  random_state=self.random_state).apply(
                                      _calculate_ecdf, axis=0
                                  )
        else:
            self.ecdfs = X.sample(frac=self.sample,
                                  random_state=self.random_state).apply(
                                      _calculate_ecdf, axis=0
                                  )

        return self

    def fit_transform(self, X, y=None):
        """Get empirical CDFs of numerical features and encode to quantiles.

        Args:
            X (pandas.DataFrame): numerical features to encode

        Returns:
            Encoded features (pandas.DataFrame).
        """
        self.fit(X, y)

        return self.transform(X)

    def transform(self, X):
        """Encode numerical features to quantiles.

        Args:
            X (pandas.DataFrame): numerical features to encode

        Returns:
            Encoded features (pandas.DataFrame).
        """
        for i, col in enumerate(X.columns):
            X.loc[:, col] = self._transform_col(X[col], i)

        return X

    def _transform_col(self, x, i):
        """Encode one numerical feature column to quantiles.

        Args:
            x (pandas.Series): numerical feature column to encode
            i (int): column index of the numerical feature

        Returns:
            Encoded feature (pandas.Series).
        """
        # Map values to the emperical CDF between .1% and 99.9%
        rv = np.ones_like(x) * -1

        filt = ~np.isnan(x)
        rv[filt] = np.floor((self.ecdfs[i](x[filt]) * 0.998 + .001) *
                            self.n_label)

        return rv


class Normalizer(base.BaseEstimator):
    """Normalizer that transforms numerical columns into normal distribution.

    Attributes:
        ecdfs (list of empirical CDF): empirical CDFs for columns
    """

    def fit(self, X, y=None):
        self.ecdfs = [None] * X.shape[1]

        for col in range(X.shape[1]):
            self.ecdfs[col] = ECDF(X[:, col])

        return self

    def transform(self, X):
        """Normalize numerical columns.

        Args:
            X (numpy.array) : numerical columns to normalize

        Returns:
            (numpy.array): normalized numerical columns
        """

        for col in range(X.shape[1]):
            X[:, col] = self._transform_col(X[:, col], col)

        return X

    def fit_transform(self, X, y=None):
        """Normalize numerical columns.

        Args:
            X (numpy.array) : numerical columns to normalize

        Returns:
            (numpy.array): normalized numerical columns
        """

        self.ecdfs = [None] * X.shape[1]

        for col in range(X.shape[1]):
            self.ecdfs[col] = ECDF(X[:, col])
            X[:, col] = self._transform_col(X[:, col], col)

        return X

    def _transform_col(self, x, col):
        """Normalize one numerical column.

        Args:
            x (numpy.array): a numerical column to normalize
            col (int): column index

        Returns:
            A normalized feature vector.
        """

        return norm.ppf(self.ecdfs[col](x) * .998 + .001)


class LabelEncoder(base.BaseEstimator):
    """Label Encoder that groups infrequent values into one label.

    Attributes:
        min_obs (int): minimum number of observation to assign a label.
        label_encoders (list of dict): label encoders for columns
        label_maxes (list of int): maximum of labels for columns
    """

    def __init__(self, min_obs=10):
        """Initialize the OneHotEncoder class object.

        Args:
            min_obs (int): minimum number of observation to assign a label.
        """

        self.min_obs = min_obs

    def __repr__(self):
        return ('LabelEncoder(min_obs={})').format(self.min_obs)

    def _get_label_encoder_and_max(self, x):
        """Return a mapping from values and its maximum of a column to integer labels.

        Args:
            x (pandas.Series): a categorical column to encode.

        Returns:
            (tuple):
                - (dict): mapping from values of features to integers
                - (int): maximum label
        """

        # NaN cannot be used as a key for dict. Impute it with a random
        # integer.
        label_count = x.fillna(NAN_INT).value_counts()
        n_uniq = label_count.shape[0]

        label_count = label_count[label_count >= self.min_obs]
        n_uniq_new = label_count.shape[0]

        # If every label appears more than min_obs, new label starts from 0.
        # Otherwise, new label starts from 1 and 0 is used for all old labels
        # that appear less than min_obs.
        offset = 0 if n_uniq == n_uniq_new else 1

        label_encoder = pd.Series(np.arange(n_uniq_new) + offset,
                                  index=label_count.index)
        max_label = label_encoder.max()
        label_encoder = label_encoder.to_dict()

        return label_encoder, max_label

    def _transform_col(self, x, i):
        """Encode one categorical column into labels.

        Args:
            x (pandas.Series): a categorical column to encode
            i (int): column index

        Returns:
            (pandas.Series): a column with labels.
        """
        return x.fillna(NAN_INT).map(self.label_encoders[i]).fillna(0)

    def fit(self, X, y=None):
        self.label_encoders = [None] * X.shape[1]
        self.label_maxes = [None] * X.shape[1]

        for i, col in enumerate(X.columns):
            self.label_encoders[i], self.label_maxes[i] = \
                self._get_label_encoder_and_max(X[col])

        return self

    def transform(self, X):
        """Encode categorical columns into label encoded columns

        Args:
            X (pandas.DataFrame): categorical columns to encode

        Returns:
            (pandas.DataFrame): label encoded columns
        """

        for i, col in enumerate(X.columns):
            X.loc[:, col] = self._transform_col(X[col], i)

        return X

    def fit_transform(self, X, y=None):
        """Encode categorical columns into label encoded columns

        Args:
            X (pandas.DataFrame): categorical columns to encode

        Returns:
            (pandas.DataFrame): label encoded columns
        """

        self.label_encoders = [None] * X.shape[1]
        self.label_maxes = [None] * X.shape[1]

        for i, col in enumerate(X.columns):
            self.label_encoders[i], self.label_maxes[i] = \
                self._get_label_encoder_and_max(X[col])

            X.loc[:, col] = (X[col].fillna(NAN_INT)
                             .map(self.label_encoders[i])
                             .fillna(0))

        return X


class OneHotEncoder(base.BaseEstimator):
    """One-Hot-Encoder that groups infrequent values into one dummy variable.

    Attributes:
        min_obs (int): minimum number of observation to create a dummy variable
        label_encoders (list of (dict, int)): label encoders and their maximums
                                              for columns
    """

    def __init__(self, min_obs=10):
        """Initialize the OneHotEncoder class object.

        Args:
            min_obs (int): minimum number of observations required to create
                a dummy variable
            label_encoder (LabelEncoder): LabelEncoder that transofrm
        """

        self.min_obs = min_obs
        self.label_encoder = LabelEncoder(min_obs)

    def __repr__(self):
        return ('OneHotEncoder(min_obs={})').format(self.min_obs)

    def _transform_col(self, x, i):
        """Encode one categorical column into sparse matrix with one-hot-encoding.

        Args:
            x (pandas.Series): a categorical column to encode
            i (int): column index

        Returns:
            (scipy.sparse.coo_matrix): sparse matrix encoding a categorical
                                       variable into dummy variables
        """

        labels = self.label_encoder._transform_col(x, i)
        label_max = self.label_encoder.label_maxes[i]

        # build row and column index for non-zero values of a sparse matrix
        index = np.array(range(len(labels)))
        i = index[labels > 0]
        j = labels[labels > 0] - 1  # column index starts from 0

        if len(i) > 0:
            return sparse.coo_matrix((np.ones_like(i), (i, j)),
                                     shape=(x.shape[0], label_max))
        else:
            # if there is no non-zero value, return no matrix
            return None

    def fit(self, X, y=None):
        self.label_encoder.fit(X)

        return self

    def transform(self, X):
        """Encode categorical columns into sparse matrix with one-hot-encoding.

        Args:
            X (pandas.DataFrame): categorical columns to encode

        Returns:
            (scipy.sparse.coo_matrix): sparse matrix encoding categorical
                                       variables into dummy variables
        """

        for i, col in enumerate(X.columns):
            X_col = self._transform_col(X[col], i)
            if X_col is not None:
                if i == 0:
                    X_new = X_col
                else:
                    X_new = sparse.hstack((X_new, X_col))

            logger.debug('{} --> {} features'.format(
                col, self.label_encoder.label_maxes[i])
            )

        return X_new

    def fit_transform(self, X, y=None):
        """Encode categorical columns into sparse matrix with one-hot-encoding.

        Args:
            X (pandas.DataFrame): categorical columns to encode

        Returns:
            sparse matrix encoding categorical variables into dummy variables
        """

        self.label_encoder.fit(X)

        return self.transform(X)


class TargetEncoder(base.BaseEstimator):
    """Target Encoder that encode categorical values into average target values.

    Attributes:
        target_encoders (list of dict): target encoders for columns
    """

    def __init__(self, cv=None):
        """Initialize the TargetEncoder class object.

        Args:
            cv (sklearn.model_selection._BaseKFold, optional): sklearn CV object
        """
        self.cv = cv

    def __repr__(self):
        return('TargetEncoder(cv={})'.format(self.cv))

    def _get_target_encoder(self, x, y):
        """Return a mapping from categories to average target values.

        Args:
            x (pandas.Series): a categorical column to encode.
            y (pandas.Series): the target column

        Returns:
            (dict): mapping from categories to average target values
        """

        assert len(x) == len(y)

        # NaN cannot be used as a key for dict. So replace it with a random
        # integer
        df = pd.DataFrame({y.name: y, x.name: x.fillna(NAN_INT)})
        return df.groupby(x.name)[y.name].mean().to_dict()

    def fit(self, X, y):
        """Encode categorical columns into average target values.

        Args:
            X (pandas.DataFrame): categorical columns to encode
            y (pandas.Series): the target column

        Returns:
            (pandas.DataFrame): encoded columns
        """
        self.target_encoders = [None] * X.shape[1]
        self.target_mean = y.mean()

        for i, col in enumerate(X.columns):
            if self.cv is None:
                self.target_encoders[i] = self._get_target_encoder(X[col], y)
            else:
                self.target_encoders[i] = []
                for i_cv, (i_trn, i_val) in enumerate(self.cv.split(X[col], y), 1):
                    self.target_encoders[i].append(self._get_target_encoder(X.loc[i_trn, col], y[i_trn]))

        return self

    def transform(self, X):
        """Encode categorical columns into average target values.

        Args:
            X (pandas.DataFrame): categorical columns to encode

        Returns:
            (pandas.DataFrame): encoded columns
        """
        for i, col in enumerate(X.columns):
            if self.cv is None:
                X.loc[:, col] = (X[col].fillna(NAN_INT)
                                       .map(self.target_encoders[i])
                                       .fillna(self.target_mean))
            else:
                for i_enc, target_encoder in enumerate(self.target_encoders[i], 1):
                    if i_enc == 1:
                        x = X[col].fillna(NAN_INT).map(target_encoder).fillna(self.target_mean)
                    else:
                        x += X[col].fillna(NAN_INT).map(target_encoder).fillna(self.target_mean)

                X.loc[:, col] = x / i_enc

        return X

    def fit_transform(self, X, y):
        """Encode categorical columns into average target values.

        Args:
            X (pandas.DataFrame): categorical columns to encode
            y (pandas.Series): the target column

        Returns:
            (pandas.DataFrame): encoded columns
        """
        self.target_encoders = [None] * X.shape[1]
        self.target_mean = y.mean()

        for i, col in enumerate(X.columns):
            if self.cv is None:
                self.target_encoders[i] = self._get_target_encoder(X[col], y)

                X.loc[:, col] = (X[col].fillna(NAN_INT)
                                       .map(self.target_encoders[i])
                                       .fillna(self.target_mean))
            else:
                self.target_encoders[i] = []
                for i_cv, (i_trn, i_val) in enumerate(self.cv.split(X[col], y), 1):
                    target_encoder = self._get_target_encoder(X.loc[i_trn, col], y[i_trn])

                    X.loc[i_val, col] = (X.loc[i_val, col].fillna(NAN_INT)
                                                          .map(target_encoder)
                                                          .fillna(y[i_trn].mean()))

                    self.target_encoders[i].append(target_encoder)

        return X


class BandpassFilter(base.BaseEstimator):

    def __init__(self, fs=10., lowcut=.5, highcut=3., order=3):
        self.fs = 10.
        self.lowcut = .5
        self.highcut = 3.
        self.order = 3
        self.b, self.a = self._butter_bandpass()

    def _butter_bandpass(self):
        nyq = .5 * self.fs
        low = self.lowcut / nyq
        high = self.highcut / nyq
        b, a = butter(self.order, [low, high], btype='band')

        return b, a

    def _butter_bandpass_filter(self, x):
        return lfilter(self.b, self.a, x)

    def fit(self, X):
        return self

    def transform(self, X, y=None):
        for col in range(X.shape[1]):
            X[:, col] = self._butter_bandpass_filter(X[:, col])

        return X
