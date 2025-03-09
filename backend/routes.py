from flask import Blueprint, request, jsonify
from database import collection
from models import User, UserPreferences
from utils.auth_utils import hash_password, verify_password
from datetime import datetime

routes = Blueprint("routes", __name__)

# Get all users
@routes.route("/users", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return jsonify(users)

# Get single user
@routes.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = collection.find_one({"username": username}, {"_id": 0})
    return jsonify(user) if user else (jsonify({"error": "User not found"}), 404)

# Create new user
@routes.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if collection.find_one({"username": data["username"]}):
        return jsonify({"error": "User already exists"}), 400
    
    user = User(
        username=data["username"],
        password=hash_password(data["password"]),
        roles=data["roles"],
        preferences=UserPreferences(timezone=data["preferences"]["timezone"]),
        created_ts=datetime.utcnow().timestamp(),
        active=data.get("active", True)
    )
    
    user_dict = user.__dict__
    user_dict["preferences"] = user.preferences.__dict__
    
    collection.insert_one(user_dict)
    return jsonify({"message": "User created successfully"}), 201

# Update user
@routes.route("/users/<username>", methods=["PUT"])
def update_user(username):
    data = request.json
    update_data = {key: data[key] for key in data if key != "username"}
    
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    
    collection.update_one({"username": username}, {"$set": update_data})
    return jsonify({"message": "User updated successfully"})

# Delete user
@routes.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    result = collection.delete_one({"username": username})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})
