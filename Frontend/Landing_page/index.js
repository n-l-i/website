window.onload = function(){
    let token = localStorage.getItem("token");
    make_http_request("POST", 'http://localhost:5000/is_signed_in', {"token":token}, open_start_tab);
}

function open_start_tab(response){
    if (response.status_code !== 200 || response.success !== true) {
        replace_html("http://localhost:5000/get_file/Frontend/Login_pages/");
        return;
    }
    replace_html("http://localhost:5000/get_file/Frontend/Content_pages/");
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
