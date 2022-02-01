const socket = io("http://81.110.114.52:3000");

socket.on('connect', () => {
    console.log('connected');
    if (!localStorage.getItem("player_id")) localStorage.setItem("player_id", document.getElementById("player_id").value);
});

socket.on('disconnect', () => {
    console.log('disconnected');
});


socket.on('start_game', (data) => {
    console.log(data);
    if (data[0].turn)
    {
        myTurn();
    }
    document.getElementById('spinner').remove();
});

function sendMessage()
{
    let msg = document.getElementById("message").value;
    socket.emit('send_message', {msg: msg});
}

function joinGame()
{
    let nick_field = document.getElementById("nick");
    let name = nick_field.value;

    if (!nick_field.value)
    {
        nick_field.style.backgroundColor = "pink";
        return;
    }

    let p_setup = document.getElementById("player-setup");
    let start_but = document.createElement('button');

    p_setup.parentElement.appendChild(start_but);
    p_setup.remove();
    start_but.innerText = "Start Game";
    start_but.classList.add("btn", "btn-success");
    start_but.style.minWidth = "200px";
    start_but.style.minHeight = "50px";
    start_but.addEventListener("click", selectStarter);

    document.getElementById("player-ready").style.display = "grid";

    document.getElementById("player-name").innerText = name;
    let player_id = localStorage.getItem("player_id");
    socket.emit("join_game", {"nick": name, "player_id": player_id});

}

function selectStarter()
{
    var rand = Math.random() * 360;  
    document.documentElement.style.setProperty('--start-spin', rand + "deg");
    document.documentElement.style.setProperty('--end-spin', (rand + 1000) + "deg");

    let spinner = document.createElement('span');
    spinner.addEventListener('animationend', startGame);
    spinner.innerText = "➤";
    spinner.id = "spinner";
    spinner.style.animation = "spin 2s ease 0s 1 normal forwards";
      
    let c_grid = document.getElementById("center-grid");
    c_grid.innerText = "";
    c_grid.appendChild(spinner);
}

function startGame(turn)
{    
    var cards = document.querySelectorAll(".player-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    socket.emit('start_game');
}

function myTurn()
{
    document.getElementById('player-info').classList.add("on-turn");
}

function notMyTurn()
{
    
}