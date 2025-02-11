
def get_users(user_id):
    users={
    123:{"id":123,"name":"Alice"},
    456:{id:456,"name":"bob"}
    }
    return users.get(user_id,{"error":"user not found"})