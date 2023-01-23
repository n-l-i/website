from time import sleep
from string import punctuation
from ..database_requests import (
    create_login,
    is_valid_token,
    delete_token,
    create_user,
    select_password,
    select_favourite_fruits
)
from random import randint
import pathlib

def get_tab(tab,token):
    if not tab:
        return {"success": False, "message":"Tab name needs to be provided.", "data": {}},400
    if token:
        result = is_signed_in(token)[0]
        signed_in = result["success"] and result["data"]
    else:
        signed_in = False
    if not signed_in:
        tab_adress = f"{pathlib.Path(__file__).parent.resolve()}/../../Frontend/Login_pages/{tab}/{tab}.html"
    else:
        tab_adress = f"{pathlib.Path(__file__).parent.resolve()}/../../Frontend/Content_pages/{tab}/{tab}.html"
    try:
        with open(tab_adress, 'r') as file:
            html = file.read().replace('\n', '')
        return {"success":True,"message":None,"data":{"tab_name":tab,"html":html}},200
    except:
        return {"success":False,"message":None},500

def sign_in(username,password):
    if (not username) or (not password):
        return {"success": False, "message":"Both email and password need to be provided."},400
    successful,old_password = select_password(username)
    if not successful:
        return {}, 500
    if old_password is None or password != old_password:
        return {"success": False, "message": "Wrong username or password."},200
    token = create_token()
    success,_ = create_login(username, token)
    if not success:
        return {}, 500
    return {"success": True, "message": "Successfully signed in.", "data": token},200

def sign_out(token):
    if len(token) == 0:
        return {"success": False, "message":"Access token needs to be provided."},400
    successful,token_is_valid = is_valid_token(token)
    if not successful:
        return {}, 500
    if not token_is_valid:
        return {"success": False, "message": "Access token is not valid."},200
    success = delete_token(token)
    if not success:
        return {}, 500
    return {"success": True, "message": "Successfully signed out."},200

def is_signed_in(token):
    if not token:
        return {"success": True, "data": False, "message": "Successfully retrieved data."},200
    success,is_valid = is_valid_token(token)
    if not success:
        return {}, 500
    return {"success": True, "data": is_valid, "message": "Successfully retrieved data."},200

def sign_up(username,password,favourite_fruit):
    if len(username) == 0 or len(password) == 0:
        return {"success": False, "message":"Both email and password need to be provided."},400
    if username.count("@") != 1 or "" in username.split("@"):
        return {"success": False, "message":"A valid email needs to be provided."},400
    if len(password) < 12:
        return {"success": False, "message":"Password needs to be at least 12 characters long."},400
    if len(favourite_fruit) > 32:
        return {"success": False, "message":"The name of this fruit is too long."},400
    if any(c in punctuation and c not in " -()" for c in favourite_fruit):
        return {"success": False, "message":"Not a valid fruit name."},400
    if len(favourite_fruit) == 0:
        favourite_fruit = None
    successful,_ = create_user(username, password, favourite_fruit)
    if not successful:
        return {}, 500
    return {"success": True, "message": "Successfully signed up."},200

def get_favourite_fruits():
    successful,fruits = select_favourite_fruits()
    if not successful:
        return {}, 500
    return {"success": True, "message": "Successfully retrieved data.","data":fruits},200

def create_token():
    token = ""
    for i in range(10):
        token += str(randint(0,9))
    return token

