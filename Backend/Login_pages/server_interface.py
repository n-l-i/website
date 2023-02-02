from time import sleep
from string import punctuation
from random import randint
import pathlib
from ..database_requests import (
    create_login,
    is_valid_token,
    delete_token,
    create_user,
    select_password,
    select_favourite_fruits
)
from .cryptography import (
    balloon_hash
)

def get_tab(tab,token):
    if not tab:
        return {"success": False,
                "message":"Tab name needs to be provided.",
                "data": {}
                },400
    if token is None and tab != "about":
        tab_adress = f"{pathlib.Path(__file__).parent.resolve()}/../../Frontend/Login_pages/{tab}/{tab}.html"
    else:
        tab_adress = f"{pathlib.Path(__file__).parent.resolve()}/../../Frontend/Content_pages/{tab}/{tab}.html"
    try:
        with open(tab_adress, 'r') as file:
            html = file.read().replace('\n', '')
        return {"success":True,
                "message":None,
                "data":{"tab_name":tab,"html":html}
                },200
    except:
        return {},500

def sign_in(username,password):
    if (not username) or (not password):
        return {"success": False,
                "message":"Both email and password need to be provided.",
                "data": {}
                },400
    successful,old_password,salt = select_password(username)
    if not successful:
        return {}, 500
    if old_password is None or balloon_hash(password,salt) != old_password:
        return {"success": False,
                "message": "Wrong email, password or secret.",
                "data": {}
                },200
    token = create_token()
    success,_ = create_login(username, token)
    if not success:
        return {}, 500
    return {"success": True,
            "message": "Successfully signed in.",
            "data": token
            },200

def sign_out(token):
    success = delete_token(token)
    if not success:
        return {}, 500
    return {"success": True,
            "message": "Successfully signed out.",
            "data": {}
            },200

def sign_up(username,password,favourite_fruit):
    if len(username) == 0 or len(password) == 0:
        return {"success": False,
                "message":"Both email and password need to be provided.",
                "data": {}
                },400
    if username.count("@") != 1 or "" in username.split("@"):
        return {"success": False,
                "message":"A valid email needs to be provided.",
                "data": {}
                },400
    if len(password) < 12:
        return {"success": False,
                "message":"Password needs to be at least 12 characters long.",
                "data": {}
                },400
    if len(favourite_fruit) > 32:
        return {"success": False,
                "message":"The name of this fruit is too long.",
                "data": {}
                },400
    if any(c in punctuation and c not in " -()" for c in favourite_fruit):
        return {"success": False,
                "message":"Not a valid fruit name.",
                "data": {}
                },400
    if len(favourite_fruit) == 0:
        favourite_fruit = None
    salt = create_token()
    password_hash = balloon_hash(password,salt)
    successful,_ = create_user(username, password_hash, salt, favourite_fruit)
    if not successful:
        return {}, 500
    return {"success": True,
            "message": "Successfully signed up.",
            "data": {}
            },200

def get_favourite_fruits():
    successful,fruits = select_favourite_fruits()
    if not successful:
        return {}, 500
    return {"success": True,
            "message": "Successfully retrieved data.",
            "data":fruits
            },200

def create_token():
    token = ""
    for i in range(10):
        token += str(randint(0,9))
    return token

