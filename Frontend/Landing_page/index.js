window.onload = function(){
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/is_signed_in', {"token":token}, open_start_tab);
}

function open_start_tab(response){
    if (response.status_code !== 200 || response.success !== true) {
        replace_html(HOST_URL+"/get_file/Frontend/Login_pages/");
        localStorage.removeItem("token");
        return;
    }
    replace_html(HOST_URL+"/get_file/Frontend/Content_pages/");
}

function replace_html(url){
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url+"index.html", true);

    xmlhttp.onload = function () {
        let html = xmlhttp.response;
        document.getElementsByTagName("html")[0].innerHTML = html;
        var newScript = document.createElement("script");
        newScript.src = url+"index.js";
        document.head.appendChild(newScript);
    };
    xmlhttp.timeout = 300000;
    xmlhttp.ontimeout = function (e) {
        return;
    };

    xmlhttp.setRequestHeader('Content-type', 'application/json')
    xmlhttp.send();
}

function make_http_request(method,url,data,onload){
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open(method, url, true);

    xmlhttp.onload = function () {
        let response = JSON.parse(xmlhttp.response);
        let success = response.success === true;
        let message = ("message" in response) ?
            response.message : "The http request failed with status code: "+xmlhttp.status+".";
        let data = response.data;
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

function show_status_message(message,is_warning = true) {
    document.getElementById("status_msg_text").innerHTML = message;
    if (is_warning){
        document.getElementById("status_msg_box").classList.add('warning');
    } else {
        document.getElementById("status_msg_box").classList.remove('warning');
    }
    document.getElementById("status_msg").classList.toggle('visible');
    document.getElementById("tabs").classList.toggle('blurred');
    document.getElementById("tab_content").classList.toggle('blurred');
}
