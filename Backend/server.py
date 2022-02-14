from flask import Flask, request, send_file
from flask_cors import CORS
from time import sleep
from database_requests import create_login,create_user,select_password,init_db

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ["GET"])
def hello():
    init_db()
    return "Hello!"

@app.route("/js", methods = ["GET"])
def send_js():
    return send_file("../Frontend/index.js")

@app.route("/select_tab", methods = ["POST"])
def select_tab():
    tab = request.get_json().get("tab")
    try:
        with open(f"../Frontend/{tab}/{tab}.html", 'r') as file:
            data = file.read().replace('\n', '')
        return {"success":True,"message":None,"data":data},200
    except:
        return {"success":False,"message":None},500

@app.route("/sign_in", methods = ["POST"])
def sign_in():
    init_db()
    create_user("email@domain.com", "p4ssw0rd")
    username = str(request.get_json().get("username"))
    password = str(request.get_json().get("password"))
    if username is None or password is None:
        return {"success": False, "message":"Both email and password need to be provided."},400
    successful,old_password = select_password(username)
    if not successful:
        return "{}", 500
    if old_password is None or password != old_password:
        return {"success": False, "message": "Wrong username or password."},200;
    token = create_token()
    success,_ = create_login(username, token,2)
    if success == False:
        return "{}", 500
    return {"success": True, "message": "Successfully signed in.", "data": token},200

def create_token():
    return "hej"

app.run(debug=True,port=5000)
