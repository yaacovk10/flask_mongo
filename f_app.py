from flask import Flask, jsonify,request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017")
client = MongoClient("mongodb+srv://yaacovana:jacob@cluster0.vpm3igp.mongodb.net/?retryWrites=true&w=majority")


db = client.myDatabase1
my_collection = db["recipes"]

# Route to get all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    result = my_collection.find()
    recipes = []
    for doc in result:
        recipe = {
            'name': doc['name'],
            'ingredients_count': len(doc['ingredients']),
            'prep_time': doc['prep_time']
        }
        recipes.append(recipe)
    return jsonify(recipes)

# Route to get a recipe by ingredient
@app.route('/recipes/<ingredient>', methods=['GET'])
def get_recipe_by_ingredient(ingredient):
    print(ingredient)
    my_doc = my_collection.find_one({"ingredients": ingredient})
    if my_doc:
        return jsonify(my_doc)
    else:
        return jsonify({"message": f"No recipes found with '{ingredient}' as an ingredient."}), 404

# Route to update a recipe's prep time by ingredient
@app.route('/recipes/<ingredient>', methods=['PUT'])
def update_prep_time_by_ingredient(ingredient):
    my_doc = my_collection.find_one_and_update({"ingredients": ingredient}, {"$set": {"prep_time": 72}}, new=True)
    if my_doc:
        return jsonify(my_doc)
    else:
        return jsonify({"message": f"No recipes found with '{ingredient}' as an ingredient."}), 404

# Route to delete recipes by name
@app.route('/recipes/delete/<name>', methods=['DELETE'])
def delete_recipe_by_name(name):
    my_result = my_collection.delete_many({"name": name})
    return jsonify({"message": f"Deleted {my_result.deleted_count} records."})


# Route to create a new recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    if not data or 'name' not in data or 'ingredients' not in data or 'prep_time' not in data:
        return jsonify({"message": "Invalid data. 'name', 'ingredients', and 'prep_time' are required."}), 400

    new_recipe = {
        "name": data['name'],
        "ingredients": data['ingredients'],
        "prep_time": data['prep_time']
    }

    # try:
    result = my_collection.insert_one(new_recipe)
    return jsonify({"message": "Recipe created successfully.", "id": str(result.inserted_id)}), 201
    # except Exception as e:
    #     return jsonify({"message": f"Failed to create recipe: {str(e)}"}), 500

# Other routes remain the same...









if __name__ == '__main__':
    app.run(debug=True)
