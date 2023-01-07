function sign_in() {
    email = document.getElementById("signin_email_input").value;
    password = document.getElementById("signin_password_input").value;
    make_http_request('POST', HOST_URL+'/sign_in', {"username":email,"password":password}, load_sign_in);
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
    fruit = document.getElementById("signup_fruit_input").value;
    make_http_request('POST', HOST_URL+'/sign_up', {"username":email,"password":password,"favourite_fruit":fruit}, load_sign_up);
}

function load_sign_up(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
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
