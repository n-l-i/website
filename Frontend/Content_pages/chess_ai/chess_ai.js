function load_chess_ai(){
    localStorage.setItem("selected_tiles","");
    localStorage.setItem("targeted_tiles","");
    localStorage.setItem("turn",null);
    localStorage.setItem("legal_moves",null);
    localStorage.setItem("selected_colour",null);
    localStorage.setItem("mode",null);
    localStorage.setItem("new_turn_timestamp",null);
    localStorage.getItem("think_time",null);
    setInterval(count_down_timer, 1000);
    select_thinktime();
    select_mode();
    select_colour();
    restart_game();
    check_thinktime();
    check_mode();
    check_colour();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function count_down_timer(){
    if (document.getElementById("chess_timer") == null) {
        return;
    }
    if (localStorage.getItem("turn") == null) {
        return;
    }
    let timer_id = localStorage.getItem("turn")+"_timer";
    document.getElementById(timer_id).innerHTML = String(parseInt(document.getElementById(timer_id).innerHTML)-1);
}

function restart_game(){
    localStorage.setItem("new_turn_timestamp",Date.now());
    document.getElementById("header").innerHTML = "On this page resides a chess AI I've written.<br><div id=\"chess_timer\">Game timer:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;White:&nbsp;<p id=\"black_timer\">600</p>,&nbsp;Black:&nbsp;<p id=\"white_timer\">600</p></div>";
    colour = localStorage.getItem("selected_colour");
    mode = localStorage.getItem("mode");
    document.getElementById("move_stack").innerHTML = "";
    localStorage.setItem("turn",colour);
    token = localStorage.getItem("token");
    reset_selected_tiles();
    make_http_request('POST', HOST_URL+'/new_chessgame', {"mode":mode,"colour":colour,"token":token}, display_board);
}

function select_mode(){
    mode = document.getElementById("mode_input").value;
    localStorage.setItem("mode",mode);
    check_mode();
}

function select_colour(){
    colour = document.getElementById("colour_input").value;
    localStorage.setItem("selected_colour",colour);
    check_colour();
}

function select_thinktime(){
    thinktime = document.getElementById("thinktime_input").value
    localStorage.setItem("think_time",parseFloat(thinktime));
    check_thinktime();
}

function display_board(response){
    // If the request was sent before the turn was started, ignore the response.
    // This can happen with slow AI responses.
    if (response.timestamp < localStorage.getItem("new_turn_timestamp")){
        return;
    }
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    let ai_turn = response.data.legal_moves.length == 0;
    if (String(localStorage.getItem("turn")) != "white") {
        localStorage.setItem("turn","white");
    } else {
        localStorage.setItem("turn","black");
    }
    render_board(response.data.board,response.data.move,ai_turn);
    localStorage.setItem("legal_moves",response.data.legal_moves);
    if (typeof response.data.move != "undefined"){
        let move = response.data.move.slice(0,2)+"&#8594;"+response.data.move.slice(2);
        let last_move_row = String(document.getElementById("move_stack").innerHTML).split("<br>")[0];
        if (last_move_row.length == 0) {
            document.getElementById("move_stack").innerHTML = move;
        } else if (last_move_row.length < 7){
            let other_move_rows = String(document.getElementById("move_stack").innerHTML).slice(last_move_row.length);
            document.getElementById("move_stack").innerHTML = String(last_move_row+",").padEnd(8).replaceAll(" ","&nbsp;")+move+other_move_rows;
        } else {
            document.getElementById("move_stack").innerHTML = move+"<br>"+document.getElementById("move_stack").innerHTML;
        }
    }
    if (typeof response.data.game_is_over !== "undefined"){
        document.getElementById("chess_ai").innerHTML = "<div id=\"gameover_msg\">Game has ended, "+response.data.end_reason+".<br>Winner: "+response.data.winner+"</div><br>"+document.getElementById("chess_ai").innerHTML;
        localStorage.setItem("turn",null);
        return;
    }
    if (ai_turn){
        document.getElementById("chess_ai").innerHTML = "Waiting for AI to make a move...<br>"+document.getElementById("chess_ai").innerHTML;
        token = localStorage.getItem("token");
        think_time = localStorage.getItem("think_time");
        make_http_request('POST', HOST_URL+'/let_ai_make_move', {"thinking_time":think_time,"token":token}, display_board);
    }
}

function reset_selected_tiles(){
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
    reset_selected_tiles();
    if (is_selected_move){
        token = localStorage.getItem("token");
        make_http_request('POST', HOST_URL+'/make_move', {"move":move,"token":token}, display_board);
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

function render_board(text_board,last_move,ai_turn){
    let board = "";
    let tile_class = "light_tile";
    let piece_codes = {"p":"&#9823;","r":"&#9820;","n":"&#9822;","b":"&#9821;","k":"&#9818;","q":"&#9819;"}
    colour = localStorage.getItem("selected_colour")
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
            if (ai_turn) {
                board += "<div class=\""+tile_class+"\" id=\""+col+row+"\">";
            } else {
                board += "<div class=\""+tile_class+" clickable\" id=\""+col+row+"\" onClick=\"select_tile(this.id)\">";
            }
            board += "<pre>";
            let piece = text_board[col+row];
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
    if (typeof last_move != "undefined"){
        localStorage.setItem("selected_tiles",last_move.slice(0,2)+","+last_move.slice(2,4));
        document.getElementById(last_move.slice(0,2)).classList.add("selected_tile");
        document.getElementById(last_move.slice(2,4)).classList.add("selected_tile");
    }
}

function check_mode() {
    let new_mode = document.getElementById("mode_input").value;
    let old_mode = localStorage.getItem("mode");
    let mode_button = document.getElementById("mode_button");
    mode_button.disabled = (new_mode === old_mode);
    if (mode_button.disabled) {
        mode_button.classList.remove("clickable");
    } else {
        mode_button.classList.add("clickable");
    }
}

function check_colour() {
    let new_colour = document.getElementById("colour_input").value;
    let old_colour = localStorage.getItem("selected_colour");
    let colour_button = document.getElementById("colour_button");
    colour_button.disabled = (new_colour === old_colour);
    if (colour_button.disabled) {
        colour_button.classList.remove("clickable");
    } else {
        colour_button.classList.add("clickable");
    }
}

function check_thinktime() {
    let new_thinktime = document.getElementById("thinktime_input").value;
    if (new_thinktime > 60) {
        document.getElementById("thinktime_input").value = 60;
        new_thinktime = 60;
    }
    if (new_thinktime < 0) {
        document.getElementById("thinktime_input").value = 0;
        new_thinktime = 0;
    }
    let old_thinktime = localStorage.getItem("think_time");
    let thinktime_button = document.getElementById("thinktime_button");
    thinktime_button.disabled = (new_thinktime === old_thinktime);
    if (thinktime_button.disabled) {
        thinktime_button.classList.remove("clickable");
    } else {
        thinktime_button.classList.add("clickable");
    }
}
