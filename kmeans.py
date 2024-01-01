import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import pymongo


def get_mongo_dataframe(connect_str, db_name, collection, query):
    '''Create a connection to MongoDB'''
    client = pymongo.MongoClient(connect_str)
    '''Query MongoDB, and fill a python list with documents to create a DataFrame'''
    db = client[db_name]
    dframe = pd.DataFrame(list(db[collection].find(query)))
    dframe.drop(['_id'], axis=1, inplace=True)
    client.close()
    return dframe


# dim_location, dim_time, dim_incident
# src_dbname = "crime"
# #connecting to mongoDB atlas server. user ncc9kn, pword 123Colby
# conn_str = {'local' : f"mongodb://localhost:27017/", 'atlas' : 'mongodb+srv://ncc9kn:123Colby@cluster0.r70tagk.mongodb.net/?retryWrites=true&w=majority'}
# df = get_mongo_dataframe(conn_str['atlas'], src_dbname, "fact_crime", {})
df = pd.read_csv("coordinates.csv")
print(df.shape)
X = df[["Latitude", "Longitude"]].to_numpy()
# X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
# fig1, ax1 = plt.subplots()
# ax1.scatter(X[:, 0], X[:, 1])
# plt.show()
kmeans = KMeans(n_clusters=75, random_state=0, n_init="auto").fit(X)
labels = kmeans.labels_
# kmeans.predict([[0, 0], [12, 3]])
# centers = kmeans.cluster_centers_
# print(centers)
data = []
fig1, ax1 = plt.subplots()
ax1.scatter(X[:, 0], X[:, 1])
for i in range(len(labels)):
    ax1.annotate(labels[i], (X[i, 0], X[i, 1]), fontsize=20)
    data.append([df["LocationKey"][i], labels[i]])
plt.xlabel("Latitude", fontsize=20)
plt.ylabel("Longitude", fontsize=20)
plt.show()

data = np.array(data)
print(data.shape)
df_cluster = pd.DataFrame(data, columns=["LocationKey", "Cluster"])
df_cluster.to_csv("clusters.csv")
