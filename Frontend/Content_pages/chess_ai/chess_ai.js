function load_chess_ai(){
    document.getElementById("header").innerHTML = "On this page resides a chess AI I've written. Select your preferred chess colour and have a go trying to beat it.";
    localStorage.setItem("selected_tiles","");
    localStorage.setItem("targeted_tiles","");
    select_colour();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function select_colour(){
    colour = document.getElementById("colour_input").value
    make_http_request('POST', 'http://localhost:5000/select_colour', {"colour":colour}, display_board)
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
        document.getElementById("chess_ai").innerHTML = "Game has ended, "+response.data.end_reason+".<br>Winner: "+response.data.winner+"<br>"+document.getElementById("chess_ai").innerHTML;
    }
    render_board(response.data.board);
    localStorage.setItem("legal_moves",response.data.legal_moves);
    document.getElementById("status_msg").innerHTML = "move request successful";
    if (response.data.legal_moves.length == 0){
        document.getElementById("chess_ai").innerHTML = "Waiting for AI to make a move...<br>"+document.getElementById("chess_ai").innerHTML;
        make_http_request('POST', 'http://localhost:5000/let_ai_make_move', {}, display_board);
    }
}

function select_tile(div_id){
    if (String(localStorage.getItem("legal_moves")).length == 0){
        return;
    }
    if (String(localStorage.getItem("selected_tiles")) == div_id){
        return;
    }
    let is_selected_move = String(localStorage.getItem("targeted_tiles")).includes(div_id);
    let move = String(localStorage.getItem("selected_tiles"))+div_id;
    if (!String(localStorage.getItem("legal_moves")+",").includes(move+",")){
        move += "q";
    }
    console.log(is_selected_move);
    console.log(move);
    String(localStorage.getItem("targeted_tiles")).split(",").forEach(targeted_id => {
        if (targeted_id.length > 0){
            document.getElementById(targeted_id).classList.remove("targeted_tile");
        }
    });
    localStorage.setItem("targeted_tiles","");
    String(localStorage.getItem("selected_tiles")).split(",").forEach(selected_id => {
        if (selected_id.length > 0){
            document.getElementById(selected_id).classList.remove("selected_tile");
        }
    });
    localStorage.setItem("selected_tiles","");
    if (is_selected_move){
        make_http_request('POST', 'http://localhost:5000/make_move', {"move":move}, display_board);
        return;
    }
    String(localStorage.getItem("legal_moves")).split(",").forEach(move => {
        if (move.slice(0,2) == div_id) {
            document.getElementById(move.slice(2,4)).classList.add("targeted_tile");
            localStorage.setItem("targeted_tiles",move.slice(2,4)+","+localStorage.getItem("targeted_tiles"));
        }
    });
    localStorage.setItem("selected_tiles",div_id);
    document.getElementById(div_id).classList.add("selected_tile");
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
            board += "<div class=\""+tile_class+"\" id=\""+col+row+"\" onClick=\"select_tile(this.id)\"><pre>"
            let piece = text_board[col+row]
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
