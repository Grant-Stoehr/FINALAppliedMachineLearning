import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

def ModelBasedRecommend (ratings):
    # Gets the number of users, and creates a pivot df of the users and their ratings
    Ratings = ratings.pivot(index = 'user_id', columns ='movie_id', values = 'rating').fillna(0)

    # Denormalizes the ratings
    R = Ratings.apply(lambda x: (x - x.mean()) / x.std())

    R = Ratings.to_numpy()
    user_ratings_mean = np.mean(R, axis = 1)
    Ratings_demeaned = R - user_ratings_mean.reshape(-1, 1)

    # Creates the Support Vector Decompostion (SVD)
    U, sigma, Vt = svds(Ratings_demeaned, k = 50)
    sigma = np.diag(sigma)

    # Begins making predictions
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds = pd.DataFrame(all_user_predicted_ratings, columns = Ratings.columns)
    return preds
    

def recommend_movies(predictions, userID, movies, original_ratings, num_recommendations):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # User ID starts at 1, not 0
    print(predictions)
    print()
    sorted_user_predictions = predictions.iloc[user_row_number].sort_values(ascending=False) # User ID starts at 1
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings[original_ratings.user_id == (userID)]
    user_full = (user_data.merge(movies, how = 'left', left_on = 'movie_id', right_on = 'movie_id').
                     sort_values(['rating'], ascending=False)
                 )

    print ('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print ('Recommending highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies[~movies['movie_id'].isin(user_full['movie_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'movie_id',
               right_on = 'movie_id').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations