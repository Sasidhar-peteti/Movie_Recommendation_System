# This script implements a Movie Recommendation System using a GUI built with tkinter. It utilizes pandas for data handling,
# sklearn for text vectorization and similarity computation, and PIL for image handling. The dataset ('Movies_dataset.csv') is 
# preprocessed to combine movie overviews and genres into tags for recommendation. Users can search movies by title or genre, 
# receiving recommendations or genre-specific movie lists. The GUI includes options for input via dropdown menu, entry widgets 
# for user input, and a search button triggering recommendation functions. Output is displayed in a formatted label below the 
# search button, with results formatted for readability. The background image ('background.jpg') is loaded and resized to fit 
# the window. Overall, the script integrates data preprocessing, machine learning for recommendation, and a user-friendly 
# interface for interactive movie searches and recommendations.

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Load data
movies = pd.read_csv('Movies_dataset.csv')

# Preprocess data
movies = movies[['id', 'title', 'overview', 'genre']]
movies['tags'] = movies['overview'] + ' ' + movies['genre']
new_data = movies.drop(columns=['overview', 'genre'])

# Initialize CountVectorizer
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
similarity = cosine_similarity(vector)

# Function to recommend movies
def recommend(movie_title):
    movie_title_lower = movie_title.lower()
    new_data['title_lower'] = new_data['title'].apply(lambda x: x.lower())
    index = new_data[new_data['title_lower'] == movie_title_lower].index
    if len(index) > 0:
        index = index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommendations = [new_data.iloc[i[0]].title for i in distance[1:6]]
        return recommendations
    else:
        return []

# Function to search by genre
def search_by_genre(genre):
    filtered_movies = new_data.dropna(subset=['tags'])
    filtered_movies = filtered_movies[filtered_movies['tags'].str.contains(genre, case=False)]
    if not filtered_movies.empty:
        filtered_movies_shuffled = filtered_movies.sample(frac=1).reset_index(drop=True)  # Shuffle without a fixed seed
        return filtered_movies_shuffled['title'].head(5).tolist()
    else:
        return []

# Create main window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("800x600")

# Load background image from local file and resize it to fit the window
background_image = Image.open("background.jpg")
background_image = background_image.resize((800, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas and set the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Function to handle the search
def on_search():
    search_option = search_var.get()
    if search_option == 'Title':
        movie_title = title_entry.get()
        if movie_title:
            recommendations = recommend(movie_title)
            if recommendations:
                recommendations_text = "Recommendations for You:\n" + "\n".join(recommendations)
                output_text.set(recommendations_text)
            else:
                output_text.set("Movie not found in the dataset.")
        else:
            messagebox.showwarning("Input Error", "Please enter a movie title.")
    elif search_option == 'Genre':
        genre = genre_entry.get()
        if genre:
            genre_movies = search_by_genre(genre.lower())
            if genre_movies:
                recommendations_text = "Recommendations for You:\n" + "\n".join(genre_movies)
                output_text.set(recommendations_text)
            else:
                output_text.set("No movies found in the selected genre.")
        else:
            messagebox.showwarning("Input Error", "Please enter a genre.")

# Create dropdown menu
search_var = tk.StringVar(root)
search_var.set("Title")

canvas.create_text(400, 120, text="Select search option:", fill="white", font=("Helvetica", 14, "bold"))
option_menu = tk.OptionMenu(root, search_var, "Title", "Genre")
option_menu_window = canvas.create_window(400, 160, window=option_menu)
option_menu.configure(font=("Helvetica", 12), bg="#e6e6e6", fg="#333333", activebackground="#d9d9d9")

# Entry widgets for user input
title_label = tk.Label(root, text="Enter Movie Title:", bg="#f0f0f0", font=("Helvetica", 12))
title_entry = tk.Entry(root, width=30, font=("Helvetica", 12))

genre_label = tk.Label(root, text="Enter Genre:", bg="#f0f0f0", font=("Helvetica", 12))
genre_entry = tk.Entry(root, width=30, font=("Helvetica", 12))

output_text = tk.StringVar()

# Function to update entry widgets based on search option
def update_entry_widgets(*args):
    if search_var.get() == "Title":
        title_label.place(x=150, y=180)
        title_entry.place(x=300, y=180)
        genre_label.place_forget()
        genre_entry.place_forget()
    else:
        genre_label.place(x=150, y=180)
        genre_entry.place(x=300, y=180)
        title_label.place_forget()
        title_entry.place_forget()

# Trace changes in dropdown menu selection
search_var.trace("w", update_entry_widgets)

# Create search button
search_button = tk.Button(root, text="Search", command=on_search, font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049")
canvas.create_window(400, 250, window=search_button)

# Create output label below the search button
output_label = tk.Label(root, textvariable=output_text, bg="#f0f0f0", font=("Helvetica", 12), wraplength=700, justify="left")
canvas.create_window(400, 350, window=output_label)

# Function to update the output text format
def format_output_text(output):
    return output.replace("Recommendations for You:", "Recommendations for You:\n------------------------------")

# Override the set method of StringVar to format the output text
original_set = output_text.set
def new_set(value):
    original_set(format_output_text(value))
output_text.set = new_set

# Initialize entry widgets visibility
update_entry_widgets()

# Run the GUI event loop
root.mainloop()
