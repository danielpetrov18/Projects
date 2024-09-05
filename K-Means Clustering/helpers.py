import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Normalization avoids overfitting because all features contribute equally to the model's learning process
def _normalize(X, new_min=1, new_max=10): 
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0)) * (new_max - 1) + new_min

def load_data(filepath='pokemon.csv', features=['Total', 'HP', 'Attack', 'Defence', 'Sp_attack', 'Sp_defence', 'Speed']):    
    df = pd.read_csv(filepath)                          
    df[features] = df[features].fillna(0)          # If any of the cells have a missing value it gets replaced by 0
    starting_data = df[features].copy().to_numpy() # Get the data in the form of numpy array
    return _normalize(starting_data)   

# Makes use of the 'Forgy method' where k observations from the dataset are chosen at random
def generate_centroids(X, k):
    random_indices = np.random.choice(X.shape[0], size=k, replace=False) # Randomly select k unique indices from the data points
    centroids = X[random_indices, :] 
    return centroids

def _euclidean_distance(X, centroids):  # It computes the euclidean distance for all the points and centroids at once
    n_samples = X.shape[0]
    n_centroids = centroids.shape[0]
    distances = np.zeros((n_samples, n_centroids)) # Each row represents the distance between a point and all centroids
    for n_centroid in range(n_centroids):
        distances[:, n_centroid] = np.sqrt(np.sum((X - centroids[n_centroid, :]) ** 2, axis=1))
    return distances

def get_labels(X, centroids): # Returns the indices of the closets centroid for each point
    distances = _euclidean_distance(X, centroids)
    return np.argmin(distances, axis=1) # Along axis 1 because each column represents the distance to a separate centroid

def plot_with_pca(k, labels, centroids, X):
    pca = PCA(n_components=2)   # Apply PCA to reduce data to 2D
    X_pca = pca.fit_transform(X)
    centroids_pca = pca.transform(centroids)
    
    colors = plt.cm.get_cmap('tab10', k)  # Choose a colormap with `k` distinct colors
    
    plt.figure(figsize=(8, 6))
    
    for cluster in range(k):
        points = X_pca[labels == cluster]
        plt.scatter(points[:, 0], points[:, 1], s=50, c=[colors(cluster)], label=f"Cluster {cluster+1}", alpha=0.6)
    
    # Plot centroids with a different marker and larger size
    plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], s=200, c='black', marker='*', edgecolors='white', label='Centroids')

    plt.title(f'K-Means Clustering with {k} Clusters (PCA Projection)')
    plt.legend()
    plt.grid(True)
    plt.show()
