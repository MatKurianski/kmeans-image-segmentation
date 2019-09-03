import numpy as np

def kmeans(X, num_clusters, max_iter=100):
    centroids = np.random.randint(256, size=(num_clusters, X.shape[1]))

    for i in range(max_iter):
        idx = find_closest_centroids(X, centroids)
        new_centroids = compute_mean(X, idx, num_clusters)

        if np.linalg.norm(new_centroids - centroids) == 0:
            break
        else:
            centroids = new_centroids
    
    return centroids, idx

def find_closest_centroids(X, centroids):
    n, clusters = X.shape[0], centroids.shape[0]
    
    distance = np.zeros((n, clusters))
    for k in range(clusters):
        distance[:, k] = np.linalg.norm(X - centroids[k], axis=1)
    
    return distance.argmin(axis=1)


def compute_mean(X, idx, clusters):
    centroids = np.zeros((clusters, X.shape[1]))
    for k in range(clusters):
        xk = X[idx == k]
        if(len(xk) == 0):
            continue
        centroids[k] = xk.mean(axis=0)
    return centroids
