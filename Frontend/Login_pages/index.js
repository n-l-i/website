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
    open_tab("signin");
}

function open_tab(tab_name){
    make_http_request("POST", HOST_URL+'/get_tab', {"tab":tab_name,"token":null}, load_tab);
}

function load_tab(response){
  document.getElementById("tab_content").innerHTML = response.data.html;
  if (response.data.tab_name === "signin") {
    list_favourite_fruits();
  }
}
