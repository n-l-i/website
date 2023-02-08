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
    prev_tab_name = localStorage.getItem("tab");
    open_tab(prev_tab_name);
    localStorage.setItem("server_time_diff",0);
    make_http_request('GET', HOST_URL+'/get_current_timestamp', {}, set_reference_time);
    setInterval(update_time_display, 100);
}

function open_tab(tab_name){
    prev_tab_name = localStorage.getItem("tab");
    if (prev_tab_name && document.getElementById(prev_tab_name+"_tab")) {
        document.getElementById(prev_tab_name+"_tab").classList.add("clickable");
    }
    if (!tab_name || !document.getElementById(tab_name+"_tab")) {
        tab_name = "home";
    }
    localStorage.setItem("tab",tab_name);
    document.getElementById(tab_name+"_tab").classList.remove("clickable");
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":token}, load_tab);
}

function load_tab(response){
    if (response.data.tab_name === "home" || response.data.tab_name === "about") {
        document.getElementById("projects_tab").innerHTML = "Projects";
    } else {
        document.getElementById("projects_tab").innerHTML = document.getElementById(response.data.tab_name+"_tab").innerHTML;
    }
    document.getElementById("tab_content").innerHTML = response.data.html;
    if (response.data.tab_name === "chess_ai") {
        load_chess_ai();
    }
}

function sign_out() {
    token = localStorage.getItem("token");
    make_http_request('POST', HOST_URL+'/sign_out', {"token":token}, load_sign_out)
}

function load_sign_out(response){
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    localStorage.removeItem("token");
    window.location.reload();
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
