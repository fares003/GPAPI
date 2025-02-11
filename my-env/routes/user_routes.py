from flask import Blueprint,request,jsonify

from controllers.user_controller import get_users

user_bp=Blueprint('users',__name__)

@user_bp.route('/get_user',methods=['POST'])
def get_user():
    data=request.get_json()#to get json body
    if not data or "user_id" not in data:
        return jsonify({"error":"user ID is required"}),400
    user_id=data["user_id"]
    user=get_users(user_id)

    return jsonify(user)


