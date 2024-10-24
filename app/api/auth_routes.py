from flask import request, jsonify
from app.models.user_model import User  # Import the User model
from app import db, bcrypt  # Import database and bcrypt for hashing
from flask_jwt_extended import create_access_token  # JWT function for creating token
from app.api import api_blueprint  # Import the blueprint
from flask_jwt_extended import jwt_required


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

    # Create new user with hashed password (handled by the User model)
    new_user = User(email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error saving user"}), 500

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

    # Verify password using the User model's check_password method
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Create JWT token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


# Logout route (optional as JWT is stateless)
@api_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Optional: Add logic here to handle logout if necessary
    return jsonify({"msg": "Logged out successfully"}), 200