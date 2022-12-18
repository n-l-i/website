load_content_pages();

function load_content_pages(){
    var newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/home/home.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/chess_ai/chess_ai.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/network_simulator/network_simulator.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/ssl_certs/ssl_certs.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/about/about.js";
    document.head.appendChild(newScript);
    document.getElementById("status_msg").innerHTML = "loaded page";
    open_tab("home");
}

function open_tab(tab_name){
    document.getElementById("header").innerHTML = "";
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":token}, load_tab);
}

function load_tab(response){
    document.getElementById("tab_content").innerHTML = response.data.html;
    if (response.data.tab_name === "chess_ai") {
        load_chess_ai();
    }
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

function sign_out() {
    token = localStorage.getItem("token");
    make_http_request('POST', HOST_URL+'/sign_out', {"token":token}, load_sign_out)
}

function load_sign_out(response){
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = "sign out failed";
        return;
    }
    localStorage.removeItem("token");
    document.getElementById("status_msg").innerHTML = "sign out successful";
    window.location.reload();
}
