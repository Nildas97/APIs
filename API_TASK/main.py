# PERFORM CRUD OPERATION USING FLASK AND POSTMAN IN MYSQL DATABASE

from flask import Flask, request, jsonify
import mysql.connector as conn
from dotenv import load_dotenv
import os

app = Flask(__name__)


# getting current root directory
ROOT_DIR = os.getcwd()

# getting the .env folder path
ENV_FILE_PATH = os.path.join(ROOT_DIR, '.env')

# loading the .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

mydb = conn.connect(
    host="localhost",
    user=os.getenv('USER_NAME'),
    passwd=os.getenv('PASS_WORD')
)

cursor = mydb.cursor()
cursor.execute("create database if not exists taskdb") 
cursor.execute("create table if not exists taskdb.tasktable (name varchar(30), number integer(5))") 

# CREATE
@app.route('/insert', methods=['POST'])
def insert(debug=True):
    if request.method=="POST":
        name = request.json['name']
        number = request.json['number']
        cursor.execute("insert into taskdb.tasktable values(%s, %s)", (name, number))
        mydb.commit()
        return jsonify(str("successfully inserted"))

# READ
@app.route("/fetch",methods = ['POST','GET'])
def fetch_data():
    cursor.execute("select * from taskdb.tasktable")
    l = []
    for i in cursor.fetchall():
        l.append(i)
    return jsonify(str(l))

# UPDATE   
@app.route("/update" , methods= ['POST'])
def update():
    if request.method=='POST':
        get_number = request.json['get_number']
        cursor.execute("update taskdb.tasktable set name = 'laptulin' where number = (%s)", (get_number,))

        mydb.commit()
        return jsonify(str("updated successfully"))
    
# DELETE
@app.route("/delete" , methods= ['POST'])
def delete():
    if request.method == 'POST':
        name_del = request.json['name_del']
        cursor.execute("delete from taskdb.tasktable where name = (%s)",(name_del,))
        mydb.commit()
        return jsonify(str("deleted successfully"))

    
if __name__ == '__main__':
    app.run()
