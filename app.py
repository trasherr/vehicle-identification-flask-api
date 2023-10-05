import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_restful import Resource, Api


CREATE_ROOMS_TABLE=(
    "CREATE TABLE IF NOT EXISTS Vehicle_Record(id SERIAL PRIMARY KEY,carNo VARCHAR(10),inTime TIMESTAMP,outTime TIMESTAMP)"
)

load_dotenv()
# creating the flask app
app = Flask(__name__)
url=os.getenv("DATABASE_URL")
api = Api(app)

connection=psycopg2.connect(url)
class Hello(Resource):

    def get(self):
  
        return jsonify({'message': 'hello world'})
  
    def post(self):
        data = request.get_json()
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE) 
        return jsonify({'data': data}), 201

  
api.add_resource(Hello, '/')
#api.add_resource(Upload,'/upload')
@app.post('/upload')
def create_room():
    data=request.get_json()
    name=data["name"]
    with connection.cursor() as cursor:
        cursor.execute(CREATE_ROOMS_TABLE)
    return {"message":"Yes Table Created"}
  
if __name__ == '__main__':
    app.run(debug = True)