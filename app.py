from cleaner import *
from genreRecommend import *
from modelRecommend import *
from deepLearningRecommend import *

import streamlit as st
import sqlite3
from sqlite3 import Error
import time
from csv import writer

#ONE TIME USE COMMAND IN ORDER TO CLEAN THE DATA AND MOVE IT FORM .dat FILES
#word = convertDat()
#print(word)

# Create the sqlite database that serves as the backend for the app
conn = sqlite3.connect('app.sqlite')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movieSaves (user_id varchar(12), Name varChar(100), Movie_Watched varChar(350), Rating int, Genre varChar(100), flag int)")
conn.close()


# I create these 2 dataframes first to avoid an error with ratings later on
users = pd.read_csv('users.csv', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('movies.csv', usecols=['movie_id', 'title', 'genres'])

conn = sqlite3.connect('app.sqlite')
cur = conn.cursor()
query = cur.execute("SELECT user_id, Movie_Watched, Rating FROM movieSaves WHERE flag = 0 ORDER BY user_id ASC")
results = query.fetchall()
print(results)

for user in results:
    movie_id = movies.loc[movies.title == user[1]].movie_id.values[0]
    ts = int(time.time())
    cur.execute('UPDATE movieSaves SET flag = 1 WHERE user_id = ? AND Movie_Watched = ?', (user[0], user[1]))
    with open('ratings.csv', 'a') as csvfile:
        writer_obj = [user[0], movie_id, user[2], ts]
        writer_object = writer(csvfile)
        writer_object.writerow([])
        writer_object.writerow(writer_obj)
        csvfile.close()
    conn.commit()

conn.close()

#Grabbing datasets and putting them into dataframes
ratings = pd.read_csv('ratings.csv', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])
ratings.drop_duplicates(inplace=True)


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
                cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre, flag) VALUES (?, ?, ?, ?, ?, 0)", (user_id, name, movie, rating, genre))
                conn.commit()
            else:
                # If there are no ids in the database, then we create a new id by adding 1 to the last id in the users df
                user_id = str(users.user_id.max() + 1)
                print(user_id)
                cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre, flag) VALUES (?, ?, ?, ?, ?, 0)", (user_id, name, movie, rating, genre))
                conn.commit()
        else:
            # If the user has an id, we use that id and add to the database
            user_id = int(results[0][0])
            # Add the user to the database
            cur.execute("INSERT INTO movieSaves (user_id, Name, Movie_Watched, Rating, Genre, flag) VALUES (?, ?, ?, ?, ?, 0)", (user_id, name, movie, rating, genre))
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
st.subheader('Enter your name:')
fullName = st.text_input('Your Name')
user_id_for_recommendations = 0

#This is the button that will save the data to the database based on whether or not the user has ever accessed the database before
if st.button('See History'):
    if fullName != '':
        conn = sqlite3.connect('app.sqlite')
        cur = conn.cursor()
        # Check if the user has a user_id
        query = cur.execute("SELECT user_id FROM movieSaves WHERE Name= ?", (fullName,))
        results = query.fetchall()
        # If the user doesnt have an id, we are going to ask them to save some movies
        if len(results) == 0:
            st.write("It looks like you haven't got any movies saved yet. Please save some movies!")
        else:
            # If the user has an id, we use that id and add to the database
            user_id_for_recommendations = int(results[0][0])
        conn.close()
    else:
        st.write('Please fill out all the fields')

if user_id_for_recommendations != 0:
    preds = ModelBasedRecommend(ratings)
    already_rated, predictions = recommend_movies(preds, user_id_for_recommendations, movies, ratings, 20)
    st.write("Based on the movies you like, we recommend:")
    st.subheader('Recommendations:')
    st.table(predictions)
else:
    st.write("Make sure to refresh the page before you start searching!")



# Create a second rating df that will be used for the deep learning model
ratingsDeepLearning = pd.read_csv('ratings.csv', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])
ratingsDeepLearning.drop_duplicates(inplace=True)
# Process ratings dataframe for Keras Deep Learning model
ratingsDeepLearning['user_emb_id'] = ratingsDeepLearning['user_id'] - 1
ratingsDeepLearning['movie_emb_id'] = ratingsDeepLearning['movie_id'] - 1
max_userid = ratingsDeepLearning['user_id'].drop_duplicates().max()
max_movieid = ratingsDeepLearning['movie_id'].drop_duplicates().max()

