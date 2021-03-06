from time import sleep
from ...Backend.database_requests import create_login,is_valid_token,create_user,select_password,select_users,init_db
from random import randint
import pathlib

def get_tab(tab):
    if tab in ("signin","signup"):
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
    if len(username) == 0 or len(password) == 0:
        return {"success": False, "message":"Both email and password need to be provided."},400
    successful,old_password = select_password(username)
    if not successful:
        return "{}", 500
    if old_password is None or password != old_password:
        return {"success": False, "message": "Wrong username or password."},200;
    token = create_token()
    success,_ = create_login(username, token)
    if not success:
        return "{}", 500
    return {"success": True, "message": "Successfully signed in.", "data": token},200

def is_signed_in(token):
    success,is_valid = is_valid_token(token)
    if not success:
        return "{}", 500
    return {"success": is_valid, "message": "Successfully retrieved data."},200

def sign_up(username,password):
    if len(username) == 0 or len(password) == 0:
        return {"success": False, "message":"Both email and password need to be provided."},400
    successful,_ = create_user(username, password)
    if not successful:
        return "{}", 500
    return {"success": True, "message": "Successfully signed up."},200

def signups():
    init_db()
    successful,users = select_users()
    if not successful:
        return "{}", 500
    return {"success": True, "message": "Successfully retrieved data.","data":users},200

def create_token():
    token = ""
    for i in range(10):
        token += str(randint(0,9))
    return token

def get_users():
    success,users = select_users()
    if not success:
        return "{}", 500
    return {"success": True, "message": "Successfully retrieved data.", "data": users},200
