load_login_pages();

function load_login_pages(){
    var newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Login_pages/home/home.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Login_pages/signup/signup.js";
    document.head.appendChild(newScript);
    newScript = document.createElement("script");
    newScript.src = HOST_URL+"/get_file/Frontend/Content_pages/about/about.js";
    document.head.appendChild(newScript);
    document.getElementById("status_msg").innerHTML = "loaded page";
    open_tab("home");
}

function open_tab(tab_name){
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":null}, load_tab);
}

function load_tab(response){
  document.getElementById("tab_content").innerHTML = response.data.html;
  if (response.data.tab_name === "home") {
    list_favourite_fruits();
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
