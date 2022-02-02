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
    var ind = getOnTurn(data);  
    selectStarter(ind);    
});

socket.on('join_game', (data) => {
    console.log(data);
    setPlayerDetails(data[0]);
    setOpponentDetails(data.slice(1));
});

function sendStart()
{
    socket.emit('start_game');
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
    start_but.addEventListener("click", sendStart);

    document.getElementById("player-ready").style.display = "grid";

    document.getElementById("player-name").innerText = name;
    let player_id = localStorage.getItem("player_id");
    socket.emit("join_game", {"nick": name, "player_id": player_id});

}

function selectStarter(ind)
{
    var finish = ind * 90;
    var rand = Math.random() * 10;
    rand -= 5;  
    document.documentElement.style.setProperty('--start-spin', 0 + "deg");
    document.documentElement.style.setProperty('--end-spin', (finish + 1890 + rand) + "deg");

    let spinner = document.createElement('span');
    spinner.addEventListener('animationend', startGame);
    spinner.innerText = "➤";
    spinner.id = "spinner";
    spinner.style.animation = "spin 2s ease 0s 1 normal forwards";
      
    let c_grid = document.getElementById("center-grid");
    c_grid.innerText = "";
    c_grid.appendChild(spinner);
}


function startGame()
{    
    setPlayerDetails(data[0]);
    setOpponentDetails(data.slice(1));
    var cards = document.querySelectorAll(".player-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    cards = document.querySelectorAll(".opponent-card-div");
    cards.forEach(element => element.classList.remove("hidden"));    
    document.getElementById('spinner').remove();
}

function setPlayerDetails(data)
{
    if (data.turn)
    {
        document.getElementById('player-info').classList.add("on-turn");
        var options = document.querySelectorAll(".turn-options");
        options.forEach(element => element.classList.remove("hidden"));
    }
    else
    {
        document.getElementById('player-info').classList.remove("on-turn");
        var options = document.querySelectorAll(".turn-options");
        options.forEach(element => element.classList.add("hidden"));
    }
}

function setOpponentDetails(data)
{
    for (var i = 0; i < data.length; i++) {
        var player = data[i];
        document.querySelector("#opponent" + i + "-name").innerText =  player.name;
        document.querySelector("#opponent" + i + "-money").innerText = "Coins: " + player.coins;
        if (player.turn)
        {
            document.querySelector("#opponent" + i + "-info").classList.add("on-turn");
        }
    }
}

function getOnTurn(data)
{
    var ind = 0;
    for (var i = 0; i < data.length; i++) {
        var player = data[i];
        if (player.turn)
        {
            ind = i;
        }
    }
    return ind;
}