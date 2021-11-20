import numpy as np 
import pandas as pd 


class CountVectorizer:


    def __init__(self):
        self.genres = []
        self.contents = []


    def get_genres_string(self, strings):
        strings = strings.split("|")
        list_genres = []
        for string in strings:
            genres = string.split(" ")
            for genre in genres:
                genre = "".join(e for e in genre if e.isalnum())
                if len(genre) >= 2:
                    list_genres.append(genre.lower())
        return list_genres


    def print_progress(self, index, total):
        percent = ("{0:.2f}").format(100 * ((index + 1) / total))
        filledLength = 50 * index // total
        bar = '=' * filledLength + '-' * (50 - filledLength - 1)
        print('\rProgress: |%s| %s%%' % (bar, percent), end = '\r')
        if index == total - 1:
            print()
    
    
    def save_model(self, neighbors, name):
        with open(name + ".npy", "wb") as f:
            np.save(f, neighbors)    
        print("[+] Saving complete. File name: {0}.npy [+]".format(name))
    

    def nearest_neighbors(self):
        movies_contents = self.contents.values
        self.neighbors = movies_contents @ movies_contents.T
        np.fill_diagonal(self.neighbors, -1)
        for neighbor_idx in range(self.neighbors.shape[0]):
            self.print_progress(neighbor_idx, self.neighbors.shape[0])

            self.neighbors[neighbor_idx] = np.argsort(self.neighbors[neighbor_idx])
            self.neighbors[neighbor_idx] = self.neighbors[neighbor_idx][::-1]


    def fit(self, movies):
        for genres in "|".join(movies.genres).split("|"):
            self.genres += self.get_genres_string(genres)

        self.genres = np.unique(self.genres)

        movies.genres = [
            self.get_genres_string(k) for k in movies.genres
        ]

        len_movies = movies.shape[0]
        len_genres = self.genres.shape[0]
        self.contents = pd.DataFrame(np.zeros((len_movies, len_genres)), columns = self.genres)

        for genre_idx, genre in enumerate(self.genres):
            self.print_progress(genre_idx, len_genres)

            self.contents[genre] = np.array([
                1 if genre in movies.genres[idx] else 0 for idx in range(len_movies)
            ])
        self.nearest_neighbors()
        self.save_model(self.neighbors, "neighbors")


if __name__ == "__main__":
    movies = pd.read_csv("../datasets/movies.csv", sep = ";", encoding='latin-1')
    movies = movies.drop("Unnamed: 3", axis = 1)
    cvt = CountVectorizer()
    cvt.fit(movies)