# PERFORM TEST GET OPERATION USING FLASK AND BROWSER IN MYSQL DATABASE

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import mysql.connector as conn
import os

app = Flask(__name__)

# loading the .env file
load_dotenv(dotenv_path='D:\Data Science\Data Science Portal\data science\APIs\.env')


mydb = conn.connect(
    host="localhost",
    user=os.getenv('USER_NAME'),
    passwd=os.getenv('PASS_WORD')
)

cursor = mydb.cursor()

@app.route("/test")
def test():
    """
    Testing get method

    in the dev server/browser, if you want to see the changes.
    then in the URL, put a '?' and then give the variable name.
    get_name along with '=', place this in URL and it is completed.
    http://127.0.0.1:5000/test?get_name=<your name>
    similarly you can add multiple variable with '&' keyword 
    http://127.0.0.1:5000/test?get_name=<your name>&<your mobile number>
    """
    get_name = request.args.get("get_name")
    mobile_number = request.args.get("mobile_number")
    return "this is my first function for get {} {}".format(get_name, mobile_number)

# fetching data from database and table
@app.route("/test_read")
def test_read_data():
    
    database_name = request.args.get("db_name")
    table_name = request.args.get("tb_name")
    cursor.execute("select * from {}.{}".format(database_name, table_name))
    l = []
    for i in cursor.fetchall():
        l.append(i)
    return jsonify(str(l))

@app.route("/test_readOne")
def test_read_dataOne():
    database_name = request.args.get("db_name")
    table_name = request.args.get("tb_name")
    try:
        cursor.execute("select * from {}.{}".format(database_name, table_name))
        data = cursor.fetchall()
        mydb.commit()
        mydb.close()
    except Exception as e:
        return jsonify(str(e))
    return jsonify(data)

@app.route('/test_create')
def test_create_data():
        # Get data from request.args
        database_name = request.args.get("database_name")
        table_name = request.args.get("table_name")
        name = request.args.get("name")
        number = int(request.args.get("number"))

        # Prepare parameterized query (safer)
        sql = f"INSERT INTO {database_name}.{table_name} (name, number) VALUES (%s, %s)"
        data = (name, number)

        cursor.execute(sql, data)
        mydb.commit()
        return jsonify(str("successfully inserted"))    
if __name__ == "__main__":
    app.run(debug=True)


