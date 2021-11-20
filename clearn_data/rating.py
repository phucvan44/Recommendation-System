import numpy as np 
import pandas as pd 


def save_model(D, name):
    with open(name + ".npy", "wb") as f:
        np.save(f, D)
    print("[+] Saving complete. File name: {0}.npy [+]".format(name))
    

def print_progress(index, total):
    percent = ("{0:.2f}").format(100 * ((index + 1) / total))
    filledLength = 50 * index // total
    bar = '=' * filledLength + '-' * (50 - filledLength - 1)
    print('\rProgress: |%s| %s%%' % (bar, percent), end = '\r')
    if index == total - 1:
        print()


def average_rating(rating):
    list_average = np.mean(rating, axis = 1)
    rating_average = []
    for idx, average in enumerate(list_average):
        print_progress(idx, len(list_average))
        rating_average.append(abs(list_average - average))
    rating_average = np.array(rating_average)
    np.fill_diagonal(rating_average, 5.1)
    rating_neighbors = []
    for idx, neighbor in enumerate(rating_average):
        print_progress(idx, len(rating_average))
        rating_neighbors.append(np.argsort(rating_average[idx]))
    rating_neighbors = np.array(rating_neighbors)
    return rating_neighbors


if __name__ == "__main__":
    ratings = pd.read_csv("../datasets/ratings.csv", sep = ";")
    X = ratings.pivot_table(values='rating',columns='userId',index='movieId').fillna(0).values
    rating_neighbors = average_rating(X)
    save_model(rating_neighbors, "rating")