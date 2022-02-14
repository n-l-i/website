window.onload = function(){
  document.getElementById("status_msg").innerHTML = "loaded page";
  open_tab("login");
  setInterval(add_dashboard_data,1000);
}

function add_dashboard_data(){
    if (document.getElementById("dashboard") !== null) {
        document.getElementById("dashboard").innerHTML += Math.floor(Math.random()*100)+"<br>";
    }
}

function open_tab(tab_name){
    make_http_request("POST", 'http://localhost:5000/select_tab', {"tab":tab_name}, load_tab);
}

function load_tab(response){
  document.getElementById("tab_content").innerHTML = response.data;
}

function reload_page() {
    email = document.getElementById("email_input").value
    password = document.getElementById("password_input").value
    make_http_request('POST', 'http://localhost:5000/sign_in', {"username":email,"password":password}, log_in)
    
    document.getElementById("debug").innerHTML += "<br>"+request_body;
}

function log_in(response){
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
