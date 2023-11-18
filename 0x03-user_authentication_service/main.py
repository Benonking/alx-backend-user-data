#!/usr/bin/env python3
import requests
base_url ="http://127.0.0.1:5000"
def register_user(email:str, password:str)-> None:
	url = f"{base_url}/users"
	data = {"email":email, "password": password}
	res = requests.post(url, json=data)
	assert res.status_code == 200
def log_in_wrong_password(email:str, password:str) ->None:
	url = f"{base_url}/login"
	data = {"email":email, "password": password}
	res = requests.post(url, data=data)
	assert res.status_code == 401
def log_in(email:str, password:str)->str:
	url = f"{base_url}/login"
	data = {"email": email, "password": password}
	res = requests.post(url, json=data)
	assert res.status_code == 200
def profile_unlogged()->None:
	
	url = f"{base_url}/profile"
	#data = {"email": '', "password": ''}
	res = requests.get(url)
	assert res.status_code == 403
def profile_logged(session_id: str) -> None:
	url = f"{base_url}/profile"
	data = {"session_id":session_id}
	res = requests.get(url, json=data)
	assert res.status_code == 200
def log_out(session_id: str) -> None:
	url = f"{base_url}/sessions"
	data = {"session_id":session_id}
	res = requests.delete(url, json=data)
	assert res.status_code == 403
def reset_password_token(session_id:str) ->None:
	url = f"{base_url}/reset_password"
	data = {"session_id":session_id}
	res = requests.post(url, json=data)
	assert res.status_code == 403
def update_password(email: str, reset_token: str, new_password: str) -> None:
	url = f"{base_url}/reset_passord"
	data = {"email":email, "reset_token": reset_token, "new_password": new_password}
	res = requests.put(url,json=data)
	assert res.status_code == 403



EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)