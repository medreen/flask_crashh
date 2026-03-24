# Rules
# Data is transferred in key-value pairs i.e JSON - Universal Key Value Pairs
# Python we converet JSON to a dictionary in JavaScript we convert it to JSON object
# Define url/uri/route
# Define http methods, POST, GET, PUT, DELETE, PATCH
# Define status codes

import sentry_sdk
from flask import Flask
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from database import Base, Employee, Authentication
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "medreen2311!"

CORS(app)
sentry_sdk.init(
    dsn="https://470f28118277d8dcd133a830ef8e0564@o4511094689628160.ingest.de.sentry.io/4511094764601424",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

allowed_methods = ["GET", "PUT", "POST", "PATCH", "DELETE"]
try:
    DATABASE_URL = "postgresql+psycopg2://postgres:Colesprouse2311!@localhost:5432/flask_auth"
except Exception as e:
    pass
    print("Error connecting to database")
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
    
@app.route("/employees", methods = allowed_methods)
@jwt_required()
def get_users():    
    try:        
        if request.method.lower() == "get":
            employee_list = []
            query = select(Employee)
            my_employees = list(my_session.scalars(query).all())

            for employee in my_employees:
                employee_list.append({"id": employee.id,
                                "name": employee.name,
                                "location": employee.location,
                                "age": employee.age})

            return jsonify({"data": employee_list}), 200
        elif method == "post":
            # convert json to dictionary
            data = request.get_json()
            # check if all fields are received
            if data["name"] == "" or data["location"] == "" or data["age"] == "":
                return jsonify({"msg": "All fields required"}), 401
            else:
                # employee_list.append(data)/store employee in employees tables using SQLAlchemypip
                new_employee = Employee(
                    name=data["name"], location=data["location"], age=data["age"])
                my_session.add(new_employee)
                my_session.commit()
                my_session.close()

                return jsonify({"msg": "Successfully added employee"}), 201
        else:
            return jsonify({"msg": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/register', methods=allowed_methods)
def register():
    try:    
        if request.method.lower() == "post":
            data = request.get_json()

            # ensure all fields are set and check if email already exists in the user authentication table.
            if data["full_name"] == "" or data["email"] == "" or data["password"] == "":
                return jsonify({"error": "Full name, email and password cannot be empty"}), 400

            existing_user = my_session.query(Authentication).filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"error": "Email already registered"}), 409

            hashed_password=bcrypt.generate_password_hash(data["password"]).decode("utf-8")
           
            new_auth = Authentication(
                email=data["email"],
                hashed_password= hashed_password,
                full_name=data["full_name"],
                created_at=datetime.utcnow()
            )
           
            my_session.add(new_auth)
            my_session.commit()            
            token=create_access_token(identity=data["email"])

            return jsonify({"message": "User created",
                            "token":f"{token}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login',methods=allowed_methods)   
def login():
    try:
        if request.method.lower() == "post":
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"error": "Email and password required"}), 400

            query = select(Authentication).where(Authentication.email == email)
            auth = my_session.scalars(query).first()
            
            if not auth:
                return jsonify({"error": "Invalid email"}), 401
            elif not bcrypt.check_password_hash(auth.hashed_password,password):
                return jsonify({"error": "Invalid password"}), 401
            else:
                token=create_access_token(identity=data["email"])

                return jsonify({
                    "message": "Login successful",
                    "user": {
                        "id": auth.id,
                        "full_name": auth.full_name,
                        "email": auth.email
                    },
                    "token":f"{token}"
                }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500

app.run(debug=True)