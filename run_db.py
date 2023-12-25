import pymongo

myclient = pymongo.MongoClient("mongodb+srv://yaacovana:jacob@cluster0.vpm3igp.mongodb.net/?retryWrites=true&w=majority")

mydb = myclient["mydatabase"]


mycol = mydb["customers"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)
