window.onload = function(){
  document.getElementById("status_msg").innerHTML = "loaded page";
  open_tab("signin");
  setInterval(add_dashboard_data,1000);
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
