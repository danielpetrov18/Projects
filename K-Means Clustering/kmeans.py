import numpy as np
from helpers import get_labels, generate_centroids, plot_with_pca

class KMeansClustering:
    
    def __init__(self, k=3, n_iters=100): 
        self.k = k  # k is the number of clusters/centroids
        self.n_iters = n_iters
      
    def fit(self, X): # We pass only X because K-means is an unsupervised algorithm
        self.X = X
        self.labels = np.zeros(self.X.shape[0])
        self.centroids = generate_centroids(self.X, self.k) 
        
        iterations = 0
        old_centroids = np.zeros_like(self.centroids)
        while iterations <= self.n_iters and not np.array_equal(old_centroids, self.centroids):
            old_centroids = self.centroids.copy()  # Save the state of the centroids before we update them
            self.labels = get_labels(self.X, self.centroids)  # Assign each point to the nearest centroid
            
            # Update each centroid to be the mean of the points assigned to it
            for i in range(self.k):
                points_assigned_to_centroid = self.X[self.labels == i]
                if points_assigned_to_centroid.shape[0] > 0:
                    # Compute the new centroid as the mean of the assigned points
                    self.centroids[i] = points_assigned_to_centroid.mean(axis=0)
                          
            iterations += 1
        
        plot_with_pca(self.k, self.labels, self.centroids, self.X)
        
        return self.labels