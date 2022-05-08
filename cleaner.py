import pandas as pd
import csv

def cleanDF(df):
    df = df.apply(lambda row: make_year(row), axis=1)
    return df

def make_year(row):
    row['Year_Created'] = row['title'][-5:-1]
    return row


def convertDat():
    with open('movies.dat', encoding='iso-8859-1') as dat_file, open('movies.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(dat_file)

        movie_arr = [['movie_id','title','genre']]

        for line in dat_file:
            row = [field.strip() for field in line.split('::')]
            movie_arr.append(row)
        
        #move the movie_arr into a the movies.csv file
        csv_writer.writerows(movie_arr)

    with open('users.dat', encoding='iso-8859-1') as dat_file, open('users.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(dat_file)
        # Specify User's Age and Occupation Column
        AGES = { 1: "Under 18", 18: "18-24", 25: "25-34", 35: "35-44", 45: "45-49", 50: "50-55", 56: "56+" }
        OCCUPATIONS = { 0: "other or not specified", 1: "academic/educator", 2: "artist", 3: "clerical/admin",
                        4: "college/grad student", 5: "customer service", 6: "doctor/health care",
                        7: "executive/managerial", 8: "farmer", 9: "homemaker", 10: "K-12 student", 11: "lawyer",
                        12: "programmer", 13: "retired", 14: "sales/marketing", 15: "scientist", 16: "self-employed",
                        17: "technician/engineer", 18: "tradesman/craftsman", 19: "unemployed", 20: "writer" }

        user_arr = [['user_id','gender','age_desc','occ_desc','zipcode']]

        for line in dat_file:
            row = [field.strip() for field in line.split('::')]
            user_arr.append(row)

        count = 0
        for row in user_arr:
            if count != 0:
                #Convert the age to a the correspoding age in the AGES dictionary
                if row[2] != '':
                    row[2] = AGES[int(row[2])]
                #Convert the occupation to a the correspoding occupation in the OCCUPATIONS dictionary
                if row[3] != '':
                    row[3] = OCCUPATIONS[int(row[3])]
            count += 1

        #move the user_arr into a the users.csv file
        csv_writer.writerows(user_arr)

    with open('ratings.dat', encoding='iso-8859-1') as dat_file, open('ratings.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(dat_file)

        rating_arr = [['user_id','movie_id','rating']]

        for line in dat_file:
            row = [field.strip() for field in line.split('::')]
            rating_arr.append(row)
        
        #move the rating_arr into a the rating.csv file
        csv_writer.writerows(rating_arr)

    return "Hello World"