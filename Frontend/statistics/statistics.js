function get_statistics_data(){
    make_http_request("GET", 'http://localhost:5000/get_users', {}, load_statistics_data);
}

function load_statistics_data(response){
    response.data.forEach((item,index) => {
        document.getElementById("statistics").innerHTML += item[0]+" - "+item[1]+"<br>";
    });
}
