function sign_in() {
    email = document.getElementById("signin_email_input").value;
    password = document.getElementById("signin_password_input").value;
    if (email.length === 0 || password.length === 0) {
        show_status_message("Both email and password need to be provided.");
        return;
    }
    if (email.length < 3 || !email.includes("@") || password.length < 12) {
        show_status_message("Wrong email or password.");
        return;
    }
    hash(password,document.URL+email).then((password_hash) => {
        let data = {"username":email,
                    "password":password_hash};
        make_http_request('POST',HOST_URL+'/sign_in',data,load_sign_in);
    });
}

function load_sign_in(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    localStorage.setItem("token",response.data);
    window.location.reload();
}

function sign_up() {
    email = document.getElementById("signup_email_input").value;
    password = document.getElementById("signup_password_input").value;
    repeat_password = document.getElementById("signup_repeat_password_input").value;
    fruit = document.getElementById("signup_fruit_input").value;
    if (email.length === 0 || password.length === 0) {
        show_status_message("Both email and password need to be provided.");
        return;
    }
    if (email.length < 3 || !email.includes("@")) {
        show_status_message("A valid email needs to be provided.");
        return;
    }
    if (password.length < 12) {
        show_status_message("Password needs to be at least 12 characters long.");
        return;
    }
    if (password !== repeat_password) {
        show_status_message("The passwords do not match each other.");
        return;
    }
    if (fruit.length > 32) {
        show_status_message("The name of this fruit is too long.");
        return;
    }
    hash(password,document.URL+email).then((password_hash) => {
        let data = {"username":email,
                    "password":password_hash,
                    "favourite_fruit":fruit};
        make_http_request('POST',HOST_URL+'/sign_up',data,load_sign_up);
    });
}

function load_sign_up(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    show_status_message(response.message,false);
    list_favourite_fruits();
}

function list_favourite_fruits(){
    if (arguments.length == 0){
        make_http_request("GET", HOST_URL+'/get_favourite_fruits', {}, list_favourite_fruits);
        return;
    }
    response = arguments[0];
    if (response.status_code !== 200) {
        document.getElementById("fruits_log").innerHTML = "Failed to fetch list of common favourite fruits from the server.";
        return;
    }
    if (response.success !== true) {
        document.getElementById("fruits_log").innerHTML = "Failed to fetch list of common favourite fruits from the server.";
        return;
    }
    document.getElementById("fruits_log").innerHTML = "Some fruits other users like:";
    let i = 0;
    response.data.forEach(favourite_fruit => {
        if (i < 10) {
            document.getElementById("fruits_log").innerHTML +=
                            "<br>&nbsp;&nbsp;&nbsp;&nbsp;"+favourite_fruit;
        }
        i += 1;
    });
}
