import pandas as pd
import numpy as np
import json


class Helper:


    def print_progress(self, index, total):
        percent = ("{0:.2f}").format(100 * ((index + 1) / total))
        filledLength = 50 * index // total
        bar = '=' * filledLength + '-' * (50 - filledLength - 1)
        print('\rProgress: |%s| %s%%' % (bar, percent), end='\r')
        if index == total - 1:
            print()


    def save_model(self, data, name):
        with open(name, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("[+] Saving complete. File name: {0}".format(name))


    def save_model_npy(self, data, name):
        with open(name, "wb") as f:
            np.save(f, data)
        print("[+] Saving complete. File name: {0}".format(name))


class MoviesNearestNeighbors(Helper):


    def __init__(self):
        self.genres = []
        self.movies = []
        Helper.__init__(self)


    def parse_genre(self, genre):
        genre = genre.split("|")
        genres = []
        for strings in genre:
            strings = strings.split(" ")
            for string in strings:
                string = "".join(e for e in string if e.isalnum())
                if len(string) >= 2:genres.append(string)
        return genres


    def nearest_neighbors(self):
        movies = self.movies.values

        neighbors = movies @ movies.T
        np.fill_diagonal(neighbors, -1)
        for neighbor_idx, neighbor in enumerate(neighbors):
            self.print_progress(neighbor_idx, len(neighbors))

            neighbor = np.argsort(neighbor)
            neighbors[neighbor_idx] = neighbor[::-1]

        return neighbors


    def run(self, movies):
        for genre in "|".join(movies.genres).split("|"):
            self.genres += self.parse_genre(genre)

        self.genres = np.unique(self.genres)

        movies.genres = [
            self.parse_genre(genre) for genre in movies.genres
        ]

        self.movies = pd.DataFrame(columns=self.genres)

        for genre_idx, genre in enumerate(self.genres):
            self.print_progress(genre_idx, len(self.genres))

            self.movies[genre] = np.array([
                1 if genre in movies.genres[idx] else 0 for idx in range(len(movies))
            ])

        neighbors = self.nearest_neighbors()
        self.save_model_npy(neighbors, "genres_neighbors.npy")


class MoviesPreprocess(Helper):


    def __init__(self):
        self.movies = []
        self.genres = []
        Helper.__init__(self)


    def run(self, movies, rating_average):
        movies = movies.values[:3706]

        genres_key = []
        genres_value = []

        for movie_idx, movie in enumerate(movies):
            self.print_progress(movie_idx, len(movies))

            genres_json = []
            for genre in movie[2].split("|"):
                genres_json.append({
                    "path": "/genres/" + "_".join(genre.split(" ")),
                    "value": genre
                })
                if genre not in genres_key:
                    genres_key.append(genre)
                    genres_value.append(genres_json[-1])

            self.movies.append({
                "id": movie_idx + 1,
                "path": "/movies/" + str(movie_idx),
                "title": movie[1],
                "rating": rating_average[movie_idx],
                "genres": genres_json
            })

        genres_key = np.argsort(genres_key)
        self.genres = [
            genres_value[idx] for idx in genres_key
        ]
        self.save_model(self.movies, "movies_contents.json")
        self.save_model(self.genres, "genres_contents.json")


class RatingNearestNeighbors(Helper):


    def __init__(self):
        Helper.__init__(self)
        self.rating = []


    def get_average(self, row):
        rating_count = len(np.where(row > 0)[0])
        if rating_count == 0:
            rating_count += 1
        return np.sum(row)/rating_count


    def nearest_neighbors(self):
        neighbors = []
        for idx, rating in enumerate(self.rating):
            self.print_progress(idx, len(self.rating))
            neighbors.append(np.argsort(rating))

        return np.array(neighbors)


    def run(self, rating):
        rating_average = np.array([
            self.get_average(row) for row in rating
        ])

        self.rating_average = rating_average.copy()

        for idx, average in enumerate(rating_average):
            self.print_progress(idx, len(rating_average))

            self.rating.append(abs(rating_average - average))

        self.rating = np.array(self.rating)
        np.fill_diagonal(self.rating, 5.1)

        neighbors = self.nearest_neighbors()
        self.save_model_npy(neighbors, "rating_neighbors.npy")


if __name__ == "__main__":
    movies = pd.read_csv("../datasets/movies.csv", sep=";", encoding='latin-1')
    movies = movies.drop("Unnamed: 3", axis=1)

    rating = pd.read_csv("../datasets/ratings.csv", sep=";")
    rating = rating.pivot_table(values='rating', columns='userId', index='movieId').fillna(0).values

    mvn = MoviesNearestNeighbors()
    mvn.run(movies.copy())

    rnn = RatingNearestNeighbors()
    rnn.run(rating.copy())

    mp = MoviesPreprocess()
    mp.run(movies.copy(), rnn.rating_average)


