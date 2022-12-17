function sign_in() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'https://localhost/sign_in', {"username":email,"password":password}, load_sign_in)
    
    document.getElementById("sent").innerHTML += "<br>"+request_body;
}

function load_sign_in(response){
    document.getElementById("received").innerHTML += "<br>"+JSON.stringify(response);
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "login failed";
        return;
    }
    localStorage.setItem("token",response.data);
    document.getElementById("status_msg").innerHTML = "login successful";
    window.location.reload();
}
