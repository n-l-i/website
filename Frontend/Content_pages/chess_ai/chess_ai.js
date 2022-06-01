function select_colour(){
    document.getElementById("chess_ai").innerHTML = "hej";
    colour = document.getElementById("colour_input").value
    make_http_request('POST', 'http://localhost:5000/select_colour', {"colour":colour}, display_board)
}

function select_move(){
    document.getElementById("chess_ai").innerHTML = "Waiting for AI to make a move...<br>"+document.getElementById("chess_ai").innerHTML;
    move = document.getElementById("move_input").value
    make_http_request('POST', 'http://localhost:5000/make_move', {"move":move}, display_board)
}

function display_board(response){
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = response.message;
        return;
    }
    document.getElementById("chess_ai").innerHTML = response.data.board;
    document.getElementById("move_input").innerHTML = "";
    console.log(response);
    response.data.legal_moves.forEach(move => {
        document.getElementById("move_input").innerHTML += "<option value=\""+move+"\">"+move+"</option>";
    });

}
