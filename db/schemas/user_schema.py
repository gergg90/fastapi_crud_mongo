

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]


