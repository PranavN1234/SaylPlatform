from flask import request, jsonify
from app.models.user_model import User  # Import the User model
from app import db, bcrypt  # Import database and bcrypt for hashing
from flask_jwt_extended import create_access_token  # JWT function for creating token
from app.api import api_blueprint  # Import the blueprint

# User registration route (no JWT required)
@api_blueprint.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    # Create new user and hash the password
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# User login route (no JWT required)
@api_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Create JWT token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
