# Rules
# Data is transferred in key-value pairs i.e JSON - Universal Key Value Pairs
# Python we converet JSON to a dictionary in JavaScript we convert it to JSON object
# Define url/uri/route
# Define http methods, POST, GET, PUT, DELETE, PATCH
# Define status codes

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import Base, User

app = Flask(__name__)

allowed_methods = ["GET", "PUT", "POST", "PATCH", "DELETE"]
DATABASE_URL = "postgresql+psycopg2://postgres:Colesprouse2311!@localhost:5432/flask_crash"

# Connecting sqlalchemy to postgresql using engine function
engine = create_engine(DATABASE_URL, echo=False)

#Create a session to call query methods
session = sessionmaker(bind=engine)
my_session = session()

#Create tables automatically
Base.metadata.create_all(engine)


@app.route("/", methods = allowed_methods)
def home():
    if request.method.upper() == "GET":
        msg = {"Flask API Version": "1.0"}
        return jsonify(msg), 200
    else:
        return jsonify({"err": "Method not Allowed."})
    
@app.route("/users", methods = allowed_methods)
def get_users():
    if request.method.upper() == "GET":
        query = select(User)
        users = my_session.scalars(query).all()

        data = []

        for user in users:
            data.append({"id": user.id, "name": user.name, "location": user.location})

            return jsonify({"data": data})
    elif request.method.upper() == "POST":
        data = request.get_json()
    #check if the required fields are received
        if data["name"] == "" or data["location"] == "":
            return jsonify({"err": "Name and location required"})
        else: 
            #store users in table using sqlalchemy
            new_user = User(name = data["name"], location = data["location"])
            my_session.add(new_user)
            my_session.commit()
            return jsonify({"msg": f"Successfully added user {data['name']}"})
    else:
        return jsonify({"error": "Method not Allowed"}), 404


app.run(debug=True)
