function sign_up() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'http://localhost:5000/sign_up', {"username":email,"password":password}, load_sign_up)
    
    document.getElementById("debug").innerHTML += "<br>"+request_body;
}

function load_sign_up(response){
    document.getElementById("results").innerHTML += "<br>"+JSON.stringify(response);
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
