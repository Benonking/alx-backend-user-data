#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)

AUTH  = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    '''
    Home page
    '''
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    '''
    Reg users
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
    email = request.form.get('email')
    password = request.form.get('password')
    
    if AUTH.valid_login(email=email,password=password):
        AUTH.create_session(email=email)
        return jsonify({"email": email, "message": "logged in"})
    abort(401)

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    session_id = request.form.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_sesssion(user.id)
        redirect('/')
    abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    '''
    '''
    session_id = request.form.get('session_id')
    user = AUTH._db.find_user_by(session_id=session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    '''
    '''
    email = request.form.get('email')
    user = AUTH._db.find_user_by(email=email)
    if user is None:
        abort(403)
    token = AUTH.get_reset_password_token()
    return jsonify({"email": user.email, "reset_token": token})

@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_password')
    new_password = request.form.get('new_password')
    user = AUTH._db.find_user_by(email=email)
    
    if user.reset_token == reset_token:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    abort(403)


if __name__ == '__main__':
    app.run(debug=True)