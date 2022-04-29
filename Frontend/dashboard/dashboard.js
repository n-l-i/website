function add_dashboard_data(){
    if (document.getElementById("dashboard") !== null) {
        document.getElementById("dashboard").innerHTML += Math.floor(Math.random()*100)+"<br>";
    }
}
