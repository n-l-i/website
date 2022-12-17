function sign_up() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'https://localhost/sign_up', {"username":email,"password":password}, load_sign_up)
    
    document.getElementById("sent").innerHTML += "<br>"+request_body;
}

function load_sign_up(response){
    document.getElementById("received").innerHTML += "<br>"+JSON.stringify(response);
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "signup failed";
        return;
    }
    document.getElementById("status_msg").innerHTML = "signup successful";
}

function list_signups(){
    if (arguments.length == 0){
        make_http_request("GET", 'https://localhost/signups', {}, list_signups);
        return;
    }
    response = arguments[0];
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "signup failed";
        return;
    }
    document.getElementById("signup_log").innerHTML = "Signed up users:";
    response.data.forEach(signup => {
            document.getElementById("signup_log").innerHTML += "<br>"+signup;
    });
}
