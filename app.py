from flask import Flask, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)


# Connect to MongoDB
client = MongoClient('mongodb+srv://yaacovana:jacob@cluster0.vpm3igp.mongodb.net/?retryWrites=true&w=majority')  # your MongoDB server details
db = client['mydatabase']  # Replace 'your_database_name' with the actual name of your MongoDB database
collection = db['customers']  # Replace 'your_collection_name' with the actual name of your MongoDB collection


@app.route('/')
def  index():
    # Retrieve data from MongoDB collection
    data_from_db = list(collection.find())

    # Pass the data to the template
    return render_template('index.html', data=data_from_db)



if __name__ == '__main__':
    app.run(debug=True)


