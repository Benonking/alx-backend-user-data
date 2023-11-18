#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)

AUTH  = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index() ->str:
    '''
    Return Home page payload
    '''
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    '''
    Return:
        Account creattion payloadReg users
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email=email, password=password)
        res = {
          'email': new_user.email,
          'message': "user created"}
        return jsonify(res)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''
    Return response to login request payload
    the function creates  new sssion onlogin
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    
    if AUTH.valid_login(email=email,password=password):
        session_id = AUTH.create_session(email=email)
        res =  jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    abort(401)

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_sesssion(user.id)
        redirect('/')
    abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() ->str:
    '''
    Return User's password reset payload
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    '''
    Reset users password route
    '''
    email = request.form.get('email')
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})

@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() ->str:
    email = request.form.get('email')
    reset_token = request.form.get('reset_password')
    new_password = request.form.get('new_password')
    changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        changed =True
    except ValueError:
        return False
    if changed is False:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')