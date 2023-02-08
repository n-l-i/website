load_login_pages();

function load_login_pages(){
    var newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Login_pages/signin/signin.js";
    document.head.appendChild(newScript);
    var newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Login_pages/signin/cryptography.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/about/about.js";
    document.head.appendChild(newScript);
    prev_tab_name = localStorage.getItem("tab");
    open_tab(prev_tab_name);
    setInterval(update_time_display, 100);
}

function open_tab(tab_name){
    prev_tab_name = localStorage.getItem("tab");
    if (prev_tab_name && document.getElementById(prev_tab_name+"_tab")) {
        document.getElementById(prev_tab_name+"_tab").classList.add("clickable");
    }
    if (!tab_name || !document.getElementById(tab_name+"_tab")) {
        tab_name = "signin";
    }
    localStorage.setItem("tab",tab_name);
    document.getElementById(tab_name+"_tab").classList.remove("clickable");
    let token = localStorage.getItem("token");
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":null}, load_tab);
}

function load_tab(response){
    document.getElementById("tab_content").innerHTML = response.data.html;
    if (response.data.tab_name === "signin") {
        list_favourite_fruits();
    }
}

function update_time_display(){
    const timeElapsed = Date.now();
    const today = new Date(timeElapsed);
    document.getElementById("current_date").innerHTML = today.toLocaleDateString();
    document.getElementById("current_time").innerHTML = today.toLocaleTimeString();
    document.getElementById("current_timestamp").innerHTML = Date.now();
}
