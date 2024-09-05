from helpers import load_data
from kmeans import KMeansClustering

k = 3
n_iters = 100

try:
    pokemons = load_data()
    kmeans = KMeansClustering(k, n_iters)
    kmeans.fit(pokemons)
except Exception as e:
    print(f'Error running K-Means Clustering: {e}')
    exit(1)
    