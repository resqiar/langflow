from db import social_data_collection, notes_collection

def get_values(_id):
    return {
        "_id": _id, 
        "social_data": {
            "name": "Instagram",
            "followers": 0,
            "likes": 0,
            "status": "Personal",
            "post_preferences": "Once a month",
        },
        "goals": ["Followers Gain"],
    }
    
def create_profile(_id):
    v = get_values(_id)
    result = social_data_collection.insert_one(v)
    return result.inserted_id, result

def get_profile(_id):
    return social_data_collection.find_one({"_id": {"$eq": _id}})

def get_notes(_id):
    return list(notes_collection.find({"user_id": {"$eq": _id}}))