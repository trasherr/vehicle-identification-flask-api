import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

CREATE_VEHICLE_TABLE =(
    "CREATE TABLE IF NOT EXISTS Vehicle_Record ( id SERIAL PRIMARY KEY,carNo VARCHAR(10), inTime TIMESTAMP,outTime TIMESTAMP);"   
    
)

INSERT_VEHICLE = "INSERT INTO Vehicle_Record (carNo, inTime, outTime) VALUES (%s, %s, %s);"

load_dotenv()

# Creating the flask app
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
api = Api(app)

# Establishing a database connection
connection = psycopg2.connect(url)


class Hello(Resource):
    def get(self):
        return jsonify({'message': 'Hello, world'})

    def post(self):
        data = request.get_json()
        with connection.cursor() as cursor:
            cursor.execute(CREATE_VEHICLE_TABLE)
        return jsonify({'data': data}), 201


api.add_resource(Hello, '/')

# API endpoint for uploading data
@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        data = request.get_json()
        car_no = data["carNo"]
        in_time = data["inTime"]
        out_time = data["outTime"]

        with connection.cursor() as cursor:
            cursor.execute(CREATE_VEHICLE_TABLE)
            cursor.execute(INSERT_VEHICLE, (car_no, in_time, out_time))
        
        connection.commit()

        return {"message": "Table created and data inserted successfully"}

    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    app.run(debug=True)
