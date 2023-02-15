window.onload = function(){
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/is_signed_in', {"token":token}, open_start_tab);
}

window.onresize = function(){
    if (!localStorage.getItem("tab")) {
        return;
    }
    if (localStorage.getItem("tab") == "chess_ai") {
        chess_ai_adjust_layout();
    }
}

function open_start_tab(response){
    if (response.status_code !== 200 || response.success !== true || response.data !== true) {
        replace_html(HOST_URL+"/get_file/Frontend/Login_pages/index.html");
        init_page();
        localStorage.removeItem("token");
        return;
    }
    replace_html(HOST_URL+"/get_file/Frontend/Content_pages/index.html");
    init_page();
}

function replace_html(url){
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, true);
    xmlhttp.onload = function () {
        let html = xmlhttp.response;
        document.getElementsByTagName("body")[0].innerHTML = html;
        if (localStorage.getItem("token")) {
            localStorage.setItem("tab", "home");
            init_page();
        } else {
            localStorage.setItem("tab", "signin");
            init_page();
        }
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
        onload({"status_code":xmlhttp.status,"success":success,"message":message,"data":data,"timestamp":xmlhttp.timestamp});
    };
    xmlhttp.timeout = 300000;
    xmlhttp.ontimeout = function (e) {
        onload({"status_code":xmlhttp.status,"success":false,"message":"Request timed out.","data":null,"timestamp":xmlhttp.timestamp});
    };

    xmlhttp.setRequestHeader('Content-type', 'application/json')
    request_body = JSON.stringify(data);
    xmlhttp.send(request_body);
    xmlhttp.timestamp = Date.now();
}

function show_status_message(message,is_warning = true) {
    document.getElementById("status_msg_text").innerHTML = message;
    if (is_warning){
        document.getElementById("status_msg_box").classList.add('warning');
    } else {
        document.getElementById("status_msg_box").classList.remove('warning');
    }
    document.getElementById("status_msg_background").classList.toggle('visible');
    document.getElementById("tab_menu").classList.toggle('blurred');
    document.getElementById("tab_content").classList.toggle('blurred');
}

function init_page(){
    prev_tab_name = localStorage.getItem("tab");
    open_tab(prev_tab_name);
    localStorage.setItem("server_time_diff",0);
    make_http_request('GET', HOST_URL+'/get_current_timestamp', {}, set_reference_time);
    setInterval(update_time_display, 100);
}

function sign_out() {
    let token = localStorage.getItem("token");
    make_http_request('POST', HOST_URL+'/sign_out', {"token":token}, load_sign_out)
}

function load_sign_out(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    localStorage.removeItem("token");
    replace_html(HOST_URL+"/get_file/Frontend/Login_pages/index.html");
}

function open_tab(tab_name){
    prev_tab_name = localStorage.getItem("tab");
    if (prev_tab_name && document.getElementById(prev_tab_name+"_tab")) {
        document.getElementById(prev_tab_name+"_tab").classList.add("clickable");
        document.getElementById(prev_tab_name+"_tab").classList.remove("selected");
        if (document.getElementById("projects_tab")) {
            document.getElementById("projects_tab").classList.remove("selected");
        }
    }
    if (!tab_name || !document.getElementById(tab_name+"_tab")) {
        if (document.getElementById("projects_tab")) {
            tab_name = "home";
        } else {
            tab_name = "signin";
        }
    }
    localStorage.setItem("tab",tab_name);
    if (!document.getElementById(tab_name+"_tab")){
        return;
    }
    document.getElementById(tab_name+"_tab").classList.remove("clickable");
    document.getElementById(tab_name+"_tab").classList.add("selected");
    if (document.getElementById("projects_tab") && !["home","about"].includes(tab_name)) {
        document.getElementById("projects_tab").classList.add("selected");
    }
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":token}, load_tab);
}

function load_tab(response){
    document.getElementById("tab_content").innerHTML = response.data.html;
    if (response.data.tab_name === "signin") {
        list_favourite_fruits();
    }
    if (response.data.tab_name === "chess_ai") {
        load_chess_ai();
    }
    if (document.getElementById("projects_tab")) {
        if (response.data.tab_name === "home" || response.data.tab_name === "about") {
            document.getElementById("projects_tab").innerHTML = "Projects";
        } else {
            document.getElementById("projects_tab").innerHTML = document.getElementById(response.data.tab_name+"_tab").innerHTML;
        }
    }
}

function set_reference_time(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    localStorage.setItem("server_time_diff",response.data-Date.now());
    const server_time_diff = localStorage.getItem("server_time_diff");
}

function update_time_display(){
    const server_time_diff = parseInt(localStorage.getItem("server_time_diff"));
    const timeElapsed = Date.now()+server_time_diff;
    const today = new Date(timeElapsed);
    document.getElementById("current_date").innerHTML = today.toLocaleDateString();
    document.getElementById("current_time").innerHTML = today.toLocaleTimeString();
    document.getElementById("current_timestamp").innerHTML = timeElapsed;
}
