from flask import Flask, render_template
import pandas as pd 
import numpy as np
import os 
import json

app = Flask(__name__)


def load_movies():
    with open(os.path.join(app.root_path, "data/", "movies.json")) as f:
        return json.load(f)

def load_genres():
    with open(os.path.join(app.root_path, "data/", "list_genres.json")) as f:
        return json.load(f)

def load_neighbors():
    with open(os.path.join(app.root_path, "data/", "neighbors.npy"), "rb") as f:
        return np.load(f)

def load_movies_csv():
    movies = pd.read_csv(os.path.join(app.root_path, "data/datasets/", "movies.csv"), sep = ";", encoding='latin-1')
    movies = movies.drop("Unnamed: 3", axis = 1)
    return movies.values

def load_rating_csv():
    ratings = pd.read_csv(os.path.join(app.root_path, "data/datasets/", "ratings.csv"), sep = ";")
    X = ratings.pivot_table(values='rating',columns='userId',index='movieId').fillna(0).values
    return X

def load_rating_npy():
    with open(os.path.join(app.root_path, "data/", "rating.npy"), "rb") as f:
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

    rating_neighbors = load_rating_npy()
    rating = load_rating_csv()

    rating_average = np.sum(rating[id])/len(rating[id])
    rating_average = '%.2f'%rating_average

    neighbors_rating = rating_neighbors[id][:10]
    rc_rating = []
    for idx, neighbor_rating in enumerate(neighbors_rating):
        neighbor = movies[neighbor_rating]
        neighbor["rating"] = np.sum(rating[neighbor_rating])/len(rating[neighbor_rating])
        neighbor["rating"] = '%.2f'%neighbor["rating"]
        rc_rating.append(neighbor)
    
    genres_neighbors = load_neighbors()
    neighbors_genres = genres_neighbors[id][:10]
    rc_genres = []
    for idx in range(len(neighbors_genres)):
        rc_genres.append(movies[neighbors_genres[idx]])

    return render_template(
        "movies.html", 
        items = movies_render, 
        url = "/", 
        title = movies_render["title"],
        rating = rating_average,
        rc_genres = rc_genres,
        rc_rating = rc_rating
    )