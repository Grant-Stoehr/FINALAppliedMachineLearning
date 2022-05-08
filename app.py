from cleaner import *
from genreRecommend import *

import streamlit as st

#ONE TIME USE COMMAND IN ORDER TO CLEAN THE DATA AND MOVE IT FORM .dat FILES
#word = convertDat()
#print(word)

#Grabbing datasets and putting them into dataframes
ratings = pd.read_csv('ratings.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])
users = pd.read_csv('users.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('/Users/grantstoehr/Desktop/ml-latest-small/movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])


# #in dataframe, add the ability for a user to check whether they have watched a movie or not that will remove 
# #the movie from their Content Based Recommendations
# your_movie = ""

# st.header('Genre-Based Recommendation System')
# your_movie = st.text_input("Enter your favorite movie:")
# #DO AN ADVANCED FILTER THAT LETS EVERYTHING ELSE POP OUT
# year_start = st.text_input("Enter the first year you would like us to search through:")
# year_end = st.text_input("Enter the last year you would like us to search through:")
# num_Results = st.text_input("Enter the number of results you would like us to return:")
# if num_Results != "":
#     num_Results = int(num_Results)
# else:
#     num_Results = 0

# RecommendedMovies = ContentBasedRecommend(your_movie, movies)
# RecommendedWithYear = []

# if year_start != '' and year_end != '':
#     for movie in RecommendedMovies:
#         year_char = movie[-5:-1]
#         if int(year_char) >= int(year_start) and int(year_char) <= int(year_end):
#             RecommendedWithYear.append(movie)
#     st.table(RecommendedWithYear)
# elif year_start != '' and year_end == '':
#     for movie in RecommendedMovies:
#         year_char = movie[-5:-1]
#         if int(year_char) >= int(year_start):
#             RecommendedWithYear.append(movie)
#     st.table(RecommendedWithYear)
# elif year_start == '' and year_end != '':
#     for movie in RecommendedMovies:
#         year_char = movie[-5:-1]
#         if int(year_char) <= int(year_end):
#             RecommendedWithYear.append(movie)
#     st.table(RecommendedWithYear)
# else:
#     if num_Results > len(RecommendedMovies):
#         st.write('Sorry, we only have ' + str(len(RecommendedMovies)) + ' results to show you.')
#         st.table(RecommendedMovies)
#     elif num_Results == 0:
#         st.table(RecommendedMovies.head(5))
#     else:
#         RecommendedMovies = RecommendedMovies.head(num_Results)
#         st.table(RecommendedMovies)
    
