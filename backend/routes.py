from flask import Blueprint, request, jsonify
from database import collection
from models import User, UserPreferences
from utils.auth_utils import hash_password, verify_password
from datetime import datetime, timezone

routes = Blueprint("routes", __name__)

# Get all users
@routes.route("/users", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0, "password": 0}))
    return jsonify(users)

# Get single user
@routes.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = collection.find_one({"username": username}, {"_id": 0, "password": 0})
    return jsonify(user) if user else (jsonify({"error": "User not found"}), 404)

# Create new user
@routes.route("/users", methods=["POST"])
def create_user():
    data = request.json

    required_fields = ["username", "password", "roles", "preferences"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    if "timezone" not in data["preferences"]:
        return jsonify({"error": "Missing required field: preferences.timezone"}), 400
    
    if not isinstance(data["roles"], list) or not data["roles"]:
        return jsonify({"error": "Roles must be a non-empty list"}), 400
    
    if collection.find_one({"username": data["username"]}):
        return jsonify({"error": "User already exists"}), 400
    
    user = User(
        username=data["username"],
        password=hash_password(data["password"]),
        roles=data["roles"],
        preferences=UserPreferences(timezone=data["preferences"]["timezone"]),
        created_ts=datetime.now(timezone.utc).timestamp(),
        last_updated_at=datetime.now(timezone.utc).timestamp(),
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

    if not collection.find_one({"username": username}):
        return jsonify({"error": "User not found"}), 404

    allowed_fields = {"password", "roles", "preferences", "active"}
    update_data = {key: data[key] for key in data if key in allowed_fields}

    if "roles" in update_data and (not isinstance(update_data["roles"], list) or not update_data["roles"]):
        return jsonify({"error": "Roles must be a non-empty list"}), 400
    
    if "preferences" in update_data and "timezone" not in update_data["preferences"]:
        return jsonify({"error": "Missing required field: preferences.timezone"}), 400
    
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
        
    update_data["last_updated_at"] = datetime.now(timezone.utc).timestamp()
    
    collection.update_one({"username": username}, {"$set": update_data})
    return jsonify({"message": "User updated successfully"})

# Delete user
@routes.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    result = collection.delete_one({"username": username})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})
