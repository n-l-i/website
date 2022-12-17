function sign_up() {
    email = document.getElementById("email_input").value;
    password = document.getElementById("password_input").value;
    fruit = document.getElementById("fruit_input").value;
    make_http_request('POST', HOST_URL+'/sign_up', {"username":email,"password":password,"favourite_fruit":fruit}, load_sign_up);
    
    document.getElementById("sent").innerHTML += "<br>"+request_body;
}

function load_sign_up(response){
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "signup failed";
        return;
    }
    document.getElementById("status_msg").innerHTML = "signup successful";
    list_favourite_fruits();
}

function list_favourite_fruits(){
    if (arguments.length == 0){
        make_http_request("GET", HOST_URL+'/get_favourite_fruits', {}, list_favourite_fruits);
        return;
    }
    response = arguments[0];
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "request failed";
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
