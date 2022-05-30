from sqlite3 import connect,IntegrityError

DB_PATH = "Backend/database.db"

def _open_connection():
    db_connection = connect(DB_PATH)
    db_cursor = db_connection.cursor()
    db_connection.execute("PRAGMA foreign_keys = ON;")
    return db_cursor

def _close_connection(db_cursor):
    db_connection = db_cursor.connection
    db_cursor.close()
    db_connection.close()

def init_db():
    db_connection = _open_connection()
    db_connection.execute("BEGIN;")
    db_connection.execute("CREATE TABLE IF NOT EXISTS users ("+ \
                            "username TEXT NOT NULL,"+ \
                            "password TEXT NOT NULL,"+ \
                            "PRIMARY KEY (username));")
    db_connection.execute("COMMIT;")
    db_connection.execute("BEGIN;")
    db_connection.execute("CREATE TABLE IF NOT EXISTS logins ("+ \
                            "token TEXT NOT NULL,"+ \
                            "username TEXT NOT NULL,"+ \
                            "issued_timestamp INT NOT NULL,"+ \
                            "PRIMARY KEY (token),"+ \
                            "FOREIGN KEY (username) REFERENCES users (username));")
    db_connection.execute("COMMIT;")
    _close_connection(db_connection)

def create_user(username, password):
    user = (username, password)
    try:
        db_connection = _open_connection()
        db_connection.execute("BEGIN;")
        db_connection.execute("INSERT INTO users VALUES (?,?);",user)
        db_connection.execute("COMMIT;")
        _close_connection(db_connection)
        return (True,None)
    except IntegrityError:
        return (True,None)
    except:
        return (False,None)

def create_login(username, token, issued_timestamp):
    login = (token,username,issued_timestamp)
    try:
        db_connection = _open_connection()
        db_connection.execute("BEGIN;")
        db_connection.execute("INSERT OR REPLACE INTO logins VALUES (?,?,?);",login)
        db_connection.execute("COMMIT;")
        _close_connection(db_connection)
        return (True,None)
    except:
        return (False,None)

def log_out_user(token):
    try:
        db_connection = _open_connection()
        try:
            result = [results for results in db_connection.execute("SELECT * FROM logins WHERE token = "+token+";")]
            return result
        except:
            return False
            db_connection.execute("BEGIN;")
            db_connection.execute("DELETE FROM logins WHERE token = "+token+";")
            db_connection.execute("COMMIT;")
            _close_connection(db_connection)
            return True
    except:
        return False

def is_valid_token(token):
    try:
        db_connection = _open_connection()
        db_connection.execute("SELECT token FROM logins WHERE token = \""+token+"\";")
        valid_tokens = db_connection.fetchone()
        _close_connection(db_connection)
        if valid_tokens is None:
            return (True,False)
        return (True,True)
    except:
        return (False,False)

def select_password(username):
    try:
        db_connection = _open_connection()
        db_connection.execute("SELECT password FROM users WHERE username = \""+username+"\";")
        password = db_connection.fetchone()
        _close_connection(db_connection)
        if password is None:
            return (True,None)
        return (True,password[0])
    except:
        return (False,None)

def select_users():
    try:
        db_connection = _open_connection()
        db_connection.execute("SELECT * FROM users;")
        users = db_connection.fetchall()
        _close_connection(db_connection)
        if users is None:
            return (True,None)
        return (True,users)
    except:
        return (False,None)
