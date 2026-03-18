# Rules
# Data is transferred in key-value pairs i.e JSON - Universal Key Value Pairs
# Python we converet JSON to a dictionary in JavaScript we convert it to JSON object
# Define url/uri/route
# Define http methods, POST, GET, PUT, DELETE, PATCH
# Define status codes

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import Base, User, Authentication
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

allowed_methods = ["GET", "PUT", "POST", "PATCH", "DELETE"]
DATABASE_URL = "postgresql+psycopg2://postgres:Colesprouse2311!@localhost:5432/flask_auth"

# Connecting sqlalchemy to postgresql using engine function_
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
            data.append({"id": user.id, "name": user.name, "location": user.location, "age": user.age})

        return jsonify({"data": data})
    elif request.method.upper() == "POST":
        data = request.get_json()
    #check if the required fields are received
        if data["name"] == "" or data["location"] == "" or data["age"] == "":
            return jsonify({"err": "All fields required"})
        else: 
            #store users in table using sqlalchemy
            new_user = User(name = data["name"], location = data["location"], age=data["age"])
            my_session.add(new_user)
            my_session.commit()
            return jsonify({"msg": f"Successfully added user {data['name']}"})
    else:
        return jsonify({"error": "Method not Allowed"}), 404
    
@app.route("/register", methods = allowed_methods)
def register_user():
    data = []
    if request.method.upper() == "POST":       
        data = request.get_json()
                  
        existing_user = my_session.query(Authentication).filter_by(email=data["email"]).first()

        if data["fullname"] == "" or data["email"] == "" or data["password"] == "":
            return jsonify({"err": "All fields required"}, 400)
        elif existing_user:
            return jsonify({"err": "Account already exists"}, 400)
        else:
             # create auth record
            new_auth = Authentication(
                fullname = data["fullname"],
                email = data["email"],
                hashed_password = data["password"],
                created_at = datetime.utcnow()
            )   
            my_session.add(new_auth)
            my_session.commit()
            return jsonify({"msg": "User created"}, 201)
    else:
        return jsonify({"err": "Method not allowed"})            
   

@app.route("/login", methods = allowed_methods)
def login():
    data = []
    if request.method.upper() == "POST":
        data = request.get_json()

        query = select(Authentication).where(Authentication.email == data["email"], Authentication.hashed_password == data["password"])
        auth = my_session.scalars(query).first()
        
        if data["email"] == "" or data["password"] == "":
            return jsonify({"err": "All fields required"}, 400)
        elif not auth:
            return jsonify({"err": "Kindly confirm fields entered"}, 400)
        else:
            return jsonify({"msg": "Login successful!"}, 200)
    else:
        return jsonify({"msg": "Method not allowed"})
    
app.run(debug=True)
