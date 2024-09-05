# K-Means Clustering on Pokémon Stats Dataset

This project implements K-Means clustering using a dataset of Pokémon stats. The dataset consists of attributes like `HP`, `Attack`, `Defense`, and others, and the goal is to cluster Pokémon based on these attributes.

## Overview

This implementation of K-Means clustering:
- Uses the **Forgy method** to randomly select initial centroids.
- Iteratively updates centroid positions and assigns data points to clusters.
- Visualizes the clustering using **Principal Component Analysis (PCA)** to reduce dimensionality for 2D plots.

## Features

- **Normalization**: Normalizes the data to avoid certain features dominating the clustering.
- **Euclidean Distance**: Uses Euclidean distance to assign points to their nearest centroids.
- **PCA for Visualization**: Since the dataset contains more than two features, PCA is used to project the data onto a 2D plane for visualization.

## Dataset

The dataset used in this project is the [Pokémon Stats Dataset](https://www.kaggle.com/datasets/shubhamchambhare/pokemons-and-there-stats), which includes various attributes for Pokémon such as:
- `Total`
- `HP`
- `Attack`
- `Defense`
- `Sp_attack`
- `Sp_defense`
- `Speed`

## Code Structure

### `helpers.py`

Contains utility functions for normalization, centroid generation, distance calculation, label assignment, and plotting with PCA.

- **_normalize(X, new_min, new_max)**: Normalizes the features between specified bounds.
- **load_data(filepath, features)**: Loads the Pokémon stats dataset and normalizes it.
- **generate_centroids(X, k)**: Randomly generates `k` centroids from the dataset.
- **_euclidean_distance(X, centroids)**: Calculates the Euclidean distance between points and centroids.
- **get_labels(X, centroids)**: Assigns points to the nearest centroid.
- **plot_with_pca(k, labels, centroids, X)**: Visualizes clusters and centroids in 2D using PCA.

### `kmeans.py`

Defines the K-Means Clustering class that performs the clustering algorithm.

- **KMeansClustering(k, n_iters)**: Initializes the K-Means algorithm with the number of clusters (`k`) and maximum iterations (`n_iters`).
- **fit(X)**: Performs the K-Means clustering on dataset `X`.

### `main.py`

Runs the clustering process by loading the Pokémon dataset and fitting the K-Means model.

## How to Run

1. Install the necessary libraries:

   ```bash
   pip install numpy pandas matplotlib scikit-learn

2. Download the dataset from [here](https://www.kaggle.com/datasets/shubhamchambhare/pokemons-and-there-stats)

3. Execute:

   ```bash
   python main.py


### Notes:
- Ensure you include an example output image (`path-to-your-example-plot.png`) in the `README.md` file if you'd like to provide a visual reference for users.
- You can customize the usage and description based on the way you want users to interact with your project.

This `README.md` file covers the key elements of your project: dataset, methodology, how to run the project, and possible future improvements.
