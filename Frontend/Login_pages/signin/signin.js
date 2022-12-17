function sign_in() {
    email = document.getElementById("email_input").value;
    password = document.getElementById("password_input").value;
    make_http_request('POST', HOST_URL+'/sign_in', {"username":email,"password":password}, load_sign_in);
}

function load_sign_in(response){
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
