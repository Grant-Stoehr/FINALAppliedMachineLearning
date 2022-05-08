from cleaner import *
from genreRecommend import *
from modelRecommend import *

import streamlit as st
import sqlite3
from sqlite3 import Error
import time

#ONE TIME USE COMMAND IN ORDER TO CLEAN THE DATA AND MOVE IT FORM .dat FILES
#word = convertDat()
#print(word)

#Grabbing datasets and putting them into dataframes
ratings = pd.read_csv('ratings.csv', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])
users = pd.read_csv('users.csv', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('movies.csv', usecols=['movie_id', 'title', 'genres'])

conn = sqlite3.connect('app.sqlite')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movieSaves (user_id varchar(12), Name varChar(100), Movie_Watched varChar(350), Rating int, Genre varChar(100))")
conn.close()


# GO AHEAD AND ADD THIS TO WHENEVER THE BUTTON IS CLICKED TO SEARCH FOR A MOVIE BASED ON MODELRECOMMENDATION -------------
conn = sqlite3.connect('app.sqlite')
cur = conn.cursor()
query = cur.execute("SELECT user_id, Movie_Watched, Rating FROM movieSaves ORDER BY user_id ASC")
results = query.fetchall()
print(results)
conn.close()

rating_append = pd.DataFrame(columns=['user_id', 'movie_id', 'rating', 'timestamp'])
for user in results:
    movie_id = movies.loc[movies.title == user[1], 'movie_id']
    ts = int(time.time())
    rating_append = rating_append.append({'user_id': user[0], 'movie_id': movie_id, 'rating': user[2], 'timestamp': ts}, ignore_index=True)
ratings = ratings.append(rating_append, ignore_index=True)
conn.close()
# END OF ADDITION -------------------------------------------------------------------------------------------------------

#Create a text area
st.subheader('Tell us about the moves you have watched!')
name = st.text_input('Name')
movie = st.text_input("Movie (FORMAT: 'Movie Name (Year Released)')")
rating = st.text_input('Rating (Make sure to input as an int)')
genre = st.text_input('Genre (FORMAT: "Genre1|Genre2|Genre3")')

#This is the button that will save the data to the database based on whether or not the user has ever accessed the database before
if st.button('Submit'):
    if movie != '' and name != '' and rating != '' and genre != '':
        conn = sqlite3.connect('app.sqlite')
        cur = conn.cursor()
        # Check if the user has a user_id
        query = cur.execute("SELECT user_id FROM movieSaves WHERE Name= ?", (name,))
        results = query.fetchall()
        # If the user doesnt have an id, we are going to make them one
        if len(results) == 0:
            #check to see what the last id is in the table
            query_last_id = cur.execute("SELECT user_id FROM movieSaves ORDER BY user_id DESC LIMIT 1")
            results = query_last_id.fetchall()
            if (results != []):
                # If there are ids in the database, then we create a new id by adding 1 to the last id in the database
                user_id = int(results[0][0]) + 1
                cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre) VALUES (?, ?, ?, ?, ?)", (user_id, name, movie, rating, genre))
                conn.commit()
            else:
                # If there are no ids in the database, then we create a new id by adding 1 to the last id in the users df
                user_id = str(users.user_id.max() + 1)
                cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre) VALUES (?, ?, ?, ?, ?)", (user_id, name, movie, rating, genre))
                conn.commit()
        else:
            # If the user has an id, we use that id and add to the database
            user_id = int(results[0][0])
            # Add the user to the database
            cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre) VALUES (?, ?, ?, ?, ?)", (user_id, name, movie, rating, genre))
            conn.commit()
        conn.close()
    else:
        st.write('Please fill out all the fields')
    

st.subheader('YOUR MOVIES:')
dat = sqlite3.connect('app.sqlite')
query = dat.execute("SELECT Name, Movie_Watched, Rating, Genre From movieSaves WHERE Name = ?", (name,))
cols = [column[0] for column in query.description]
results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
st.table(results)
dat.close()


#in dataframe, add the ability for a user to check whether they have watched a movie or not that will remove 
#the movie from their Content Based Recommendations
your_movie = ""

st.header('Genre-Based Recommendation System')
your_movie = st.text_input("Enter your favorite movie (FORMAT: 'Movie Name (Year Released)'):")
#DO AN ADVANCED FILTER THAT LETS EVERYTHING ELSE POP OUT
year_start = st.text_input("Enter the first year you would like us to search through:")
year_end = st.text_input("Enter the last year you would like us to search through:")
num_Results = st.text_input("Enter the number of results you would like us to return:")
if num_Results != "":
    num_Results = int(num_Results)
else:
    num_Results = 0

genreRecommendedMovies = ContentBasedRecommend(your_movie, movies)
genreRecommendedWithYear = []

if year_start != '' and year_end != '':
    for movie in genreRecommendedMovies:
        year_char = movie[-5:-1]
        if int(year_char) >= int(year_start) and int(year_char) <= int(year_end):
            genreRecommendedWithYear.append(movie)
    st.table(genreRecommendedWithYear)
elif year_start != '' and year_end == '':
    for movie in genreRecommendedMovies:
        year_char = movie[-5:-1]
        if int(year_char) >= int(year_start):
            genreRecommendedWithYear.append(movie)
    st.table(genreRecommendedWithYear)
elif year_start == '' and year_end != '':
    for movie in genreRecommendedMovies:
        year_char = movie[-5:-1]
        if int(year_char) <= int(year_end):
            genreRecommendedWithYear.append(movie)
    st.table(genreRecommendedWithYear)
else:
    if num_Results > len(genreRecommendedMovies):
        st.write('Sorry, we only have ' + str(len(genreRecommendedMovies)) + ' results to show you.')
        st.table(genreRecommendedMovies)
    elif num_Results == 0:
        try:
            st.table(genreRecommendedMovies.head(5))
        except:
            print("No movie is currently being searched for.")
    else:
        RecommendedMovies = genreRecommendedMovies.head(num_Results)
        st.table(RecommendedMovies)
    


st.header('Would you like to see recommendations based on your movie viewing history?')

# preds = ModelBasedRecommend(ratings)
# already_rated, predictions = recommend_movies(preds, 1310, movies, ratings, 20)