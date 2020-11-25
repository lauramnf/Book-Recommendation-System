import os
from os import name
import pandas as pd #data processing

def clear():
#Function to clear the terminal screen
    # for windows
    if name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def validate_book_rating():
#Function that validades rating data according to the number of users that rated the book

    rates_per_book = books_rating['ISBN'].value_counts()  #Count how many rates a book had. 'ISBN' as the identifier.
    valid_ratings = rates_per_book[rates_per_book >= 15].index  #Separate data. Only books with 15 or more rates are considered
    valid_rates = books_rating[books_rating['ISBN'].isin(valid_ratings)] #Clear rating file data set. Only valid data remains
    valid_books = books[books['ISBN'].isin(valid_ratings)]  #Clear rating file data set. Only valid data remains
    return valid_rates, valid_books


#Reading the 3 file data
books = pd.read_csv('BX-Books.csv', sep = ';', error_bad_lines = False, encoding = "latin-1")
users = pd.read_csv('BX-Users.csv', sep = ';', error_bad_lines = False, encoding = "latin-1")
books_rating = pd.read_csv('BX-Book-Ratings.csv', sep = ';', error_bad_lines = False, encoding = "latin-1")

valid_rates, valid_books = validate_book_rating()

valid_rates = (valid_rates).groupby(valid_rates['ISBN']).mean() #Group valid data by its indentifier and get rating's mean for each book
named_rates = valid_rates.merge(valid_books, on = 'ISBN') #Join books infos and rating infos

clear() #Clear the screen

authors = ['Stephen King', 'Nora Roberts','Danielle Steel','Mary Higgins Clark','Dean R. Koontz','Robert Asprin','Mildred D. Taylor']
print('Now it\'s time for you to choose your favorite author. Here are some examples:')
for author in authors: print(author)
print('and much more...')
author = input('Which one is your favorite? ') #Get users data

named_rates = named_rates.loc[named_rates['Book-Author'].str.contains(author)] #Filter rating data according to users preferences
sorted_books = named_rates.sort_values(by="Book-Rating", ascending=False) #Sort data

#erase unimportant columns
sorted_books = sorted_books.drop(columns=['Image-URL-M', 'Image-URL-L', 'ISBN', 'Image-URL-S','User-ID'])

print('Hey! Your TOP 5 recommended books are:')
print(sorted_books.head())
