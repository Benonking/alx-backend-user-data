#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE')


if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()


@app.before_request
def before_request():
    '''
    Handle before each request
    '''
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/']

        setattr(request, "current_user", auth.current_user(request))
        if auth.require_auth(request.path, excluded_paths):
            cookie = auth.session_cookie(request)
            if auth.authorization_header(request) is None and cookie is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Un authorised handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbiden_error(error) -> str:
    '''
    Fordiden error
    '''
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
