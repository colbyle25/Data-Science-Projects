import csv
from geopy.geocoders import Nominatim
import pymongo
import pandas as pd
import numpy as np

# ignore = []
# ignore_file = "IgnoredCrimes.txt"
# f = open(ignore_file, "r")
# lines = f.readlines()
# for line in lines:
#     ignore.append(line[:-1])
# f.close()
#
geolocator = Nominatim(timeout=10, user_agent = "myGeolocator")
city_name = "Charlottesville"
state_name = "VA"
#
# file_name = "Crime_Data.csv"
#
# found = 0
# missing = 0
#
# outfile = "Crime_Coordinates.txt"
# f = open(outfile, "w")


def get_mongo_dataframe(connect_str, db_name, collection, query):
    '''Create a connection to MongoDB'''
    client = pymongo.MongoClient(connect_str)
    '''Query MongoDB, and fill a python list with documents to create a DataFrame'''
    db = client[db_name]
    dframe = pd.DataFrame(list(db[collection].find(query)))
    dframe.drop(['_id'], axis=1, inplace=True)
    client.close()
    return dframe


src_dbname = "crime"
# connecting to mongoDB atlas server. user ncc9kn, pword 123Colby
conn_str = {'local' : f"mongodb://localhost:27017/", 'atlas' : 'mongodb+srv://ncc9kn:123Colby@cluster0.r70tagk.mongodb.net/?retryWrites=true&w=majority'}
df = get_mongo_dataframe(conn_str['atlas'], src_dbname, "dim_location", {})
coordinates = []
print(df.shape)
for i in range(df.shape[0]):
    address = str(df["BlockNumber"][i]) + " " + str(df["StreetName"][i]) + "," + city_name + "," + state_name
    location = geolocator.geocode(address)
    if location is not None:
        coordinate = [df["LocationKey"][i], location.latitude, location.longitude]
        print(str(df["StreetName"][i]))
        coordinates.append(coordinate)
        print(coordinate)
    print("-")

coordinates = np.array(coordinates)
df_coordinates = pd.DataFrame(coordinates, columns=["LocationKey", "Latitude", "Longitude"])
df_coordinates.to_csv("coordinates.csv")
# with open(file_name, newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for row in reader:
#         crime = row[1]
#         block = row[3]
#         street = row[4]
#         date = row[6]
#         year = date[0:4]
#         if year != 'Date':
#             year = int(year)
#             if year > 2021:
#                 address = block+" "+street+","+city_name+","+state_name
#                 if crime not in ignore:
#                     location = geolocator.geocode(address)
#                     if location != None:
#                         coordinate = [address, location.latitude, location.longitude]
#                         found = found + 1
#                         f.write(crime+","+str(coordinate[0])+","+str(coordinate[1])+","+str(coordinate[2])+","+date+"\n")
#                     else:
#                         missing = missing + 1
# print(found, missing) #3469 959
# csvfile.close()
# f.close()
