from flask import Flask, request, send_file
import pathlib
from ..Backend.Login_pages.server_interface import (
    get_tab as _get_tab,
    sign_in as _sign_in,
    sign_out as _sign_out,
    is_signed_in as _is_signed_in,
    sign_up as _sign_up,
    signups as _signups,
    get_users as _get_users
)
from ..Backend.Content_pages.chess_ai.server_interface import (
    select_mode as _select_mode,
    select_colour as _select_colour,
    make_move as _make_move,
    let_ai_make_move as _let_ai_make_move
)
from ..Backend.database_requests import (
    init_db as _init_db
)

_init_db()

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def hello():
    return send_file("../Frontend/Landing_page/index.html")

@app.route("/get_file/<path:file_path>", methods = ["GET"])
def get_file(file_path):
    return send_file(f"../{file_path}")

@app.route("/get_tab", methods = ["POST"])
def get_tab():
    tab = str(request.get_json().get("tab"))
    return _get_tab(tab)

@app.route("/sign_in", methods = ["POST"])
def sign_in():
    username = str(request.get_json().get("username"))
    password = str(request.get_json().get("password"))
    return _sign_in(username,password)

@app.route("/sign_out", methods = ["POST"])
def sign_out():
    token = str(request.get_json().get("token"))
    return _sign_out(token)

@app.route("/is_signed_in", methods = ["POST"])
def is_signed_in():
    token = str(request.get_json().get("token"))
    return _is_signed_in(token)

@app.route("/sign_up", methods = ["POST"])
def sign_up():
    username = str(request.get_json().get("username"))
    password = str(request.get_json().get("password"))
    return _sign_up(username,password)

@app.route("/signups", methods = ["GET"])
def signups():
    return _signups()

@app.route("/get_users", methods = ["GET"])
def get_users():
    return _get_users()

@app.route("/select_mode", methods = ["POST"])
def select_mode():
    mode = str(request.get_json().get("mode")).lower()
    return _select_mode(mode)

@app.route("/select_colour", methods = ["POST"])
def select_colour():
    colour = str(request.get_json().get("colour")).lower()
    return _select_colour(colour)

@app.route("/make_move", methods = ["POST"])
def make_move():
    move = str(request.get_json().get("move")).lower()
    return _make_move(move)

@app.route("/let_ai_make_move", methods = ["POST"])
def let_ai_make_move():
    return _let_ai_make_move()

SSL_CERT_PATH = f"{pathlib.Path(__file__).parent.parent.resolve()}/SSL_cert"
ssl_cert = f"{SSL_CERT_PATH}/fullchain.pem"
ssl_key = f"{SSL_CERT_PATH}/privkey.pem"
app.run(debug=True,host='0.0.0.0', port=443, ssl_context=(ssl_cert,ssl_key))
