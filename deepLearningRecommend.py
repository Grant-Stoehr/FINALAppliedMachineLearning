# Import libraries
%matplotlib inline
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create training set
shuffled_ratings = ratings.sample(frac=1., random_state=RNG_SEED)

# Shuffling users
Users = shuffled_ratings['user_emb_id'].values
print 'Users:', Users, ', shape =', Users.shape

# Shuffling movies
Movies = shuffled_ratings['movie_emb_id'].values
print 'Movies:', Movies, ', shape =', Movies.shape

# Shuffling ratings
Ratings = shuffled_ratings['rating'].values
print 'Ratings:', Ratings, ', shape =', Ratings.shape