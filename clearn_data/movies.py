import json
import numpy as np 
import pandas as pd 

if __name__ == "__main__":
    movies = pd.read_csv("../datasets/movies.csv", sep = ";", encoding='latin-1')
    movies = movies.drop("Unnamed: 3", axis = 1)

    dataJson = []
    genres = []
    for movie_idx, movie in enumerate(movies.values):
        genres += movie[2].split("|")
        genre_list = []
        for genre in movie[2].split("|"):
            genre_list.append({
                "path": "/genres/" + "_".join(genre.split(" ")),
                "genre":genre
            })
        dataJson.append({
            "id": movie_idx + 1,
            "path": "/movies/" + str(movie_idx),
            "title": movie[1],
            "genres": genre_list
        })
    genres = list(set(genres))
    genres.sort()
    for genre_idx, genre in enumerate(genres):
        subData = {
            "path": "/genres/" + "_".join(genre.split(" ")),
            "genre": genre
        }
        genres[genre_idx] = subData
    with open('movies.json', 'w') as f:
        json.dump(dataJson, f, ensure_ascii=False, indent=4)
    with open("list_genres.json", "w") as f:
        json.dump(genres, f, ensure_ascii=False, indent=4)
    print("[+] Saving complete. File name: {0}.json [+]".format("movies"))
    print("[+] Saving complete. File name: {0}.json [+]".format("list_genres"))