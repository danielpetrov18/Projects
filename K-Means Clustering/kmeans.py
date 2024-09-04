import numpy as np
import pandas as pd

def load_data(path='pokemon.csv', features=['Total', 'HP', 'Attack', 'Defence', 'Sp_attack', 'Sp_defence', 'Speed']):
    df = pd.read_csv(path) # Source: https://www.kaggle.com/datasets/shubhamchambhare/pokemons-and-there-stats 
    df[features] = df[features].fillna(0) # If any of the cells have a missing value it gets replaced by 0
    return df[features].copy()

# Normalization avoids overfitting because all features contribute equally to the model's learning process
def normalize(data, new_min=1, new_max=10): 
    return (data - data.min()) / (data.max() - data.min()) * (new_max - 1) + new_min

class KMeans:
    
    def __init__(self, k=3, n_iters=100, n_features=7): # k is the number of clusters
        self.k = k
        self.n_iters = n_iters
        
        # Each centroid represents the geometric mean of each cluster (central point)
        self.centroids = np.random.uniform(low=1.0, high=10.1, size=(k, n_features)) 
      
    @staticmethod
    def euclidean_distance(p, q):
        return np.sqrt(np.sum((p - q) ** 2))
   
    def predict(self, X): # We pass only X because K-means is a unsupervised algorithm
        self.X = X
        self.samples, self.features = X.shape
        
        # 1. Initialize random centroids
        # 2. Label each point with the closest centroid
        # 3. Compute the geometric mean of the points in each cluster to find the position of the respective centroid
        # 4. Update the centroids
        # 5. Repeat until convergence or max iterations
        

    