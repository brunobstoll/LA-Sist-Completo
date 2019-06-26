from sklearn.cluster import KMeans
import numpy as np


X = np.array([[1, 2], [1, 4], [1, 0],
              [4, 2], [4, 4], [4, 0]])

#X = np.array([['A', '2'], ['A', '4'], ['A', '0'],
#              ['B', '2'], ['B', '4'], ['B', '0']])

print (X)

kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)

print(kmeans.labels_)

