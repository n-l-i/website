function load_chess_ai(){
    document.getElementById("header").innerHTML = "On this page resides a chess AI I've written. Select your preferred chess colour and have a go trying to beat it.";
    select_colour();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function select_colour(){
    colour = document.getElementById("colour_input").value
    make_http_request('POST', 'http://localhost:5000/select_colour', {"colour":colour}, display_board)
}

function select_move(){
    document.getElementById("status_msg").innerHTML = "processing request";
    move = document.getElementById("move_input").value;
    make_http_request('POST', 'http://localhost:5000/make_move', {"move":move}, display_board);
}

function display_board(response){
    if (response.status_code !== 200) {
        document.getElementById("status_msg").innerHTML = "move request failed";
        return;
    }
    if (response.success !== true) {
        document.getElementById("status_msg").innerHTML = response.message;
        return;
    }
    if (typeof response.data.game_is_over !== "undefined"){
        document.getElementById("chess_ai").innerHTML = "Game has ended, "+response.data.end_reason+".<br>Winner: "+response.data.winner;
        return;
    }
    render_board(response.data.board);
    document.getElementById("move_input").innerHTML = "";
    let legal_moves = response.data.legal_moves;
    legal_moves.forEach(move => {
        document.getElementById("move_input").innerHTML += "<option value=\""+move+"\">"+move+"</option>";
    });
    document.getElementById("status_msg").innerHTML = "move request successful";
    if (legal_moves.length == 0){
        document.getElementById("chess_ai").innerHTML = "Waiting for AI to make a move...<br>"+document.getElementById("chess_ai").innerHTML;
        make_http_request('POST', 'http://localhost:5000/let_ai_make_move', {}, display_board);
    }
}

function render_board(text_board){
    let board = "";
    let tile_class = "light_tile";
    let piece_codes = {"p":"&#9823;","r":"&#9820;","n":"&#9822;","b":"&#9821;","k":"&#9818;","q":"&#9819;"}
    colour = document.getElementById("colour_input").value
    let rows;
    let cols;
    if (colour === "white") {
        rows = ["8","7","6","5","4","3","2","1"];
        cols = ["a","b","c","d","e","f","g","h"];
    } else {
        rows = ["1","2","3","4","5","6","7","8"];
        cols = ["h","g","f","e","d","c","b","a"];
    }
    rows.forEach(row => {
        board += "<div class=\"chess_tile_row\">";
        cols.forEach(col => {
            board += "<div class=\""+tile_class+"\" id=\""+row+col+"\"><pre>"
            let piece = text_board[row+col]
            if (typeof piece === "undefined"){
                board += " ";
            } else if (piece.toLowerCase() === piece){
                board += piece_codes[piece];
            } else {
                board += "&#"+String(parseInt(piece_codes[piece.toLowerCase()].slice(2,6))-6)+";";
            }
            board += "</pre></div>";
            if (tile_class === "light_tile"){
                tile_class = "dark_tile";
            } else {
                tile_class = "light_tile";
            }
        });
        if (tile_class === "light_tile"){
            tile_class = "dark_tile";
        } else {
            tile_class = "light_tile";
        }
        board += "</div>";
    });
    document.getElementById("chess_ai").innerHTML = board;
}
