#!/usr/bin/env python3
'''
Module for views session routes
'''
import os
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    '''
    route to login authenticated user and create a session
    '''
    email = request.form.get("email")
    password = request.form.get('password')

    if email == '' or email is None:
        return jsonify({"error": "email missing"}), 400
    if password == '' or password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or users == [] :
        return({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


app_views.route('/auth_session/logout',
                methods=['DELETE'], strict_slashes=False)


def logout():
    """
    function to log out user or end ssession
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
