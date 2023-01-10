from flask import Flask, request, send_file, make_response, session
from pathlib import Path
import json
from datetime import datetime
from string import ascii_letters
from random import choice
from .Login_pages.server_interface import (
    get_tab as _get_tab,
    sign_in as _sign_in,
    sign_out as _sign_out,
    is_signed_in as _is_signed_in,
    sign_up as _sign_up,
    get_favourite_fruits as _get_favourite_fruits
)
from .Content_pages.chess_ai.server_interface import (
    select_mode as _select_mode,
    select_colour as _select_colour,
    make_move as _make_move,
    let_ai_make_move as _let_ai_make_move
)
from .database_requests import (
    init_db as _init_db
)

app = Flask(__name__)

def get_app():
    _init_db()
    app.secret_key = "".join([choice(ascii_letters) for _ in range(20)])
    return app

LOGS_DIR = Path(__file__).resolve().parent.parent.joinpath("Log")

@app.before_request
def before_request():
    request.arrival_time = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")[:18]
    try:
        data = json.dumps(request.get_json())
    except:
        data = "{}"
    with open(LOGS_DIR.joinpath("all_requests.txt"),"a") as log_file:
        log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.environ['HTTP_CF_CONNECTING_IP']}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{data}"
        log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
        log_file.write(log_entry+"\n")

@app.after_request
def after_request(response):
    request.departure_time = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")[:18]
    try:
        request_data = json.dumps(request.get_json())
    except:
        request_data = "{}"
    try:
        response_data = json.dumps(response.get_json())
    except:
        response_data = "{}"
    if response.status_code < 400:
        with open(LOGS_DIR.joinpath("successful_requests.txt"),"a") as log_file:
            log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.departure_time}<[SEPARATOR]>{request.environ['HTTP_CF_CONNECTING_IP']}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{response.status_code}<[SEPARATOR]>{request_data}<[SEPARATOR]>{response_data}"
            log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
            log_file.write(log_entry+"\n")
    else:
        try:
            error_description = str(request.error)
            error_type = type(request.error).__name__
        except:
            error_description = ""
            error_type = ""
        with open(LOGS_DIR.joinpath("failed_requests.txt"),"a") as log_file:
            log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.departure_time}<[SEPARATOR]>{request.environ['HTTP_CF_CONNECTING_IP']}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{response.status_code}<[SEPARATOR]>{request_data}<[SEPARATOR]>{response_data}<[SEPARATOR]>{error_type}<[SEPARATOR]>{error_description}"
            log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
            log_file.write(log_entry+"\n")
    return response

@app.errorhandler(Exception)
def error_generic(e):
    request.error = e
    return make_response({}, 500)

@app.errorhandler(404)
def error_404(e):
    request.error = e
    if request.url in ("https://josefine.dev/favicon.ico",
                       "https://josefine.dev/apple-touch-icon.png",
                       "https://josefine.dev/apple-touch-icon-precomposed.png"):
        return make_response({}, 204)
    return make_response({}, 404)

@app.route("/", methods = ["GET"])
def root_page():
    return get_file("Frontend/Landing_page/index.html")

@app.route("/get_file/<path:file_path>", methods = ["GET"])
def get_file(file_path):
    file_path = Path(__file__).resolve().parent.parent.joinpath(file_path)
    if (not file_path.is_file()) or Path(__file__).resolve().parent.parent.joinpath("Frontend") not in file_path.parents:
        return make_response({}, 400)
    return make_response(send_file(file_path))

@app.route("/get_tab", methods = ["POST"])
def get_tab():
    tab = str(request.get_json().get("tab"))
    if tab not in ("about","signin","home","chess_ai","network_simulator","ssl_certs"):
        return make_response({}, 400)
    token = str(request.get_json().get("token"))
    return make_response(_get_tab(tab,token))

@app.route("/sign_in", methods = ["POST"])
def sign_in():
    username = str(request.get_json().get("username"))
    password = str(request.get_json().get("password"))
    return make_response(_sign_in(username,password))

@app.route("/sign_out", methods = ["POST"])
def sign_out():
    token = str(request.get_json().get("token"))
    response = make_response(_sign_out(token))
    return response

@app.route("/is_signed_in", methods = ["POST"])
def is_signed_in():
    token = str(request.get_json().get("token"))
    return make_response(_is_signed_in(token))

@app.route("/sign_up", methods = ["POST"])
def sign_up():
    username = str(request.get_json().get("username"))
    password = str(request.get_json().get("password"))
    favourite_fruit = str(request.get_json().get("favourite_fruit"))
    return make_response(_sign_up(username,password,favourite_fruit))

@app.route("/signups", methods = ["GET"])
def signups():
    return make_response(_signups())

@app.route("/get_favourite_fruits", methods = ["GET"])
def get_favourite_fruits():
    return make_response(_get_favourite_fruits())

@app.route("/select_mode", methods = ["POST"])
def select_mode():
    mode = str(request.get_json().get("mode")).lower()
    return make_response(_select_mode(mode,session))

@app.route("/select_colour", methods = ["POST"])
def select_colour():
    colour = str(request.get_json().get("colour")).lower()
    return make_response(_select_colour(colour,session))

@app.route("/make_move", methods = ["POST"])
def make_move():
    move = str(request.get_json().get("move")).lower()
    return make_response(_make_move(move,session))

@app.route("/let_ai_make_move", methods = ["POST"])
def let_ai_make_move():
    thinking_time = int(str(request.get_json().get("thinking_time")))
    return make_response(_let_ai_make_move(thinking_time,session))
