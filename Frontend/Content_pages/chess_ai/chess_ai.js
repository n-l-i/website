function load_chess_ai(){
    chess_ai_adjust_layout();
    localStorage.setItem("selected_tiles","");
    localStorage.setItem("targeted_tiles","");
    localStorage.setItem("turn",null);
    localStorage.setItem("legal_moves",null);
    localStorage.setItem("selected_colour",null);
    localStorage.setItem("mode",null);
    localStorage.setItem("turn_start_timestamp",null);
    localStorage.getItem("white_time_left",null);
    localStorage.getItem("black_time_left",null);
    localStorage.getItem("think_time",null);
    setInterval(count_down_timer, 100);
    select_thinktime();
    select_mode();
    select_colour();
    restart_game();
    check_thinktime();
    check_mode();
    check_colour();
}

previous_display_board_response = null;

function chess_ai_adjust_layout() {
    let move_stack = null;
    if (document.getElementById("move_stack")) {
        move_stack = document.getElementById("move_stack").innerHTML;
    }
    if (window.innerHeight > window.innerWidth) {
        document.getElementById("chess_page").innerHTML = document.getElementById("vertical_layout").innerHTML;
    } else {
        document.getElementById("chess_page").innerHTML = document.getElementById("horizontal_layout").innerHTML;
    }
    document.getElementById("chess_menu").innerHTML = document.getElementById("chess_menu_contents").innerHTML;
    if (move_stack) {
        document.getElementById("move_stack").innerHTML = move_stack;
    }
    if (previous_display_board_response) {
        previous_display_board_response.timestamp = Date.now();
        display_board(previous_display_board_response);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function count_down_timer(){
    if (!document.getElementById("white_timer")) {
        return;
    }
    if (localStorage.getItem("turn") == null) {
        return;
    }
    let timer_id = localStorage.getItem("turn")+"_timer";
    let time_left_key = localStorage.getItem("turn")+"_time_left";
    let time_step = Date.now()-parseInt(localStorage.getItem("turn_start_timestamp"));
    let time_left = parseInt(localStorage.getItem(time_left_key))-time_step;
    if (time_left >= 20000 || time_left <= 0) {
        time_left = Math.ceil(time_left/1000);
    } else {
        time_left = (Math.ceil(time_left/100)/10).toFixed(1);
    }
    if (time_left >= 0) {
        document.getElementById(timer_id).innerHTML = String(time_left);
    } else {
        document.getElementById(timer_id).innerHTML = String(-time_left)+" (overtime)";
    }
}

function restart_game(){
    localStorage.setItem("turn_start_timestamp",Date.now());
    document.getElementById("white_timer").innerHTML = "600";
    localStorage.setItem("white_time_left", 600000);
    document.getElementById("black_timer").innerHTML = "600";
    localStorage.setItem("black_time_left", 600000);
    colour = localStorage.getItem("selected_colour");
    mode = localStorage.getItem("mode");
    document.getElementById("move_stack").innerHTML = '<div class="item container container--row"></div>';
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
    thinktime = document.getElementById("thinktime_input").value;
    localStorage.setItem("think_time",parseFloat(thinktime));
    check_thinktime();
}

function display_board(response){
    // If the request was sent before the turn was started, ignore the response.
    // This can happen with slow AI responses.
    if (response.timestamp < localStorage.getItem("turn_start_timestamp")){
        return;
    }
    if (response.status_code !== 200 || response.success !== true) {
        show_status_message(response.message);
        return;
    }
    let time_spent = Date.now()-localStorage.getItem("turn_start_timestamp");
    localStorage.setItem("turn_start_timestamp",Date.now());
    let time_left = localStorage.getItem("turn_start_timestamp");
    previous_display_board_response = response;
    let ai_turn = response.data.legal_moves.length == 0;
    if (String(localStorage.getItem("turn")) != "white") {
        localStorage.setItem("turn","white");
        localStorage.setItem("black_time_left", parseInt(localStorage.getItem("black_time_left"))-time_spent);
    } else {
        localStorage.setItem("turn","black");
        localStorage.setItem("white_time_left", parseInt(localStorage.getItem("white_time_left"))-time_spent);
    }
    render_board(response.data.board,response.data.move,ai_turn);
    localStorage.setItem("legal_moves",response.data.legal_moves);
    if (typeof response.data.move != "undefined"){
        let move = response.data.move.slice(0,2)+"&#8594;"+response.data.move.slice(2);
        update_move_stack(move);
    }
    if (typeof response.data.game_is_over !== "undefined"){
        document.getElementById("chess_ai").innerHTML = "<div id=\"gameover_msg\">Game has ended, "+response.data.end_reason+".<br>Winner: "+response.data.winner+"</div><br>"+document.getElementById("chess_ai").innerHTML;
        localStorage.setItem("turn",null);
        return;
    }
    if (ai_turn){
        document.getElementById("chess_ai").innerHTML = "<div>Waiting for AI to make a move...</div>"+document.getElementById("chess_ai").innerHTML;
        token = localStorage.getItem("token");
        think_time = localStorage.getItem("think_time");
        make_http_request('POST', HOST_URL+'/let_ai_make_move', {"thinking_time":think_time,"token":token}, display_board);
    }
}

function update_move_stack(move){
    let top_row = document.getElementById("move_stack").children[0];
    if (document.getElementById("move_stack").children[0].children.length == 0) {
        document.getElementById("move_stack").children[0].innerHTML = "<p>"+move+"</p>";
    } else if (document.getElementById("move_stack").children[0].children.length == 1){
        document.getElementById("move_stack").children[0].innerHTML += "<p>,&nbsp;</p><p>"+move+"</p>";
    } else {
        document.getElementById("move_stack").innerHTML = '<div class="item container container--row"><p>'+move+'</p></div>'+document.getElementById("move_stack").innerHTML;
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
        board += "<div class=\"item item--big item--fill container container--row\">";
        cols.forEach(col => {
            if (ai_turn) {
                board += "<div class=\"item item--big item--fill container container--chess_tile "+tile_class+"\" id=\""+col+row+"\">";
            } else {
                board += "<div class=\"item item--big item--fill container container--chess_tile "+tile_class+" clickable\" id=\""+col+row+"\" onClick=\"select_tile(this.id)\">";
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
