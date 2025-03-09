import json
import pymongo
from utils.auth_utils import hash_password
from datetime import datetime
from models import User, UserPreferences
from database import collection

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Parse Data and Insert into MongoDB
def insert_users(file_path):
    data = load_json(file_path)["users"]
    users = []
    for item in data:
        roles = []
        if item.get("is_user_admin"): roles.append("admin")
        if item.get("is_user_manager"): roles.append("manager")
        if item.get("is_user_tester"): roles.append("tester")
        
        user = User(
            username=item["user"],
            password=hash_password(item["password"]),
            roles=roles,
            preferences=UserPreferences(timezone=item["user_timezone"]),
            active=item.get("is_user_active", True),
            created_ts=datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        )
        user_dict = user.__dict__  # Convert User to dictionary
        user_dict["preferences"] = user.preferences.__dict__  # Convert nested UserPreferences to dictionary
        users.append(user_dict)
    
    collection.insert_many(users)
    print("Users inserted successfully!")

def seed_database():
    if collection.count_documents({}) == 0:
        insert_users("udata.json")
        print("Database seeded successfully!")
    else:
        print("Database already contains data. Skipping seeding.")

if __name__ == "__main__":
    seed_database()