"""Utilities for input validation."""


import numpy as np
import pandas as pd

from pandas.api.types import is_categorical_dtype, is_numeric_dtype


__all__ = [
    "check_uniq",
    "check_column_existence",
    "check_is_dataframe",
    "is_numeric",
    "find_sparsity",
    "check_continuity"
]


def check_uniq(X):
    """Checks whether all input data values are unique.

    Parameters
    ----------
    X: array-like, shape = (n_samples, )
        Vector to check whether it cointains unique values.

    Returns
    -------
    boolean: Whether all input data values are unique.

    """
    s = set()
    return not any(x in s or s.add(x) for x in X)


def check_column_existence(X, columns):
    """Checks whether all listed columns are in a given DataFrame.

    Parameters
    ----------
    X: pandas.DataFrame
        Data with columns to be checked for occurrence.

    columns: single label or list-like
        Columns' labels to check.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If one of the elements of `cols` is not found in the `X` columns.

    """
    if isinstance(columns, str):
        columns = [columns]

    exist = all(col in X.columns for col in columns)

    if not exist:
        cols_error = list(set(columns) - set(X.columns))
        raise ValueError(
            "Columns not found in the DataFrame: {}"
            .format(", ".join(cols_error))
        )


def check_is_dataframe(X):
    """Checks whether object is a pandas.DataFrame.

    Parameters
    ----------
    X: object
        Object suspected of being a pandas.DataFrame.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If object is not a pandas.DataFrame.

    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("Input must be an instance of pandas.DataFrame.")


def is_numeric(X, project=True):
    """Checks whether given vector contains numeric-only values excluding
    boolean vectors.

    Parameters
    ----------
    X: array-like, shape = (n_samples, )
        Vector where n_samples is the number of samples.

    project: bool, optional (default=True)
        If True tries to project on a numeric type unless categorical dtype is
        passed.

    Returns
    -------
    bool

    """
    if project and not is_categorical_dtype(X):
        try:
            X = np.array(X).astype(np.number)
        except ValueError:
            return False

    return is_numeric_dtype(X) and not set(X) <= {0, 1}


def find_sparsity(X, thresh=.01):
    """Finds columns with highly sparse categories.

    For categorical and binary features finds columns where categories with
    relative frequencies under the threshold are present.

    For numerical features (excluding binary variables) returns columns
    where NaNs or 0 are dominating in the given dataset.

    Parameters
    ----------
    X: pandas.DataFrame
        Data to be checked for sparsity.

    thresh: float, optional (default=.01)
        Fraction of one of the categories under which the sparseness will be
        reported.

    Returns
    -------
    sparse_{num, bin, cat}: list
        List of {numerical, binary, categorical} X column names where high
        sparsity was detected.

    """
    assert isinstance(X, pd.DataFrame), \
        'Input must be an instance of pandas.DataFrame()'
    assert len(X) > 0, 'Input data can not be empty!'

    sparse_num, sparse_bin, sparse_cat = [[] for _ in range(3)]

    for col in X.columns:
        tab_counter = X[col].value_counts(normalize=True, dropna=False)
        if is_numeric(X[col]):
            most_freq = tab_counter.index[0]
            if most_freq != most_freq or most_freq == 0:
                sparse_num.append(col)
        else:
            min_frac = tab_counter.iloc[-1]
            if min_frac < thresh:
                if set(X[col]) <= {0, 1}:
                    sparse_bin.append(col)
                else:
                    sparse_cat.append(col)

    return sparse_num, sparse_bin, sparse_cat


def check_continuity(X, thresh=.5):
    """Checks whether input variable is continuous.

    Parameters
    ----------
    X: array-like, shape = (n_samples, )
        Vector to check for continuity.

    thresh: float, optional (default=.5)
        Fraction of non-unique values under which lack of continuity will be
        reported.

    Returns
    -------
    boolean: Whether variable is continuous.

    """
    return is_numeric(X) and len(np.unique(X)) / len(X) >= 1 - thresh
