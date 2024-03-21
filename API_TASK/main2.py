# PERFORM CRUD OPERATION USING FLASK AND POSTMAN IN MONGODB DATABASE

from flask import Flask, request, jsonify
import pymongo
from dotenv import load_dotenv
import os

app = Flask(__name__)

# loading the .env file
load_dotenv(dotenv_path='D:\Data Science\Data Science Portal\data science\APIs\.env')

# mongodb credentials
username = os.getenv('USERNAMES')
password = os.getenv('PASSWORDS')
cluster_level = os.getenv('CLUSTER_LEVEL')
cluster_number = os.getenv('CLUSTER')

# mongodb url link
mongodb_url = f"mongodb+srv://{username}:{password}@{cluster_level}.mongodb.net/?retryWrites=true&w=majority&appName={cluster_number}"
print(mongodb_url)

# connecting to the mongodb database
client = pymongo.MongoClient(mongodb_url)

db_name = "task_database"
collection_name = "task_collection"

# database = client[db_name]
# collection = database[collection_name]

# Check if the database exists
if db_name not in client.list_database_names():
    # Create the database if it doesn't exist
    database = client[db_name]
    print(f"Database '{db_name}' created.")

# Get the database object
database = client[db_name]

# Check if the collection exists
if collection_name not in database.list_collection_names():
    # Create the collection if it doesn't exist
    collection = database[collection_name]
    print(f"Collection '{collection_name}' created.")

# CREATE
# @app.route("/insert/mongo", methods=['POST'])
# def insert():
#     if request.method == 'POST':
#         name = request.json['name']
#         number = request.json['number']
#         collection.insert_one({name:number})
#         return jsonify(str("successfully inserted"))

@app.route("/insert/mongo", methods=['POST'])
def insert():
    # Get the database object within the function
    database = client[db_name]

    # Get (or create) the collection object within the function
    collection = database[collection_name]

    if request.method == 'POST':
        try:
            name = request.json['name']
            number = request.json['number']
            collection.insert_one({name: number})
            return jsonify(str("successfully inserted"))
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong'}), 500


# UPDATE   
@app.route("/update/mongo" , methods= ['PUT'])
def update():
    # Get the database object within the function
    database = client[db_name]

    # Get (or create) the collection object within the function
    collection = database[collection_name]

    if request.method == 'PUT':
        data = request.get_json()
        update_name = data['update_name']
        new_values = {'$set': {'number': data['update_num']}}

        try:
            update_result = collection.update_one({'name': update_name}, new_values)
            if update_result is None:
                return jsonify({'error': 'Document not found'}), 404
            elif update_result.modified_count == 0:
                # Document might exist but wasn't modified (e.g., same value)
                return jsonify({'message': 'No changes made to the document'}), 200
            else:
                return jsonify({'message': 'Document updated successfully'})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong'}), 500
    
# DELETE
@app.route("/delete/mongo/", methods=['DELETE'])
def delete(delete_name):
    # Get the database object within the function
    database = client[db_name]

    # Get (or create) the collection object within the function
    collection = database[collection_name]
    if request.method == 'DELETE':
        delete_name = request.json['name']
        try:
            delete_result = collection.delete_one({'name': delete_name})
            if delete_result.deleted_count == 0:
                return jsonify({'error': 'Document not found'}), 404
            return jsonify({'message': 'Document deleted successfully'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'Something went wrong'}), 500




if __name__ == '__main__':
    app.run(debug=True)

