window.onload = function(){
  document.getElementById("status_msg").innerHTML = "loaded page";
  open_tab("signin");
  setInterval(add_dashboard_data,1000);
}

function add_dashboard_data(){
    if (document.getElementById("dashboard") !== null) {
        document.getElementById("dashboard").innerHTML += Math.floor(Math.random()*100)+"<br>";
    }
}

function get_statistics_data(){
    make_http_request("GET", 'http://localhost:5000/get_users', {}, load_statistics_data);
}

function load_statistics_data(response){
    response.data.forEach((item,index) => {
        document.getElementById("statistics").innerHTML += item[0]+" - "+item[1]+"<br>";
    });
}

function open_tab(tab_name){
    make_http_request("POST", 'http://localhost:5000/get_tab', {"tab":tab_name}, load_tab);
    if (tab_name === "statistics") {
        get_statistics_data();
    }
}

function load_tab(response){
  document.getElementById("tab_content").innerHTML = response.data;
}

function sign_in() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'http://localhost:5000/sign_in', {"username":email,"password":password}, load_sign_in)
    
    document.getElementById("debug").innerHTML += "<br>"+request_body;
}

function sign_up() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'http://localhost:5000/sign_up', {"username":email,"password":password}, load_sign_up)
    
    document.getElementById("debug").innerHTML += "<br>"+request_body;
}

function load_sign_in(response){
    document.getElementById("results").innerHTML += "<br>"+JSON.stringify(response);
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "login failed";
        return;
    }
    document.getElementById("status_msg").innerHTML = "login successful, token = "+response.data;
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

function make_http_request(method,url,data,onload){
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open(method, url, true);
    
    xmlhttp.onload = function () {
        let success = JSON.parse(xmlhttp.response).success === true;
        let message = JSON.parse(xmlhttp.response).message;
        let data = JSON.parse(xmlhttp.response).data;
        onload({"status_code":xmlhttp.status,"success":success,"message":message,"data":data});
    };
    xmlhttp.timeout = 300000;
    xmlhttp.ontimeout = function (e) {
        onload({"status_code":xmlhttp.status,"success":false,"message":"Request timed out.","data":null});
    };

    xmlhttp.setRequestHeader('Content-type', 'application/json')
    request_body = JSON.stringify(data);
    xmlhttp.send(request_body);
}
