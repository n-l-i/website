from flask import Flask, request, send_file, make_response
from pathlib import Path
import json
from datetime import datetime
from string import ascii_letters
from random import choice, uniform
from ipaddress import ip_address, ip_network
from functools import lru_cache
from time import time
from .Login_pages.server_interface import (
    get_tab as _get_tab,
    sign_in as _sign_in,
    sign_out as _sign_out,
    sign_up as _sign_up,
    get_favourite_fruits as _get_favourite_fruits
)
from .Content_pages.chess_ai.server_interface import (
    new_chessgame as _new_chessgame,
    make_move as _make_move,
    let_ai_make_move as _let_ai_make_move
)
from .database_requests import (
    is_valid_token
)

constant_time_pages = {"sign_in":0,
                       "is_signed_in":0,
                       "sign_out":0,
                       "sign_up":0}

app = Flask(__name__)
app.secret_key = "".join([choice(ascii_letters) for _ in range(20)])

def get_app():
    return app

LOGS_DIR = Path(__file__).resolve().parent.parent.joinpath("Log")
BACKEND_DIR = Path(__file__).resolve().parent

def is_proxied(http_request):
    for network in cloudflare_ips():
        if ip_address(http_request.remote_addr) in ip_network(network):
            return True
    return False

@lru_cache(maxsize=None)
def cloudflare_ips():
    with open(BACKEND_DIR.joinpath("cloudflare_ips.json")) as file_obj:
        ips = json.load(file_obj)["result"]
    ips = ips["ipv4_cidrs"]+ips["ipv6_cidrs"]
    return ips

def is_trusted_ip(address):
    for network in cloudflare_ips()+["127.0.0.1/32"]:
        if ip_address(address) in ip_network(network):
            return True
    return False

def get_origin_ip(http_request):
    # Select the most recently appended IP that is not a trusted proxy.
    request_route = http_request.access_route+[http_request.remote_addr]
    for address in reversed(request_route):
        if not is_trusted_ip(address):
            return address
    # The request originates from a trusted proxy
    return request_route[0]

def _is_valid(token):
    assert isinstance(token,str) or token is None
    success,token_is_valid = is_valid_token(token)
    if not success:
        return {}, 500
    if not token_is_valid:
        return {"success": False,
                "message": "Valid access token needs to be provided.",
                "data": {}
                },400
    return {"success": True,
            "message": "Successfully retrieved data.",
            "data": True
            },200

@app.before_request
def before_request():
    request.arrival_time = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")[:18]
    request.arrival_timestamp = time()
    if request.remote_addr != "127.0.0.1" and not is_proxied(request):
        return make_response({}, 404)
    try:
        data = json.dumps(request.get_json())
    except:
        data = "{}"
    request.origin_ip = get_origin_ip(request)
    with open(LOGS_DIR.joinpath("all_requests.txt"),"a") as log_file:
        log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.origin_ip}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{data}"
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
            log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.departure_time}<[SEPARATOR]>{request.origin_ip}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{response.status_code}<[SEPARATOR]>{request_data}<[SEPARATOR]>{response_data}"
            log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
            log_file.write(log_entry+"\n")
    else:
        try:
            error_description = str(request.error)
            error_type = type(request.error).__name__
        except:
            error_description = ""
            error_type = ""
        if "HTTP_CF_CONNECTING_IP" in request.environ:
            with open(LOGS_DIR.joinpath("failed_requests.txt"),"a") as log_file:
                log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.departure_time}<[SEPARATOR]>{request.origin_ip}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{response.status_code}<[SEPARATOR]>{request_data}<[SEPARATOR]>{response_data}<[SEPARATOR]>{error_type}<[SEPARATOR]>{error_description}"
                log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
                log_file.write(log_entry+"\n")
        else:
            with open(LOGS_DIR.joinpath("non_proxied_requests.txt"),"a") as log_file:
                log_entry = f"{request.arrival_time}<[SEPARATOR]>{request.departure_time}<[SEPARATOR]>{request.origin_ip}<[SEPARATOR]>{request.method}<[SEPARATOR]>{request.url}<[SEPARATOR]>{response.status_code}<[SEPARATOR]>{request_data}<[SEPARATOR]>{response_data}<[SEPARATOR]>{error_type}<[SEPARATOR]>{error_description}"
                log_entry = log_entry.replace(";","").replace("<[SEPARATOR]>",";").replace("\n","")
                log_file.write(log_entry+"\n")
    if response.get_json():
        assert "success" in response.get_json(), (request.get_json(),response.get_json())
        assert "message" in response.get_json(), (request.get_json(),response.get_json())
        assert "data" in response.get_json(), (request.get_json(),response.get_json())
    # Make sure that security pages give constant time responses.
    if request.path in constant_time_pages:
        constant_time_pages[request.path] = max(constant_time_pages[request.path],
                                               time()-request.arrival_timestamp)
        response_time = constant_time_pages[request.path]*uniform(1,1.5)
        while time() < request.arrival_timestamp+response_time:
            pass
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
    return get_file("Frontend/Landing_page/index_live.html")

@app.route("/get_file/<path:file_path>", methods = ["GET"])
def get_file(file_path):
    assert isinstance(file_path,str)
    file_path = Path(__file__).resolve().parent.parent.joinpath(file_path)
    if (not file_path.is_file()) or Path(__file__).resolve().parent.parent.joinpath("Frontend") not in file_path.parents:
        print(file_path.is_file(),Path(__file__).resolve().parent.parent.joinpath("Frontend"))
        return make_response({}, 400)
    return make_response(send_file(file_path))

@app.route("/get_tab", methods = ["POST"])
def get_tab():
    tab = str(request.get_json().get("tab"))
    if tab not in ("about","signin","home","chess_ai","spbmap","network_simulator","ssl_certs"):
        return make_response({}, 400)
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        token = None
    return make_response(_get_tab(tab,token))

@app.route("/sign_in", methods = ["POST"])
def sign_in():
    username = request.get_json().get("username")
    assert isinstance(username,str) or username is None
    password = request.get_json().get("password")
    assert isinstance(password,str) or password is None
    return make_response(_sign_in(username,password))

@app.route("/sign_out", methods = ["POST"])
def sign_out():
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    return make_response(_sign_out(token))

@app.route("/is_signed_in", methods = ["POST"])
def is_signed_in():
    token = request.get_json().get("token")
    token_is_valid = _is_valid(token)[1] == 200
    return make_response(({"success": True,
                           "message": "Successfully retrieved data.",
                           "data": token_is_valid
                           },200))

@app.route("/sign_up", methods = ["POST"])
def sign_up():
    username = request.get_json().get("username")
    assert isinstance(username,str) or username is None
    password = request.get_json().get("password")
    assert isinstance(password,str) or password is None
    favourite_fruit = request.get_json().get("favourite_fruit")
    assert isinstance(favourite_fruit,str) or favourite_fruit is None
    return make_response(_sign_up(username,password,favourite_fruit))

@app.route("/get_favourite_fruits", methods = ["GET"])
def get_favourite_fruits():
    return make_response(_get_favourite_fruits())

@app.route("/select_mode", methods = ["POST"])
def select_mode():
    mode = request.get_json().get("mode")
    assert isinstance(mode,str) or mode is None
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    return make_response(_new_chessgame(token,mode=mode))

@app.route("/select_colour", methods = ["POST"])
def select_colour():
    colour = request.get_json().get("colour")
    assert isinstance(colour,str) or colour is None
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    return make_response(_new_chessgame(token,colour=colour))

@app.route("/new_chessgame", methods = ["POST"])
def new_chessgame():
    mode = request.get_json().get("mode")
    assert isinstance(mode,str) or mode is None
    colour = request.get_json().get("colour")
    assert isinstance(colour,str) or colour is None
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    return make_response(_new_chessgame(token,mode,colour))

@app.route("/make_move", methods = ["POST"])
def make_move():
    move = str(request.get_json().get("move")).lower()
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    return make_response(_make_move(move,token))

@app.route("/let_ai_make_move", methods = ["POST"])
def let_ai_make_move():
    token = request.get_json().get("token")
    if _is_valid(token)[1] != 200:
        return _is_valid(token)
    thinking_time = float(str(request.get_json().get("thinking_time")))
    assert 0 <= thinking_time <= 60
    return make_response(_let_ai_make_move(thinking_time,token))
