from flask import Flask, render_template
import pandas as pd 
import numpy as np
import os 
import json

app = Flask(__name__)


def load_movies():
    with open(os.path.join(app.root_path, "data/", "movies_contents.json")) as f:
        return json.load(f)

def load_genres():
    with open(os.path.join(app.root_path, "data/", "genres_contents.json")) as f:
        return json.load(f)

def load_movies_csv():
    movies = pd.read_csv(os.path.join(app.root_path, "data/datasets/", "movies.csv"), sep = ";", encoding='latin-1')
    movies = movies.drop("Unnamed: 3", axis = 1)
    return movies.values[:3706]

def load_neighbors():
    with open(os.path.join(app.root_path, "data/", "genres_neighbors.npy"), "rb") as f:
        return np.load(f)

def load_rating_csv():
    ratings = pd.read_csv(os.path.join(app.root_path, "data/datasets/", "ratings.csv"), sep = ";")
    X = ratings.pivot_table(values='rating',columns='userId',index='movieId').fillna(0).values
    return X

def load_rating_npy():
    with open(os.path.join(app.root_path, "data/", "rating_neighbors.npy"), "rb") as f:
        return np.load(f)

@app.route("/")
def HOME():
    movies = load_movies()
    genres = load_genres()
    return render_template("index.html", items=movies, genres=genres)

@app.route("/genres/<string:genre>")
def GENRES(genre):
    movies = load_movies()
    genre = " ".join(genre.split("_"))
    movies_csv = load_movies_csv()
    movies_render = []
    for movie_idx, movie in enumerate(movies_csv):
        if genre in movie[2]:
            movies_render.append(movies[movie_idx])
    return render_template("genres.html", items=movies_render, url="/")

@app.route("/movies/<int:id>")
def MOVIES(id):
    movies = load_movies()
    movies_render = movies[id]
    movies_render["rating"] = "%.2f"%movies_render["rating"]

    neighbors_rating = load_rating_npy()[id][:10]
    rc_rating = []
    for neighbor in neighbors_rating:
        rc_rating.append(movies[neighbor])
        rc_rating[-1]["rating"] = "%.2f"%rc_rating[-1]["rating"]
    
    
    neighbors_genres = load_neighbors()[id][:10]
    rc_genres = []
    for neighbor in neighbors_genres:
        rc_genres.append(movies[neighbor])
        rc_genres[-1]["rating"] = "%.2f"%rc_genres[-1]["rating"]

    return render_template(
        "movies.html", 
        items = movies_render, 
        url = "/", 
        title = movies_render["title"],
        rc_genres = rc_genres,
        rc_rating = rc_rating
    )