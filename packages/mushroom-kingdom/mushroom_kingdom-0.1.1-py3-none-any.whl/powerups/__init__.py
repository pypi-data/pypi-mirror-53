"""
powerups is a collection of data science helper functions
"""

import pandas as pd
import numpy as np

# Sample
ONES = pd.DataFrame(np.ones(10))


# The below function was written to handle seeding of randomized set creation.
# You should not rely on set splitting that doesn't randomize the sets.

def THREE_PIECE_MEAL(df, train_percent=.6, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.ix[perm[:train_end]]
    validate = df.ix[perm[train_end:validate_end]]
    test = df.ix[perm[validate_end:]]
    return train, validate, test
